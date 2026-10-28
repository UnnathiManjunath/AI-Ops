import re

app_path = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    text = f.read()

new_routes = """@app.route("/api/filesystem/compress-selected", methods=["POST"])
def api_filesystem_compress_selected():
    \"\"\"Compresses ONLY the user-selected files on local hard drive, enforcing SRE safety rules.\"\"\"
    data = request.json or {}
    file_list = data.get("files", [])
    if not file_list:
        return jsonify({"success": False, "error": "No files selected for compression."}), 400

    res = real_filesystem_engine.compress_selected_files(file_list)
    if res.get("reclaimed_bytes", 0) > 0:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE system_metrics SET value = 62.4, status = 'OK' WHERE metric_key = 'disk_usage_pct'")
        conn.commit()
        conn.close()
    return jsonify(res)

@app.route("/api/filesystem/rollback-selected", methods=["POST"])
def api_filesystem_rollback_selected():
    \"\"\"Restores selected or all archive files back to raw logs on disk.\"\"\"
    data = request.json or {}
    archive_list = data.get("archives", None)
    res = real_filesystem_engine.rollback_selected_files(archive_list)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE system_metrics SET value = 94.2, status = 'CRITICAL' WHERE metric_key = 'disk_usage_pct'")
    conn.commit()
    conn.close()
    return jsonify(res)
"""

target = "@app.route(\"/api/filesystem/execute-rollback\", methods=[\"POST\"])\ndef api_filesystem_execute_rollback():\n    \"\"\"Gunzips files back to raw UTF-8 logs on local hard drive.\"\"\"\n    res = real_filesystem_engine.execute_real_rollback()\n    conn = get_db()\n    cursor = conn.cursor()\n    cursor.execute(\"UPDATE system_metrics SET value = 94.2, status = 'CRITICAL' WHERE metric_key = 'disk_usage_pct'\")\n    conn.commit()\n    conn.close()\n    return jsonify(res)"

if target in text:
    text = text.replace(target, target + "\n\n" + new_routes, 1)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully added selective compression routes to app.py!")
else:
    print("Target not found; trying regex...")
    rgx = r'(@app\.route\("/api/filesystem/execute-rollback", methods=\["POST"\]\)[\s\S]*?return jsonify\(res\)\n)'
    m = re.search(rgx, text)
    if m:
        text = text[:m.end()] + "\n" + new_routes + "\n" + text[m.end():]
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully added via regex to app.py!")
    else:
        print("Could not match regex!")
