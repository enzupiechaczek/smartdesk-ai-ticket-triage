import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone
from flask import Flask, jsonify, request
from database import get_connection, init_db
from ai.predictor import predict_category

app = Flask(__name__)
init_db()


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "SmartDesk local API"})


@app.get("/api/tickets")
def list_tickets():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/tickets")
def create_ticket():
    data = request.get_json(silent=True) or {}
    subject = str(data.get("subject", "")).strip()
    description = str(data.get("description", "")).strip()
    if not subject or len(subject) > 100:
        return jsonify({"error": "Subject is required (max 100 characters)"}), 400
    if not description or len(description) > 500:
        return jsonify({"error": "Description is required (max 500 characters)"}), 400
    prediction = predict_category(subject + ". " + description)
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO tickets (subject, description, category, confidence, priority, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                subject,
                description,
                prediction["category"],
                prediction["confidence"],
                "normal",
                created_at,
            ),
        )
        ticket_id = cur.lastrowid
    return (
        jsonify(
            {
                "id": ticket_id,
                "subject": subject,
                "description": description,
                "category": prediction["category"],
                "confidence": prediction["confidence"],
                "priority": "normal",
                "created_at": created_at,
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
