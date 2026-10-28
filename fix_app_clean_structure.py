import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
APP_PATH = os.path.join(PROJECT_DIR, "app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove if __name__ == "__main__": and everything below it
idx_main = code.find('if __name__ == "__main__":')
if idx_main != -1:
    code = code[:idx_main].strip()

# 2. Add BASE_DIR, os.chdir, get_active_preset, set_active_preset, and find_dataset_file at the top
top_block = '''BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def get_active_preset():
    """Returns the currently active industry dataset preset (it_sector, ecommerce, healthcare, fintech)."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM safety_policies WHERE policy_key = 'active_preset'")
        row = cursor.fetchone()
        conn.close()
        if row and row['value']:
            return row['value'].strip().lower()
    except Exception:
        pass
    return "it_sector"

def set_active_preset(preset_name):
    """Persists the active industry preset into SQLite."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO safety_policies (policy_key, policy_name, value, description)
        VALUES ('active_preset', 'Active Operational Preset', ?, 'Currently active industry scenario dataset')
    """, (preset_name,))
    conn.commit()
    conn.close()

def find_dataset_file(filename):
    """Finds a dataset file whether in base dir, datasets subdir, or cwd."""
    candidates = [
        os.path.join(BASE_DIR, "datasets", filename),
        os.path.join(BASE_DIR, filename),
        os.path.join(os.getcwd(), "datasets", filename),
        os.path.join(os.getcwd(), filename),
        filename
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.isfile(c):
            return os.path.abspath(c)
    return None
'''

# Insert right after `app = Flask(__name__) ... seed_default_data()`
seed_marker = "seed_default_data()"
idx_seed = code.find(seed_marker)
if idx_seed != -1:
    idx_insert = idx_seed + len(seed_marker)
    code = code[:idx_insert] + "\n\n" + top_block + "\n" + code[idx_insert:]

# 3. Update download_preset_db to use find_dataset_file and proper mimetype
old_db_func = '''@app.route("/api/database/download-preset-db/<preset_name>", methods=["GET"])
def download_preset_db(preset_name):
    """Download the SQLite binary for a chosen preset."""
    preset_name = preset_name.lower().strip()
    files = {
        "it_sector": ("safeops_it_sector.db", "DevOpsCorp_ITSector.db"),
        "ecommerce": ("safeops_ecommerce.db", "QuickCart_ECommerce.db"),
        "healthcare": ("safeops_healthcare.db", "LifeCare_Healthcare.db"),
        "fintech": ("safeops_master.db", "GlobalPay_Fintech.db")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = os.path.join(os.path.dirname(__file__), src)
        if os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name)
    return jsonify({"error": "Preset DB file not found"}), 404'''

new_db_func = '''@app.route("/api/database/download-preset-db/<preset_name>", methods=["GET"])
def download_preset_db(preset_name):
    """Download the SQLite binary for a chosen preset."""
    preset_name = preset_name.lower().strip()
    files = {
        "it_sector": ("safeops_it_sector.db", "DevOpsCorp_ITSector.db"),
        "it": ("safeops_it_sector.db", "DevOpsCorp_ITSector.db"),
        "ecommerce": ("safeops_ecommerce.db", "QuickCart_ECommerce.db"),
        "healthcare": ("safeops_healthcare.db", "LifeCare_Healthcare.db"),
        "fintech": ("safeops_master.db", "GlobalPay_Fintech.db")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = find_dataset_file(src)
        if p and os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name, mimetype="application/x-sqlite3")
    return jsonify({"error": f"Preset DB file '{preset_name}' not found on server."}), 404'''

if old_db_func in code:
    code = code.replace(old_db_func, new_db_func)
else:
    # Try regex or substring replacement
    idx_db = code.find('def download_preset_db')
    idx_sub = code.find('@app.route("/api/subsystem-state', idx_db)
    if idx_db != -1 and idx_sub != -1:
        route_header = '@app.route("/api/database/download-preset-db/<preset_name>", methods=["GET"])\n'
        code = code[:code.rfind('@app.route', 0, idx_db)] + new_db_func + "\n\n" + code[idx_sub:]

# 4. Update download_preset_json to use find_dataset_file
new_json_func = '''@app.route("/api/database/download-preset/<preset_name>", methods=["GET"])
def download_preset_json(preset_name):
    """Download the JSON dataset for a chosen preset."""
    preset_name = preset_name.lower().strip()
    files = {
        "it_sector": ("DATASET_IT_SECTOR_DEVOPS.json", "DevOpsCorp_ITSector_Dataset.json"),
        "it": ("DATASET_IT_SECTOR_DEVOPS.json", "DevOpsCorp_ITSector_Dataset.json"),
        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.json", "QuickCart_ECommerce_Dataset.json"),
        "healthcare": ("DATASET_HEALTHCARE_LIFECARE.json", "LifeCare_Healthcare_Dataset.json"),
        "fintech": ("MASTER_DATABASE_DATASET.json", "GlobalPay_Fintech_Dataset.json")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = find_dataset_file(src)
        if p and os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name, mimetype="application/json")
    return jsonify({"error": f"Preset JSON file '{preset_name}' not found on server."}), 404'''

idx_json = code.find('def download_preset_json')
idx_sql = code.find('@app.route("/api/database/download-preset-sql', idx_json)
if idx_json != -1 and idx_sql != -1:
    code = code[:code.rfind('@app.route', 0, idx_json)] + new_json_func + "\n\n" + code[idx_sql:]

# 5. Update download_preset_sql to use find_dataset_file
new_sql_func = '''@app.route("/api/database/download-preset-sql/<preset_name>", methods=["GET"])
def download_preset_sql(preset_name):
    """Download the SQL Schema & Seeds for a chosen preset."""
    preset_name = preset_name.lower().strip()
    files = {
        "it_sector": ("DATASET_IT_SECTOR_DEVOPS.sql", "DevOpsCorp_ITSector_Schema.sql"),
        "it": ("DATASET_IT_SECTOR_DEVOPS.sql", "DevOpsCorp_ITSector_Schema.sql"),
        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.sql", "QuickCart_ECommerce_Schema.sql"),
        "healthcare": ("DATASET_HEALTHCARE_LIFECARE.sql", "LifeCare_Healthcare_Schema.sql"),
        "fintech": ("MASTER_SRE_DATABASE.sql", "GlobalPay_Fintech_Schema.sql")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = find_dataset_file(src)
        if p and os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name, mimetype="application/sql")
    return jsonify({"error": f"Preset SQL file '{preset_name}' not found on server."}), 404'''

idx_sql_def = code.find('def download_preset_sql')
idx_db_def = code.find('@app.route("/api/database/download-preset-db', idx_sql_def)
if idx_sql_def != -1 and idx_db_def != -1:
    code = code[:code.rfind('@app.route', 0, idx_sql_def)] + new_sql_func + "\n\n" + code[idx_db_def:]

# 6. Append if __name__ == "__main__": at the absolute end of file
code += '\n\nif __name__ == "__main__":\n    app.run(host="0.0.0.0", port=8080, debug=False)\n'

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Cleanly reconstructed app.py with all helpers at top and app.run at bottom!")
