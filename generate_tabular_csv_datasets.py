import csv
import json
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
DATASETS_DIR = os.path.join(PROJECT_DIR, "datasets")
os.makedirs(DATASETS_DIR, exist_ok=True)

# =========================================================================
# 1. GENERATE IT SECTOR TABULAR CSV
# =========================================================================
it_json_path = os.path.join(PROJECT_DIR, "DATASET_IT_SECTOR_DEVOPS.json")
with open(it_json_path, "r", encoding="utf-8") as f:
    it_data = json.load(f)

it_csv_rows = []
for rb in it_data.get("runbooks", []):
    tier = rb.get("safe_action_tier", "")
    is_human = "YES (Mandatory Sign-off)" if ("Tier 3" in tier or "Human" in tier) else "NO (Safe Autonomous)"
    
    # Determine severity
    if "Critical" in rb["title"] or "CRIT" in rb["runbook_id"]:
        severity = "CRITICAL (P1)"
    elif "Warning" in rb["title"] or "WARN" in rb["runbook_id"]:
        severity = "WARNING (P2)"
    else:
        severity = "UNCRITICAL (Routine P4)"
        
    it_csv_rows.append({
        "Runbook_ID": rb.get("runbook_id"),
        "Title": rb.get("title"),
        "Subsystem_Category": rb.get("category"),
        "Target_Subsystem": rb.get("target_subsystem"),
        "Severity": severity,
        "Trigger_Condition": rb.get("trigger_condition"),
        "Safe_Action_Tier": rb.get("safe_action_tier"),
        "Blast_Radius": rb.get("blast_radius"),
        "Requires_Human_Approval": is_human,
        "Remediation_Command": rb.get("remediation_command"),
        "Rollback_Command": rb.get("rollback_command"),
        "Verification_Check": rb.get("verification_check"),
        "SRE_Operational_Judgment": rb.get("judgment_rules")
    })

fieldnames_rb = [
    "Runbook_ID", "Title", "Subsystem_Category", "Target_Subsystem", "Severity",
    "Trigger_Condition", "Safe_Action_Tier", "Blast_Radius", "Requires_Human_Approval",
    "Remediation_Command", "Rollback_Command", "Verification_Check", "SRE_Operational_Judgment"
]

def write_csv(filename, rows, fieldnames):
    p1 = os.path.join(PROJECT_DIR, filename)
    p2 = os.path.join(DATASETS_DIR, filename)
    for p in [p1, p2]:
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    print(f"Generated {filename} successfully ({len(rows)} rows)!")

write_csv("DATASET_IT_SECTOR_DEVOPS.csv", it_csv_rows, fieldnames_rb)

# =========================================================================
# 2. GENERATE ALL OTHER SECTOR TABULAR CSVs
# =========================================================================
sectors = {
    "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.json", "DATASET_ECOMMERCE_QUICKCART.csv"),
    "healthcare": ("DATASET_HEALTHCARE_LIFECARE.json", "DATASET_HEALTHCARE_LIFECARE.csv"),
    "fintech": ("MASTER_DATABASE_DATASET.json", "MASTER_DATABASE_DATASET.csv")
}

master_all_rows = []

# Add IT rows to master
for r in it_csv_rows:
    row_copy = dict(r)
    row_copy["Industry_Sector"] = "IT Sector (DevOpsCorp)"
    master_all_rows.append(row_copy)

for sec_key, (json_fn, csv_fn) in sectors.items():
    jp = os.path.join(PROJECT_DIR, json_fn)
    if os.path.exists(jp):
        with open(jp, "r", encoding="utf-8") as f:
            sec_data = json.load(f)
            
        sec_rows = []
        for rb in sec_data.get("runbooks", []):
            tier = rb.get("safe_action_tier", "")
            is_human = "YES (Mandatory Sign-off)" if ("Tier 3" in tier or "Human" in tier) else "NO (Safe Autonomous)"
            
            if "Critical" in rb["title"] or "CRIT" in rb["runbook_id"] or "01" in rb["runbook_id"]:
                severity = "CRITICAL (P1)"
            elif "Warning" in rb["title"] or "WARN" in rb["runbook_id"]:
                severity = "WARNING (P2)"
            elif "Uncritical" in rb["title"] or "UNC" in rb["runbook_id"]:
                severity = "UNCRITICAL (Routine P4)"
            else:
                severity = "STANDARD (P3)"
                
            row_dict = {
                "Runbook_ID": rb.get("runbook_id"),
                "Title": rb.get("title"),
                "Subsystem_Category": rb.get("category"),
                "Target_Subsystem": rb.get("target_subsystem"),
                "Severity": severity,
                "Trigger_Condition": rb.get("trigger_condition"),
                "Safe_Action_Tier": rb.get("safe_action_tier"),
                "Blast_Radius": rb.get("blast_radius"),
                "Requires_Human_Approval": is_human,
                "Remediation_Command": rb.get("remediation_command"),
                "Rollback_Command": rb.get("rollback_command"),
                "Verification_Check": rb.get("verification_check", "echo PASS"),
                "SRE_Operational_Judgment": rb.get("judgment_rules", "")
            }
            sec_rows.append(row_dict)
            
            # Master row
            master_row = dict(row_dict)
            master_row["Industry_Sector"] = sec_data.get("metadata", {}).get("dataset_name", sec_key.upper())
            master_all_rows.append(master_row)
            
        write_csv(csv_fn, sec_rows, fieldnames_rb)

# Write Master All Sectors Table CSV
fieldnames_master = ["Industry_Sector"] + fieldnames_rb
write_csv("DATASET_MASTER_ALL_SECTORS_TABLE.csv", master_all_rows, fieldnames_master)

# =========================================================================
# 3. GENERATE SYSTEM METRICS TABULAR CSV
# =========================================================================
metrics_rows = []
for sec_name, jfn in [
    ("IT Sector (DevOpsCorp)", "DATASET_IT_SECTOR_DEVOPS.json"),
    ("E-Commerce (QuickCart)", "DATASET_ECOMMERCE_QUICKCART.json"),
    ("Healthcare (LifeCare ICU)", "DATASET_HEALTHCARE_LIFECARE.json"),
    ("Fintech (GlobalPay)", "MASTER_DATABASE_DATASET.json")
]:
    jp = os.path.join(PROJECT_DIR, jfn)
    if os.path.exists(jp):
        with open(jp, "r", encoding="utf-8") as f:
            s_data = json.load(f)
            for m in s_data.get("system_metrics", []):
                metrics_rows.append({
                    "Industry_Sector": sec_name,
                    "Metric_Key": m.get("metric_key"),
                    "Subsystem_Metric_Name": m.get("name"),
                    "Live_Value": m.get("value"),
                    "Unit": m.get("unit"),
                    "Threshold_Warn": m.get("threshold_warn"),
                    "Threshold_Crit": m.get("threshold_crit"),
                    "Current_Status": m.get("status"),
                    "Target_Server_Node": m.get("server_node")
                })

fieldnames_metrics = [
    "Industry_Sector", "Metric_Key", "Subsystem_Metric_Name", "Live_Value", "Unit",
    "Threshold_Warn", "Threshold_Crit", "Current_Status", "Target_Server_Node"
]
write_csv("DATASET_SYSTEM_METRICS_TABLE.csv", metrics_rows, fieldnames_metrics)

print(f"\nSuccessfully generated all table datasets! Total master scenario rows: {len(master_all_rows)}")
