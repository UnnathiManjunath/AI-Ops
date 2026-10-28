import json
import sqlite3
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"

presets = {
    "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.json", "safeops_ecommerce.db", "DATASET_ECOMMERCE_QUICKCART.sql", "QuickCart E-Commerce & Logistics Cloud"),
    "healthcare": ("DATASET_HEALTHCARE_LIFECARE.json", "safeops_healthcare.db", "DATASET_HEALTHCARE_LIFECARE.sql", "LifeCare Hospital & ICU Patient Cloud")
}

schema_sql = """CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    threshold_warn REAL NOT NULL,
    threshold_crit REAL NOT NULL,
    status TEXT NOT NULL,
    server_node TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS safety_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_key TEXT UNIQUE NOT NULL,
    policy_name TEXT NOT NULL,
    value TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runbooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    runbook_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    target_subsystem TEXT NOT NULL,
    trigger_condition TEXT NOT NULL,
    safe_action_tier TEXT NOT NULL,
    blast_radius TEXT NOT NULL,
    judgment_rules TEXT NOT NULL,
    remediation_command TEXT NOT NULL,
    rollback_command TEXT NOT NULL,
    verification_check TEXT NOT NULL,
    documentation TEXT
);

CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    fault_type TEXT NOT NULL,
    server_node TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    current_step INTEGER DEFAULT 1,
    telemetry_snapshot TEXT NOT NULL,
    root_cause TEXT,
    ai_reasoning TEXT,
    risk_tier TEXT,
    blast_radius_desc TEXT,
    proposed_action TEXT,
    remediation_command TEXT,
    rollback_command TEXT,
    verification_check TEXT,
    requires_human_approval BOOLEAN DEFAULT 0,
    approved_by TEXT,
    approval_timestamp TIMESTAMP,
    remediation_logs TEXT,
    verification_status TEXT,
    rollback_triggered BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    change_id TEXT UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    incident_code TEXT,
    incident_title TEXT,
    actor TEXT NOT NULL,
    action_type TEXT NOT NULL,
    risk_tier TEXT,
    command_executed TEXT,
    blast_radius TEXT,
    outcome TEXT NOT NULL,
    itil_justification TEXT,
    verification_details TEXT
);"""

for preset_key, (json_fn, db_fn, sql_fn, display_name) in presets.items():
    json_path = os.path.join(PROJECT_DIR, json_fn)
    db_path = os.path.join(PROJECT_DIR, db_fn)
    sql_path = os.path.join(PROJECT_DIR, sql_fn)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(schema_sql)
    
    sql_statements = [
        f"-- ============================================================================",
        f"-- SafeOps AI - Operational Database: {display_name}",
        f"-- Team: Idea Ignitors (XH-23) - Cynefian Hackathon Problem AO-04",
        f"-- ============================================================================",
        schema_sql
    ]
    
    for m in data.get('system_metrics', []):
        cur.execute("""INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (m['metric_key'], m['name'], m['value'], m['unit'], m['threshold_warn'], m['threshold_crit'], m['status'], m['server_node']))
        sql_statements.append(f"INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('{m['metric_key']}', '{m['name']}', {m['value']}, '{m['unit']}', {m['threshold_warn']}, {m['threshold_crit']}, '{m['status']}', '{m['server_node']}');")

    for p in data.get('safety_policies', []):
        cur.execute("""INSERT INTO safety_policies (policy_key, policy_name, value, description)
                       VALUES (?, ?, ?, ?)""",
                    (p['policy_key'], p['policy_name'], p['value'], p['description']))
        clean_desc = p['description'].replace("'", "''")
        sql_statements.append(f"INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('{p['policy_key']}', '{p['policy_name']}', '{p['value']}', '{clean_desc}');")

    for rb in data.get('runbooks', []):
        cur.execute("""INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (rb['runbook_id'], rb['title'], rb['category'], rb['target_subsystem'], rb['trigger_condition'], rb['safe_action_tier'], rb['blast_radius'], rb['judgment_rules'], rb['remediation_command'], rb['rollback_command'], rb['verification_check'], rb['documentation']))
        clean_desc = rb['documentation'].replace("'", "''")
        clean_rules = rb['judgment_rules'].replace("'", "''")
        clean_blast = rb['blast_radius'].replace("'", "''")
        clean_title = rb['title'].replace("'", "''")
        clean_trig = rb['trigger_condition'].replace("'", "''")
        sql_statements.append(f"INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('{rb['runbook_id']}', '{clean_title}', '{rb['category']}', '{rb['target_subsystem']}', '{clean_trig}', '{rb['safe_action_tier']}', '{clean_blast}', '{clean_rules}', '{rb['remediation_command']}', '{rb['rollback_command']}', '{rb['verification_check']}', '{clean_desc}');")

    conn.commit()
    conn.close()
    
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(sql_statements))
        
    print(f"Successfully built {db_fn} and {sql_fn}!")
