import sqlite3
import json
import os
import shutil

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
DB_PATH = os.path.join(PROJECT_DIR, "safeops.db")
MASTER_DB_PATH = os.path.join(PROJECT_DIR, "safeops_master.db")
JSON_PATH = os.path.join(PROJECT_DIR, "MASTER_DATABASE_DATASET.json")

def export_full_dataset():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Read all tables
    cursor.execute("SELECT * FROM safety_policies")
    policies = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM system_metrics")
    metrics = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM runbooks")
    runbooks = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT 50")
    incidents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50")
    audit_logs = [dict(r) for r in cursor.fetchall()]

    conn.close()

    master_dataset = {
        "metadata": {
            "dataset_name": "SafeOps AI - Master SRE Operational Database",
            "version": "2.4.0-ITIL",
            "hackathon": "Cynefian 24-Hour Student Hackathon - AI-Ops Track",
            "problem_statement": "AO-04: Automation Safe Enough to Leave Switched On",
            "team": "Idea Ignitors (XH-23) - Unnathi T M, Chaithanya N S, M Eshwar, Babitha M",
            "format": "Relational SQLite & JSON Interchange Schema",
            "coverage": {
                "problem_1_disk": "Critical (MySQL Core Dumps) & Uncritical (Routine /tmp & Inactive Logs)",
                "problem_2_worker": "Critical (Postgres Pool Saturation) & Uncritical (Routine Heap Trim)",
                "problem_3_queue": "Critical (Poison Pill Crash) & Uncritical (Off-Peak Backlog Drain)",
                "problem_4_ssl": "Critical (Root CA Revocation) & Uncritical (45-Day Preventive Audit)"
            }
        },
        "safety_policies": policies,
        "system_metrics": metrics,
        "runbooks": runbooks,
        "incidents": incidents,
        "audit_logs": audit_logs
    }

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(master_dataset, f, indent=2)
    print(f"Master JSON Dataset created at: {JSON_PATH} ({len(runbooks)} runbooks, {len(metrics)} metrics, {len(policies)} policies)")

    # Also make an exact master copy of the SQLite DB
    shutil.copyfile(DB_PATH, MASTER_DB_PATH)
    print(f"Master SQLite DB created at: {MASTER_DB_PATH}")

if __name__ == "__main__":
    export_full_dataset()
