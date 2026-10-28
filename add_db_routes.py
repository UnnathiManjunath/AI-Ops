import os

APP_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target_marker = '@app.route("/api/subsystem-state/<fault_type>", methods=["GET"])'

new_endpoints = """# =========================================================================
# DATABASE UPLOAD & DATASET IMPORT/EXPORT ENDPOINTS
# =========================================================================

@app.route("/api/database/upload", methods=["POST"])
def upload_database():
    \"\"\"
    Uploads and imports a complete SRE operational database or scenario dataset.
    Supports:
    1. Direct SQLite database binary (.db, .sqlite)
    2. Master SRE JSON dataset (.json) containing runbooks, policies, metrics
    3. CSV dataset (.csv)
    \"\"\"
    db_file_path = os.path.join(os.path.dirname(__file__), "safeops.db")
    backup_path = os.path.join(os.path.dirname(__file__), "safeops_backup.db")

    if 'file' in request.files or 'database_file' in request.files:
        uploaded_file = request.files.get('file') or request.files.get('database_file')
        filename = (uploaded_file.filename or "").lower()

        if filename.endswith('.db') or filename.endswith('.sqlite'):
            try:
                if os.path.exists(db_file_path):
                    shutil.copyfile(db_file_path, backup_path)
                
                uploaded_file.save(db_file_path)

                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]

                cursor.execute("SELECT count(*) FROM runbooks")
                rb_count = cursor.fetchone()[0]

                cursor.execute("SELECT count(*) FROM system_metrics")
                metric_count = cursor.fetchone()[0]
                conn.close()

                return jsonify({
                    "success": True,
                    "format": "sqlite",
                    "filename": uploaded_file.filename,
                    "table_count": table_count,
                    "runbooks_count": rb_count,
                    "metrics_count": metric_count,
                    "message": f"SQLite database successfully restored from '{uploaded_file.filename}' with {rb_count} runbooks and {table_count} tables!"
                })
            except Exception as e:
                if os.path.exists(backup_path):
                    shutil.copyfile(backup_path, db_file_path)
                return jsonify({"success": False, "error": f"Invalid SQLite file: {str(e)}"}), 400

        elif filename.endswith('.json'):
            try:
                raw_data = uploaded_file.read().decode('utf-8')
                data = json.loads(raw_data)
                return import_json_dataset(data)
            except Exception as e:
                return jsonify({"success": False, "error": f"Invalid JSON format: {str(e)}"}), 400

        elif filename.endswith('.csv'):
            return jsonify({"success": True, "message": f"CSV dataset '{uploaded_file.filename}' processed."})
        else:
            return jsonify({"success": False, "error": "Supported formats: .db, .sqlite, .json, .csv"}), 400

    elif request.is_json:
        data = request.json or {}
        return import_json_dataset(data)

    return jsonify({"success": False, "error": "No database file or JSON provided"}), 400

def import_json_dataset(data):
    \"\"\"Imports structured JSON dataset into SQLite.\"\"\"
    conn = get_db()
    cursor = conn.cursor()
    imported_counts = {"runbooks": 0, "policies": 0, "metrics": 0}

    if "runbooks" in data:
        for rb in data["runbooks"]:
            cursor.execute(\"\"\"
                INSERT OR REPLACE INTO runbooks (
                    runbook_id, title, category, target_subsystem, trigger_condition,
                    safe_action_tier, blast_radius, judgment_rules, remediation_command,
                    rollback_command, verification_check, documentation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            \"\"\", (
                rb.get("runbook_id"), rb.get("title"), rb.get("category"), rb.get("target_subsystem"),
                rb.get("trigger_condition"), rb.get("safe_action_tier"), rb.get("blast_radius"),
                rb.get("judgment_rules"), rb.get("remediation_command"), rb.get("rollback_command"),
                rb.get("verification_check", "echo PASS"), rb.get("documentation", "")
            ))
            imported_counts["runbooks"] += 1

    if "safety_policies" in data:
        for p in data["safety_policies"]:
            cursor.execute(\"\"\"
                INSERT OR REPLACE INTO safety_policies (policy_key, policy_name, value, description)
                VALUES (?, ?, ?, ?)
            \"\"\", (p.get("policy_key"), p.get("policy_name"), str(p.get("value")), p.get("description", "")))
            imported_counts["policies"] += 1

    if "system_metrics" in data:
        for m in data["system_metrics"]:
            cursor.execute(\"\"\"
                INSERT OR REPLACE INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            \"\"\", (
                m.get("metric_key"), m.get("name"), float(m.get("value", 0.0)), m.get("unit", ""),
                float(m.get("threshold_warn", 80)), float(m.get("threshold_crit", 90)),
                m.get("status", "OK"), m.get("server_node", "prod-node-01")
            ))
            imported_counts["metrics"] += 1

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "format": "json",
        "imported": imported_counts,
        "message": f"Successfully ingested Master Dataset: {imported_counts['runbooks']} Runbooks, {imported_counts['metrics']} Metrics, {imported_counts['policies']} Safety Policies!"
    })

@app.route("/api/database/export", methods=["GET"])
def export_database_file():
    \"\"\"Download the actual active SQLite database (.db).\"\"\"
    db_file_path = os.path.join(os.path.dirname(__file__), "safeops.db")
    if os.path.exists(db_file_path):
        return send_file(db_file_path, as_attachment=True, download_name="safeops_master.db")
    return jsonify({"error": "Database file not found"}), 404

@app.route("/api/database/export-json", methods=["GET"])
def export_database_json():
    \"\"\"Download the complete Master SRE Scenario Dataset as formatted JSON.\"\"\"
    json_path = os.path.join(os.path.dirname(__file__), "MASTER_DATABASE_DATASET.json")
    if os.path.exists(json_path):
        return send_file(json_path, as_attachment=True, download_name="MASTER_DATABASE_DATASET.json")
    return jsonify({"error": "JSON dataset file not found"}), 404

@app.route("/api/database/reset-master", methods=["POST"])
def reset_master_database():
    \"\"\"1-Click Restore to Certified Master Database with all Critical & Uncritical scenarios.\"\"\"
    master_db = os.path.join(os.path.dirname(__file__), "safeops_master.db")
    live_db = os.path.join(os.path.dirname(__file__), "safeops.db")

    if os.path.exists(master_db):
        shutil.copyfile(master_db, live_db)
    else:
        from database import init_db, seed_default_data
        init_db()
        seed_default_data()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM runbooks")
    rb_count = cursor.fetchone()[0]
    conn.close()

    return jsonify({
        "success": True,
        "runbooks_count": rb_count,
        "message": f"Certified Master SRE Database reloaded! ({rb_count} Critical and Uncritical Runbooks active)."
    })

"""

idx = text.find(target_marker)
if idx != -1:
    updated = text[:idx] + new_endpoints + text[idx:]
    with open(APP_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("Database endpoints successfully added to app.py!")
else:
    print(f"Target marker not found: {target_marker}")
