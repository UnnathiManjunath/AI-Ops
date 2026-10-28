import os

APP_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = "def export_database_json():"
idx = text.find(target)

new_route = """@app.route("/api/database/export-sql", methods=["GET"])
def export_database_sql():
    \"\"\"Download human-readable SQL Schema and Seed Script.\"\"\"
    sql_path = os.path.join(os.path.dirname(__file__), "MASTER_SRE_DATABASE.sql")
    if os.path.exists(sql_path):
        return send_file(sql_path, as_attachment=True, download_name="MASTER_SRE_DATABASE.sql")
    return jsonify({"error": "SQL file not found"}), 404

"""

if idx != -1:
    text = text[:idx] + new_route + text[idx:]
    with open(APP_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("export-sql route added to app.py!")
else:
    print("Target not found")
