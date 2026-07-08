#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import socket
import sqlite3
import sys
from datetime import date
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_from_directory

if getattr(sys, 'frozen', False):
    BUNDLE_DIR = Path(sys._MEIPASS)
    BASE_DIR   = Path(sys.executable).parent.resolve()
    app = Flask(__name__, template_folder=str(BUNDLE_DIR / "templates"), static_folder="static")
else:
    BASE_DIR   = Path(__file__).parent.parent.resolve()
    app = Flask(__name__, template_folder="templates", static_folder="static")

VOCAB_JSON = BASE_DIR / "vocab.json"
DB_PATH    = BASE_DIR / "progress.db"
PORT       = 5100


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                key             TEXT PRIMARY KEY,
                fav             INTEGER DEFAULT 0,
                known           INTEGER DEFAULT 0,
                introduced_date TEXT
            )
        """)
        try:
            conn.execute("ALTER TABLE progress ADD COLUMN introduced_date TEXT")
        except sqlite3.OperationalError:
            pass  # column already exists



def load_vocab(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cards = data.get("cards", [])
    for c in cards:
        c.setdefault("fav", False)
        c.setdefault("known", False)
    return cards


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/api/fav", methods=["POST"])
def fav_card():
    data = request.json
    key  = data.get("key", "")
    if not key:
        return jsonify({"ok": False, "error": "missing key"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO progress(key,fav,known) VALUES(?,?,0) "
            "ON CONFLICT(key) DO UPDATE SET fav=excluded.fav",
            (key, 1 if data.get("fav") else 0)
        )
    return jsonify({"ok": True})


@app.route("/api/known", methods=["POST"])
def known_card():
    data = request.json
    key  = data.get("key", "")
    if not key:
        return jsonify({"ok": False, "error": "missing key"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO progress(key,fav,known) VALUES(?,0,?) "
            "ON CONFLICT(key) DO UPDATE SET known=excluded.known",
            (key, 1 if data.get("known") else 0)
        )
    return jsonify({"ok": True})


@app.route("/api/start-day", methods=["POST"])
def start_day():
    n         = int(request.json.get("new", 10))
    all_cards = load_vocab(VOCAB_JSON)

    today = date.today().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT key, fav, known, introduced_date FROM progress"
        ).fetchall()
        prog = {
            r[0]: {"fav": bool(r[1]), "known": bool(r[2]), "date": r[3]}
            for r in rows
        }

    # Đếm đã introduce hôm nay — chỉ tính vocab keys, không tính cluster keys
    vocab_keys    = {c["key"] for c in all_cards}
    today_n       = sum(1 for k, p in prog.items() if k in vocab_keys and p.get("date") == today)
    remaining_new = max(0, n - today_n)

    session, review_n, new_n = [], 0, 0
    for c in all_cards:
        p = prog.get(c["key"], {})
        d = p.get("date")
        if d is not None:
            c["fav"]    = p["fav"]
            c["known"]  = p["known"]
            c["is_new"] = False
            session.append(c)
            if d != today:
                review_n += 1
        elif new_n < remaining_new:
            c["fav"]    = p.get("fav", False)
            c["known"]  = p.get("known", False)
            c["is_new"] = True
            session.append(c)
            new_n += 1

    return jsonify({"cards": session, "review": review_n,
                    "today_introduced": today_n, "new": new_n})


@app.route("/api/introduce", methods=["POST"])
def introduce():
    key   = request.json.get("key", "")
    today = date.today().isoformat()
    if not key:
        return jsonify({"ok": False}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO progress(key,fav,known,introduced_date) VALUES(?,0,0,?) "
            "ON CONFLICT(key) DO UPDATE SET "
            "introduced_date=COALESCE(introduced_date, excluded.introduced_date)",
            (key, today)
        )
    return jsonify({"ok": True})


@app.route("/api/history")
def history():
    if not DB_PATH.exists():
        return jsonify([])
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT key, introduced_date FROM progress "
            "WHERE introduced_date IS NOT NULL ORDER BY introduced_date DESC"
        ).fetchall()
    card_map = {c["key"]: c["term"] for c in load_vocab(VOCAB_JSON)}
    grouped  = {}
    for key, d in rows:
        if key not in card_map:
            continue  # skip cluster entries (syn_*, casual_*, etc.)
        grouped.setdefault(d, []).append(card_map[key])
    return jsonify([
        {"date": d, "words": words}
        for d, words in sorted(grouped.items(), reverse=True)
    ])


@app.route("/api/reset", methods=["POST"])
def reset_progress():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM progress")
    return jsonify({"ok": True})


@app.route("/api/clusters")
def get_clusters():
    clusters_path = BASE_DIR / "clusters.json"
    if not clusters_path.exists():
        return jsonify({"clusters": []})
    with open(clusters_path, encoding="utf-8") as f:
        data = json.load(f)
    clusters = data.get("clusters", [])

    if not DB_PATH.exists() or not clusters:
        return jsonify({"clusters": clusters})

    cluster_ids = [c["id"] for c in clusters]
    placeholders = ",".join("?" * len(cluster_ids))
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            f"SELECT key, fav, known, introduced_date FROM progress WHERE key IN ({placeholders})",
            cluster_ids
        ).fetchall()
    prog = {r[0]: {"fav": bool(r[1]), "known": bool(r[2]), "date": r[3]} for r in rows}

    for c in clusters:
        p = prog.get(c["id"], {})
        c["fav"] = p.get("fav", False)
        c["known"] = p.get("known", False)
        c["introduced_date"] = p.get("date")

    return jsonify({"clusters": clusters})


@app.route("/api/sync", methods=["POST", "OPTIONS"])
def sync_progress():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})
    client_prog = request.json.get("progress", {}) if request.json else {}
    with sqlite3.connect(DB_PATH) as conn:
        for key, val in client_prog.items():
            fav   = 1 if val.get("fav") else 0
            known = 1 if val.get("known") else 0
            dt    = val.get("date") if (val.get("date") and str(val.get("date")).strip()) else None
            conn.execute(
                "INSERT INTO progress(key,fav,known,introduced_date) VALUES(?,?,?,?) "
                "ON CONFLICT(key) DO UPDATE SET "
                "fav=max(fav, excluded.fav), "
                "known=max(known, excluded.known), "
                "introduced_date=COALESCE(introduced_date, excluded.introduced_date)",
                (key, fav, known, dt)
            )
        rows = conn.execute("SELECT key, fav, known, introduced_date FROM progress").fetchall()
        server_prog = {
            r[0]: {"fav": bool(r[1]), "known": bool(r[2]), "date": r[3]}
            for r in rows
        }
    return jsonify({"ok": True, "progress": server_prog})


@app.route("/mobile/<path:filename>")
def serve_mobile(filename):
    return send_from_directory(str(BASE_DIR / "mobile"), filename)


@app.route("/mobile/")
@app.route("/mobile")
def serve_mobile_index():
    return send_from_directory(str(BASE_DIR / "mobile"), "index.html")


def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    init_db()
    ip = local_ip()
    print()
    print("╔══════════════════════════════════════════╗")
    print("║       📚  Vocab Practice — Server        ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║  PC nay   : http://localhost:{PORT}          ║")
    print(f"║  Thiet bi : http://{ip}:{PORT}       ║")
    print("║  Nhan Ctrl+C de dung                     ║")
    print("╚══════════════════════════════════════════╝")
    print()

    from waitress import serve
    serve(app, host="0.0.0.0", port=PORT, threads=4)

