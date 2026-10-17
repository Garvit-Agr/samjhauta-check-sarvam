import asyncio
import os
from samjhautacheck.config import SARVAM_API_KEY
from samjhautacheck.db import init_db, compute_hash, get_cached_audit, save_cached_audit
from samjhautacheck.demo_data import DEMO_RENTAL_AGREEMENT, DEMO_AUDIT_REPORT
from samjhautacheck.ingestion import extract_text_from_pdf_pypdf, ingest_document
from samjhautacheck.sarvam_client import (
    fallback_forensic_audit,
    audit_contract_with_sarvam,
    translate_spoken_script,
    synthesize_spoken_briefing,
)


def test_database_and_caching():
    init_db()
    test_text = "Clause: Landlord shall forfeit deposit unconditionally upon early exit."
    test_lang = "hi"
    
    hash_key = compute_hash(test_text, test_lang)
    assert len(hash_key) == 64, "SHA-256 hash must be 64 characters long"

    # Save to SQLite
    save_cached_audit(
        hash_key=hash_key,
        filename="test_rental.txt",
        language=test_lang,
        report=DEMO_AUDIT_REPORT,
        audio_base64="fake_base64_audio_payload",
        spoken_script="Dhyan se suno bhai...",
    )

    # Retrieve from SQLite
    cached = get_cached_audit(hash_key)
    assert cached is not None, "Failed to retrieve saved cached record"
    assert cached["report"].fairness_score == DEMO_AUDIT_REPORT.fairness_score
    assert cached["audio_base64"] == "fake_base64_audio_payload"
    assert cached["language"] == test_lang
    print("✅ test_database_and_caching passed!")


def test_forensic_audit():
    report = fallback_forensic_audit(DEMO_RENTAL_AGREEMENT)
    assert report.fairness_score <= 40, f"Expected low fairness score for predatory contract, got {report.fairness_score}"
    assert len(report.red_flags) >= 4, f"Expected at least 4 red flags, got {len(report.red_flags)}"
    assert len(report.missing_protections) >= 3, "Expected at least 3 missing protections"
    assert len(report.whatsapp_negotiation_draft) > 50, "WhatsApp negotiation draft must be populated"
    assert len(report.spoken_briefing_script) > 30, "Spoken briefing script must be populated"
    print(f"✅ test_forensic_audit passed! Fairness Score: {report.fairness_score}/100, Traps detected: {len(report.red_flags)}")


async def test_multilingual_pipeline():
    # Translation
    hi_script = await translate_spoken_script(DEMO_AUDIT_REPORT.spoken_briefing_script, "hi")
    assert len(hi_script) > 20, "Hindi script must be populated"

    hinglish_script = await translate_spoken_script(DEMO_AUDIT_REPORT.spoken_briefing_script, "hinglish")
    assert len(hinglish_script) > 20, "Hinglish script must be populated"

    te_script = await translate_spoken_script(DEMO_AUDIT_REPORT.spoken_briefing_script, "te")
    assert len(te_script) > 20, "Telugu script must be populated"

    ta_script = await translate_spoken_script(DEMO_AUDIT_REPORT.spoken_briefing_script, "ta")
    assert len(ta_script) > 20, "Tamil script must be populated"
    
    print("✅ test_multilingual_pipeline passed!")


async def test_ingestion():
    raw_bytes = DEMO_RENTAL_AGREEMENT.encode("utf-8")
    text, method = await ingest_document(raw_bytes, "demo.txt", "text/plain")
    assert "Pinecrest Apartments" in text
    assert method == "plain_text"
    print("✅ test_ingestion passed!")


def main():
    test_database_and_caching()
    test_forensic_audit()
    asyncio.run(test_multilingual_pipeline())
    asyncio.run(test_ingestion())
    print("\n🎉 ALL PIPELINE TESTS PASSED WITH 0 FAILURES!")


if __name__ == "__main__":
    main()
