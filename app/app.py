import os

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "appdb"),
        user=os.environ.get("DB_USER", "appuser"),
        password=os.environ.get("DB_PASSWORD", ""),
        connect_timeout=3,
    )


@app.route("/")
def home():
    return jsonify(message="Flask app is running")


@app.route("/health")
def health():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return jsonify(status="ok", database="connected")
    except Exception:
        app.logger.exception("Database health check failed")
        return jsonify(status="error", database="unavailable"), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
