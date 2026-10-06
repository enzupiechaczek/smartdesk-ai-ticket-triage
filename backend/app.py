# Placeholder. Group A1 builds the Flask server in tasks A1-1.1 and A1-2.2.
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "SmartDesk local API"})

if __name__ == "__main__":
    app.run(debug=True)