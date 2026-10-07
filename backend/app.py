import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone
from flask import Flask, jsonify, request
from database import get_connection, init_db
from ai.predictor import predict_category
from priority import compute_priority

app = Flask(__name__, static_folder="../frontend", static_url_path="")
init_db()


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "SmartDesk local API"})


@app.get("/api/tickets")
def list_tickets():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tickets ORDER BY CASE priority WHEN 'urgent' THEN 0 ELSE 1 END, id DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/tickets")
def create_ticket():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400
    subject = data.get("subject")
    description = data.get("description")
    if not isinstance(subject, str):
        return jsonify({"error": "Subject must be a string"}), 400
    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400
    subject = subject.strip()
    description = description.strip()
    if not subject or len(subject) > 100:
        return jsonify({"error": "Subject is required (max 100 characters)"}), 400
    if not description or len(description) > 500:
        return jsonify({"error": "Description is required (max 500 characters)"}), 400
    prediction = predict_category(subject + ". " + description)
    priority = compute_priority(subject, description)
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
                priority,
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
                "priority": priority,
                "created_at": created_at,
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
