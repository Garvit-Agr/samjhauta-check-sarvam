from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from samjhautacheck.config import (
    SARVAM_API_KEY,
    SARVAM_LLM_MODEL,
    SARVAM_TTS_MODEL,
    SARVAM_TRANSLATE_MODEL,
    STATIC_DIR,
    LANGUAGE_MAP,
)
from samjhautacheck.db import (
    init_db,
    compute_hash,
    get_cached_audit,
    save_cached_audit,
)
from samjhautacheck.demo_data import (
    DEMO_RENTAL_AGREEMENT,
    DEMO_AUDIT_REPORT,
    REGIONAL_BRIEFING_SCRIPTS,
)
from samjhautacheck.ingestion import ingest_document
from samjhautacheck.models import AnalysisResponse
from samjhautacheck.sarvam_client import (
    audit_contract_with_sarvam,
    translate_spoken_script,
    synthesize_spoken_briefing,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database on startup
    init_db()
    yield


app = FastAPI(
    title="SamjhautaCheck API",
    description="AI-powered Fine-Print Trap Detector & Negotiation Coach built on Sarvam AI",
    version="1.0.0",
    lifespan=lifespan,
)

# Ensure static directory exists and mount static assets
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def get_index():
    """Serves the Single-Page Application interface."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse(
        {
            "message": "SamjhautaCheck Backend is Running. Frontend index.html loading..."
        }
    )


@app.get("/api/status")
async def get_status():
    """Returns system status, active models, and Sarvam AI configuration status."""
    return {
        "status": "healthy",
        "sarvam_configured": bool(SARVAM_API_KEY and len(SARVAM_API_KEY) > 5),
        "api_key_masked": (
            f"sk_...{SARVAM_API_KEY[-4:]}"
            if SARVAM_API_KEY and len(SARVAM_API_KEY) > 5
            else "Not configured (Running in Intelligent Local Demo Mode)"
        ),
        "models": {
            "llm": SARVAM_LLM_MODEL,
            "tts": SARVAM_TTS_MODEL,
            "translate": SARVAM_TRANSLATE_MODEL,
        },
        "supported_languages": list(LANGUAGE_MAP.keys()),
    }


@app.get("/api/demo")
async def get_demo_text():
    """Returns the pre-wired realistic predatory rental agreement text."""
    return {
        "title": "Bangalore 11-Month Residential Tenancy Agreement (Predatory Draft)",
        "text": DEMO_RENTAL_AGREEMENT.strip(),
    }


@app.post("/api/audit", response_model=AnalysisResponse)
async def audit_document(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: str = Form("en"),
    filename: Optional[str] = Form(None),
):
    """Main audit endpoint: Ingests PDF/Image/Text, audits for predatory traps,

    translates briefing script, synthesizes Sarvam Bulbul audio, and caches in
    SQLite.
    """
    contract_text = ""
    resolved_filename = filename or "Contract_Document.txt"
    ingestion_method = "direct_text"

    if file and file.filename:
        resolved_filename = file.filename
        file_bytes = await file.read()
        contract_text, ingestion_method = await ingest_document(
            file_bytes=file_bytes,
            filename=file.filename,
            content_type=file.content_type or "",
        )
    elif text and text.strip():
        contract_text = text.strip()
        ingestion_method = "direct_text"
    else:
        # If nothing provided, use demo agreement
        contract_text = DEMO_RENTAL_AGREEMENT
        resolved_filename = "Bangalore_Rental_Agreement_Demo.pdf"
        ingestion_method = "demo_fallback"

    if not contract_text or len(contract_text.strip()) < 30:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Extracted document text is too brief or empty to perform legal forensic audit.",
            },
        )

    # 1. Compute SHA-256 fingerprint for caching
    doc_hash = compute_hash(contract_text, language)

    # 2. Check SQLite cache for instantaneous zero-latency response
    cached_record = get_cached_audit(doc_hash)
    if cached_record:
        return AnalysisResponse(
            success=True,
            cached=True,
            document_hash=doc_hash,
            filename=cached_record["filename"],
            report=cached_record["report"],
            spoken_language=language,
            audio_base64=cached_record["audio_base64"],
            translated_script=cached_record.get(
                "spoken_script", cached_record["report"].spoken_briefing_script
            ),
            is_demo=("demo" in resolved_filename.lower()),
            notes="Served instantaneously from local SQLite cache.",
        )

    # 3. Perform Forensic Legal Audit (Sarvam LLM or Intelligent Local Engine)
    # If it is the exact demo agreement and no key, use pre-computed demo report
    is_demo_text = (
        "Pinecrest Apartments" in contract_text
        and "Rs. 4,50,000" in contract_text
    )
    if is_demo_text and not SARVAM_API_KEY:
        report = DEMO_AUDIT_REPORT
    else:
        report = await audit_contract_with_sarvam(contract_text)

    # 4. Multilingual Translation for Audio Briefing
    translated_script = await translate_spoken_script(
        report.spoken_briefing_script, language
    )

    # 5. Multilingual Spoken Audio Briefing (Sarvam Bulbul TTS)
    audio_base64 = await synthesize_spoken_briefing(translated_script, language)

    # 6. Save in SQLite cache
    save_cached_audit(
        hash_key=doc_hash,
        filename=resolved_filename,
        language=language,
        report=report,
        audio_base64=audio_base64,
        spoken_script=translated_script,
    )

    return AnalysisResponse(
        success=True,
        cached=False,
        document_hash=doc_hash,
        filename=resolved_filename,
        report=report,
        spoken_language=language,
        audio_base64=audio_base64,
        translated_script=translated_script,
        is_demo=is_demo_text,
        notes=f"Audit completed successfully via {ingestion_method}.",
    )


@app.post("/api/demo/audit", response_model=AnalysisResponse)
async def audit_demo_agreement(language: str = "en"):
    """Instant endpoint to run the demo rental agreement in the chosen language."""
    return await audit_document(
        file=None,
        text=DEMO_RENTAL_AGREEMENT,
        language=language,
        filename="Bangalore_Rental_Agreement_Demo.pdf",
    )
