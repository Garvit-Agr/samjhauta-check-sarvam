import io
from typing import Tuple
from pypdf import PdfReader
import httpx
from samjhautacheck.config import SARVAM_API_KEY, SARVAM_DOC_URL


def extract_text_from_pdf_pypdf(file_bytes: bytes) -> str:
    """Extracts text from digital PDF using local pypdf for instantaneous processing."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for i, page in enumerate(reader.pages):
            page_content = page.extract_text()
            if page_content:
                pages_text.append(f"--- Page {i + 1} ---\n{page_content.strip()}")
        return "\n\n".join(pages_text).strip()
    except Exception as e:
        return ""


async def extract_text_with_sarvam_doc_ai(
    file_bytes: bytes, filename: str
) -> str:
    """Sends scanned PDF or document image to Sarvam Document/Vision Digitisation API."""
    if not SARVAM_API_KEY:
        return ""

    headers = {"api-subscription-key": SARVAM_API_KEY}
    files = {"file": (filename, file_bytes)}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                SARVAM_DOC_URL, headers=headers, files=files
            )
            if response.status_code in (200, 201, 202):
                data = response.json()
                # If job based, check if result is immediately returned or text is inside
                if "extracted_text" in data:
                    return data["extracted_text"]
                if "text" in data:
                    return data["text"]
                if "job_id" in data:
                    job_id = data["job_id"]
                    # Poll for a short time (up to 3 attempts)
                    for _ in range(3):
                        status_res = await client.get(
                            f"https://api.sarvam.ai/doc-ai/v1/job/{job_id}/status",
                            headers=headers,
                        )
                        if status_res.status_code == 200:
                            job_data = status_res.json()
                            if job_data.get("status") == "COMPLETED":
                                return job_data.get("output", {}).get(
                                    "text", ""
                                )
    except Exception:
        pass
    return ""


async def ingest_document(
    file_bytes: bytes, filename: str, content_type: str = ""
) -> Tuple[str, str]:
    """Ingests a document (PDF, Text, or Image) and returns (extracted_text, method_used)."""
    filename_lower = filename.lower()

    # Plain text / Markdown
    if (
        filename_lower.endswith(".txt")
        or filename_lower.endswith(".md")
        or "text/plain" in content_type
    ):
        try:
            return file_bytes.decode("utf-8", errors="replace"), "plain_text"
        except Exception:
            return file_bytes.decode("latin-1", errors="replace"), "plain_text"

    # PDF Document
    if filename_lower.endswith(".pdf") or "pdf" in content_type:
        # Step 1: Fast local pypdf extraction
        pypdf_text = extract_text_from_pdf_pypdf(file_bytes)
        if len(pypdf_text.strip()) >= 50:
            return pypdf_text, "pypdf_local"

        # Step 2: Fallback to Sarvam Doc AI if pypdf extracted empty/scanned pages
        if SARVAM_API_KEY:
            doc_ai_text = await extract_text_with_sarvam_doc_ai(
                file_bytes, filename
            )
            if doc_ai_text:
                return doc_ai_text, "sarvam_doc_ai"

        if pypdf_text:
            return pypdf_text, "pypdf_local_partial"

        return (
            "Warning: This PDF appears to be a scanned image with no embedded text. "
            "Please provide a digital PDF, paste the contract text directly, or configure a SARVAM_API_KEY with Vision credits.",
            "unreadable_scanned_pdf",
        )

    # Images (JPG, PNG, TIFF)
    if (
        filename_lower.endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp"))
        or "image/" in content_type
    ):
        if SARVAM_API_KEY:
            doc_ai_text = await extract_text_with_sarvam_doc_ai(
                file_bytes, filename
            )
            if doc_ai_text:
                return doc_ai_text, "sarvam_vision"
        return (
            "Image received. To transcribe scanned contract images via Sarvam OCR, ensure your SARVAM_API_KEY is configured in .env. Alternatively, you can paste the contract text directly.",
            "image_ocr_pending",
        )

    # Fallback to UTF-8 decoding
    try:
        return file_bytes.decode("utf-8", errors="replace"), "fallback_text"
    except Exception:
        return "", "unsupported_format"
