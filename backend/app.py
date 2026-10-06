# Placeholder. Group A1 builds the Flask server in tasks A1-1.1 and A1-2.2.

from flask import Flask, jsonify
from database import get_connection, init_db

app = Flask(__name__, static_folder="../frontend", static_url_path="")

init_db()


@app.route("/")
def serve_index():
    return app.send_static_file("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "SmartDesk local API"})


if __name__ == "__main__":
    app.run(debug=True)
