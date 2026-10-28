import os

APP_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

bad_block = """@app.route("/api/database/export-json", methods=["GET"])
@app.route("/api/database/export-sql", methods=["GET"])
def export_database_sql():
    \"\"\"Download human-readable SQL Schema and Seed Script.\"\"\"
    sql_path = os.path.join(os.path.dirname(__file__), "MASTER_SRE_DATABASE.sql")
    if os.path.exists(sql_path):
        return send_file(sql_path, as_attachment=True, download_name="MASTER_SRE_DATABASE.sql")
    return jsonify({"error": "SQL file not found"}), 404

def export_database_json():"""

good_block = """@app.route("/api/database/export-sql", methods=["GET"])
def export_database_sql():
    \"\"\"Download human-readable SQL Schema and Seed Script.\"\"\"
    sql_path = os.path.join(os.path.dirname(__file__), "MASTER_SRE_DATABASE.sql")
    if os.path.exists(sql_path):
        return send_file(sql_path, as_attachment=True, download_name="MASTER_SRE_DATABASE.sql")
    return jsonify({"error": "SQL file not found"}), 404

@app.route("/api/database/export-json", methods=["GET"])
def export_database_json():"""

if bad_block in text:
    text = text.replace(bad_block, good_block)
    with open(APP_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed decorator mapping!")
else:
    print("Bad block not found directly, checking normalized...")
    # Normalize \r\n
    text_norm = text.replace("\r\n", "\n")
    if bad_block in text_norm:
        text_norm = text_norm.replace(bad_block, good_block)
        with open(APP_PATH, "w", encoding="utf-8") as f:
            f.write(text_norm)
        print("Fixed decorator mapping with normalized line endings!")
    else:
        print("Could not match block")
