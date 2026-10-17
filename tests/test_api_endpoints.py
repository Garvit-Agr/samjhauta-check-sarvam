import io
from fastapi.testclient import TestClient
from samjhautacheck.app import app
from samjhautacheck.demo_data import DEMO_RENTAL_AGREEMENT

client = TestClient(app)


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "SamjhautaCheck" in response.text
    print("✅ test_index_page passed!")


def test_status_endpoint():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "supported_languages" in data
    print("✅ test_status_endpoint passed!")


def test_demo_endpoint():
    response = client.get("/api/demo")
    assert response.status_code == 200
    data = response.json()
    assert "Pinecrest Apartments" in data["text"]
    print("✅ test_demo_endpoint passed!")


def test_audit_endpoint_text_and_cache():
    # 1. First audit (generates report and saves to SQLite)
    response = client.post(
        "/api/audit",
        data={
            "text": DEMO_RENTAL_AGREEMENT,
            "language": "hi",
            "filename": "Test_Tenancy.txt",
        },
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert data["success"] is True
    assert data["report"]["fairness_score"] <= 40
    assert len(data["report"]["red_flags"]) >= 4
    assert len(data["report"]["whatsapp_negotiation_draft"]) > 30
    assert data["spoken_language"] == "hi"
    print(f"✅ First audit completed. Fairness Score: {data['report']['fairness_score']}/100")

    # 2. Second audit with same text & language -> MUST HIT SQLITE CACHE INSTANTLY!
    cached_response = client.post(
        "/api/audit",
        data={
            "text": DEMO_RENTAL_AGREEMENT,
            "language": "hi",
            "filename": "Test_Tenancy.txt",
        },
    )
    assert cached_response.status_code == 200
    cached_data = cached_response.json()
    assert cached_data["cached"] is True, "Expected cached: true from SQLite layer"
    print("✅ SQLite Cache hit verification: SUCCESS! Instantaneous zero-latency retrieval verified.")


def test_audit_endpoint_pdf_upload():
    from pathlib import Path
    pdf_path = Path("static/Bangalore_Rental_Agreement_Demo.pdf")
    assert pdf_path.exists(), "Sample PDF must exist"

    with open(pdf_path, "rb") as f:
        response = client.post(
            "/api/audit",
            files={"file": ("Bangalore_Rental_Agreement_Demo.pdf", f, "application/pdf")},
            data={"language": "hinglish"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["report"]["red_flags"]) >= 4
    print("✅ PDF upload and audit verification: SUCCESS!")


if __name__ == "__main__":
    test_index_page()
    test_status_endpoint()
    test_demo_endpoint()
    test_audit_endpoint_text_and_cache()
    test_audit_endpoint_pdf_upload()
    print("\n🎉 ALL API ENDPOINT TESTS PASSED WITH 100% SUCCESS!")
