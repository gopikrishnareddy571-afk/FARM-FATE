
from flask import Flask, render_template, request, jsonify, session
import sqlite3, os
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)
app.secret_key = "farm_fate_secret"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def db():
    return sqlite3.connect("farm.db")

# ---------- DATABASE ----------
with db() as con:
    con.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT UNIQUE
    )""")
    con.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        user_id INTEGER,
        aadhaar TEXT,
        kisan TEXT,
        state TEXT,
        district TEXT,
        village TEXT,
        aadhaar_img TEXT,
        kisan_img TEXT
    )""")


@app.route("/")
def home():
    return render_template("index.html")

# ---------- LOGIN ----------
@app.route("/api/login", methods=["POST"])
def login():
    phone = request.json["phone"]
    with db() as con:
        user = con.execute("SELECT id FROM users WHERE phone=?", (phone,)).fetchone()
        if not user:
            con.execute("INSERT INTO users(phone) VALUES(?)", (phone,))
            user = con.execute("SELECT id FROM users WHERE phone=?", (phone,)).fetchone()
    session["user_id"] = user[0]
    return jsonify({"status": "logged_in"})

@app.route("/api/logout")
def logout():
    session.clear()
    return jsonify({"status": "logged_out"})

# ---------- PROFILE ----------
@app.route("/api/save-profile", methods=["POST"])
def save_profile():
    if "user_id" not in session:
        return jsonify({"error": "unauthorized"})

    data = request.form
    aadhaar_img = request.files.get("aadhaar_img")
    kisan_img = request.files.get("kisan_img")

    aadhaar_path = secure_filename(aadhaar_img.filename) if aadhaar_img else ""
    kisan_path = secure_filename(kisan_img.filename) if kisan_img else ""

    if aadhaar_img: aadhaar_img.save(os.path.join(UPLOAD_FOLDER, aadhaar_path))
    if kisan_img: kisan_img.save(os.path.join(UPLOAD_FOLDER, kisan_path))

    with db() as con:
        con.execute("DELETE FROM profile WHERE user_id=?", (session["user_id"],))
        con.execute("""
        INSERT INTO profile VALUES (?,?,?,?,?,?,?,?)
        """, (session["user_id"], data["aadhaar"], data["kisan"],
              data["state"], data["district"], data["village"],
              aadhaar_path, kisan_path))
    return jsonify({"status": "saved"})

@app.route("/api/load-profile")
def load_profile():
    if "user_id" not in session:
        return jsonify({})
    p = db().execute("""
    SELECT aadhaar,kisan,state,district,village
    FROM profile WHERE user_id=?
    """, (session["user_id"],)).fetchone()
    if not p: return jsonify({})
    return jsonify({
        "aadhaar": p[0],
        "kisan": p[1],
        "state": p[2],
        "district": p[3],
        "village": p[4]
    })
@app.route("/market-price/<crop>")
def market_price(crop):

    API_KEY = "PASTE_YOUR_API_KEY_HERE"
    RESOURCE_ID = "PASTE_YOUR_RESOURCE_ID_HERE"

    url = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=json&filters[commodity]={crop}"

    try:
        response = requests.get(url)
        data = response.json()

        if "records" in data and data["records"]:
            price = data["records"][0].get("modal_price", "Not Available")
            return jsonify({"price": price})
        else:
            return jsonify({"price": "Not Found"})

    except:
        return jsonify({"price": "Error"})

if __name__ == "__main__":
    app.run(debug=True)
