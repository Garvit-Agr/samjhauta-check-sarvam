import hashlib
import json
import sqlite3
from typing import Any, Dict, Optional
from samjhautacheck.config import DB_PATH
from samjhautacheck.models import AuditReport


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize SQLite database with contract_audits table and indexes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contract_audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash_key TEXT UNIQUE NOT NULL,
            filename TEXT NOT NULL,
            language TEXT NOT NULL,
            document_type TEXT NOT NULL,
            fairness_score INTEGER NOT NULL,
            audit_json TEXT NOT NULL,
            audio_base64 TEXT,
            spoken_script TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_hash_key ON contract_audits(hash_key)"
    )
    conn.commit()
    conn.close()


def compute_hash(text_content: str, language: str = "en") -> str:
    """Computes a SHA-256 fingerprint from document text and target language."""
    normalized = " ".join(text_content.strip().split())
    to_hash = f"{normalized}__lang_{language.lower()}".encode("utf-8")
    return hashlib.sha256(to_hash).hexdigest()


def get_cached_audit(hash_key: str) -> Optional[Dict[str, Any]]:
    """Retrieves cached forensic audit and synthesized audio if previously analyzed."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT hash_key, filename, language, document_type, fairness_score, 
               audit_json, audio_base64, spoken_script, created_at
        FROM contract_audits
        WHERE hash_key = ?
        """,
        (hash_key,),
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    try:
        report_data = json.loads(row["audit_json"])
        report = AuditReport(**report_data)
        return {
            "hash_key": row["hash_key"],
            "filename": row["filename"],
            "language": row["language"],
            "report": report,
            "audio_base64": row["audio_base64"],
            "spoken_script": row["spoken_script"],
            "created_at": row["created_at"],
        }
    except Exception:
        return None


def save_cached_audit(
    hash_key: str,
    filename: str,
    language: str,
    report: AuditReport,
    audio_base64: Optional[str] = None,
    spoken_script: Optional[str] = None,
) -> None:
    """Saves audit results and audio payload in SQLite database for instant retrieval."""
    conn = get_db_connection()
    cursor = conn.cursor()
    audit_json = report.model_dump_json()

    cursor.execute(
        """
        INSERT INTO contract_audits 
            (hash_key, filename, language, document_type, fairness_score, audit_json, audio_base64, spoken_script)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(hash_key) DO UPDATE SET
            filename = excluded.filename,
            document_type = excluded.document_type,
            fairness_score = excluded.fairness_score,
            audit_json = excluded.audit_json,
            audio_base64 = excluded.audio_base64,
            spoken_script = excluded.spoken_script
        """,
        (
            hash_key,
            filename,
            language,
            report.document_type,
            report.fairness_score,
            audit_json,
            audio_base64,
            spoken_script or report.spoken_briefing_script,
        ),
    )
    conn.commit()
    conn.close()
