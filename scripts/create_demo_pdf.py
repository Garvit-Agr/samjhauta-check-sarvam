"""Generates a valid, multi-page digital PDF containing the predatory Bangalore rental agreement.
"""

from pathlib import Path


def generate_simple_pdf(text: str, output_path: str):
    """Generates a clean text PDF using standard PDF 1.4 spec."""
    lines = text.strip().split("\n")
    pages = []
    current_page = []
    
    for line in lines:
        current_page.append(line)
        if len(current_page) >= 38:
            pages.append(current_page)
            current_page = []
    if current_page:
        pages.append(current_page)

    # Build PDF object tree
    pdf_objects = []
    
    # 1: Catalog
    pdf_objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj")
    
    # Page object IDs
    page_ids = []
    content_ids = []
    obj_counter = 4
    for _ in pages:
        page_ids.append(obj_counter)
        content_ids.append(obj_counter + 1)
        obj_counter += 2

    # 2: Pages
    kids_str = " ".join([f"{pid} 0 R" for pid in page_ids])
    pdf_objects.append(f"2 0 obj\n<< /Type /Pages /Kids [{kids_str}] /Count {len(pages)} >>\nendobj")

    # 3: Font
    pdf_objects.append("3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj")

    for i, page_lines in enumerate(pages):
        pid = page_ids[i]
        cid = content_ids[i]

        # Content stream
        stream_lines = ["BT", "/F1 10 Tf", "14 TL", "40 760 Td"]
        for line in page_lines:
            # Escape parentheses and backslashes in PDF strings
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            # Truncate overly long lines to fit page width
            if len(escaped) > 85:
                escaped = escaped[:85] + "..."
            stream_lines.append(f"({escaped}) '")
        stream_lines.append("ET")
        stream_content = "\n".join(stream_lines)

        # Page Object
        pdf_objects.append(
            f"{pid} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> /Contents {cid} 0 R >>\nendobj"
        )
        # Content Stream Object
        pdf_objects.append(
            f"{cid} 0 obj\n<< /Length {len(stream_content)} >>\nstream\n{stream_content}\nendstream\nendobj"
        )

    # Assemble PDF with cross-reference table
    header = "%PDF-1.4\n"
    body = ""
    xref = ["xref", f"0 {len(pdf_objects) + 1}", "0000000000 65535 f "]
    offset = len(header)

    for obj in pdf_objects:
        xref.append(f"{offset:010d} 00000 n ")
        body += obj + "\n"
        offset = len(header) + len(body)

    xref_offset = offset
    xref_str = "\n".join(xref) + "\n"
    trailer = f"trailer\n<< /Size {len(pdf_objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF"

    full_pdf = header + body + xref_str + trailer
    Path(output_path).write_bytes(full_pdf.encode("latin-1"))


if __name__ == "__main__":
    from samjhautacheck.demo_data import DEMO_RENTAL_AGREEMENT
    out_file = "/Users/garvit/Desktop/Sarvam/static/Bangalore_Rental_Agreement_Demo.pdf"
    generate_simple_pdf(DEMO_RENTAL_AGREEMENT, out_file)
    print(f"✅ Generated sample digital PDF at: {out_file}")
