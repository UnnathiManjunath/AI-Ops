import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
APP_PATH = os.path.join(PROJECT_DIR, "app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    code = f.read()

csv_routes = '''
@app.route("/api/database/download-preset-csv/<preset_name>", methods=["GET"])
def download_preset_csv(preset_name):
    """Download tabular CSV dataset (rows and columns) for Excel / Google Sheets."""
    preset_name = preset_name.lower().strip()
    files = {
        "it_sector": ("DATASET_IT_SECTOR_DEVOPS.csv", "DevOpsCorp_ITSector_Table.csv"),
        "it": ("DATASET_IT_SECTOR_DEVOPS.csv", "DevOpsCorp_ITSector_Table.csv"),
        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.csv", "QuickCart_ECommerce_Table.csv"),
        "healthcare": ("DATASET_HEALTHCARE_LIFECARE.csv", "LifeCare_Healthcare_Table.csv"),
        "fintech": ("MASTER_DATABASE_DATASET.csv", "GlobalPay_Fintech_Table.csv"),
        "master": ("DATASET_MASTER_ALL_SECTORS_TABLE.csv", "SafeOps_Master_All_Sectors_Table.csv"),
        "all": ("DATASET_MASTER_ALL_SECTORS_TABLE.csv", "SafeOps_Master_All_Sectors_Table.csv"),
        "metrics": ("DATASET_SYSTEM_METRICS_TABLE.csv", "SafeOps_System_Metrics_Table.csv")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = find_dataset_file(src)
        if p and os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name, mimetype="text/csv")
    return jsonify({"error": f"Preset CSV table '{preset_name}' not found."}), 404

@app.route("/api/database/table-data/<preset_name>", methods=["GET"])
def get_table_data(preset_name):
    """Returns dataset as structured table (columns and rows) for live UI table viewer."""
    preset_name = preset_name.lower().strip()
    files = {
        "it_sector": "DATASET_IT_SECTOR_DEVOPS.csv",
        "it": "DATASET_IT_SECTOR_DEVOPS.csv",
        "ecommerce": "DATASET_ECOMMERCE_QUICKCART.csv",
        "healthcare": "DATASET_HEALTHCARE_LIFECARE.csv",
        "fintech": "MASTER_DATABASE_DATASET.csv",
        "master": "DATASET_MASTER_ALL_SECTORS_TABLE.csv",
        "all": "DATASET_MASTER_ALL_SECTORS_TABLE.csv",
        "metrics": "DATASET_SYSTEM_METRICS_TABLE.csv"
    }
    target_csv = files.get(preset_name, "DATASET_IT_SECTOR_DEVOPS.csv")
    p = find_dataset_file(target_csv)
    if not p or not os.path.exists(p):
        return jsonify({"success": False, "error": f"Table file for '{preset_name}' not found"}), 404

    rows = []
    columns = []
    with open(p, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        for r in reader:
            rows.append(r)

    return jsonify({
        "success": True,
        "preset": preset_name,
        "filename": target_csv,
        "columns": columns,
        "rows": rows,
        "total_rows": len(rows)
    })
'''

if "/api/database/download-preset-csv" not in code:
    idx_sub = code.find('@app.route("/api/subsystem-state')
    if idx_sub != -1:
        code = code[:idx_sub] + csv_routes + "\n\n" + code[idx_sub:]
        with open(APP_PATH, "w", encoding="utf-8") as f:
            f.write(code)
        print("Added CSV table download and view endpoints to app.py!")
    else:
        print("Could not find insertion point in app.py")
else:
    print("CSV routes already present in app.py")
