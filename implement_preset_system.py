import re
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
APP_PATH = os.path.join(PROJECT_DIR, "app.py")
AI_ENGINE_PATH = os.path.join(PROJECT_DIR, "ai_engine.py")

# =========================================================================
# 1. UPDATE app.py
# =========================================================================
with open(APP_PATH, "r", encoding="utf-8") as f:
    app_code = f.read()

# Add get_active_preset and set_active_preset helpers if not present
preset_helpers = '''
def get_active_preset():
    """Returns the currently active industry dataset preset (ecommerce, healthcare, fintech)."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM safety_policies WHERE policy_key = 'active_preset'")
        row = cursor.fetchone()
        conn.close()
        if row and row['value']:
            return row['value']
    except Exception:
        pass
    return "fintech"

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
'''

if "def get_active_preset" not in app_code:
    # Insert right after get_db definition
    idx = app_code.find("def get_db():")
    idx_end = app_code.find("return conn", idx)
    idx_end = app_code.find("\n", idx_end)
    app_code = app_code[:idx_end+1] + preset_helpers + app_code[idx_end+1:]

# Add preset routes to app.py
preset_routes = '''
@app.route("/api/database/presets", methods=["GET"])
def get_database_presets():
    """Returns metadata and download links for the 3 distinct industry presets."""
    active = get_active_preset()
    presets_data = [
        {
            "id": "ecommerce",
            "name": "QuickCart Global E-Commerce & Food Delivery Cloud",
            "domain": "E-Commerce, Food Delivery & Real-Time Logistics",
            "tag": "QuickCart E-Commerce",
            "icon": "shopping-cart",
            "badge_color": "amber",
            "system_node": "quickcart-prod-cluster-01",
            "runbooks_count": 12,
            "metrics": {
                "disk": "98.7% (Invoicing Storage - 450MB left, 3,420 orders blocked)",
                "worker": "3,420 Orders Waiting (Rider Auto-Dispatch Lock)",
                "queue": "184,000 msgs (Rider GPS Stream - 88.2% Err)",
                "ssl": "4 Hours Left (Kitchen Partner Tablet API)"
            },
            "uncritical": {
                "disk": "51.4% (Restaurant Menu Preview Thumbnail Cache)",
                "worker": "Daily Loyalty Points Calculation Worker",
                "queue": "620 msgs (Analytics Clickstream Batch)",
                "ssl": "62 Days (Warehouse Logistics mTLS)"
            },
            "json_url": "/api/database/download-preset/ecommerce",
            "sql_url": "/api/database/download-preset-sql/ecommerce",
            "db_url": "/api/database/download-preset-db/ecommerce"
        },
        {
            "id": "healthcare",
            "name": "LifeCare Hospital ICU & Medical Patient Cloud",
            "domain": "Hospital Healthcare, Patient Vitals & Emergency EMS",
            "tag": "LifeCare Hospital ICU",
            "icon": "activity",
            "badge_color": "rose",
            "system_node": "lifecare-icu-cluster-04",
            "runbooks_count": 12,
            "metrics": {
                "disk": "99.1% (ICU Cardiac ECG - 180MB left, 42 patients)",
                "worker": "18 Active 911 Calls (EMS Ambulance Dispatch Locked)",
                "queue": "96,000 msgs (Bedside Vitals Stream - 94.1% Err)",
                "ssl": "5 Hours Left (Telemedicine Doctor Video Gateway)"
            },
            "uncritical": {
                "disk": "48.2% (Nurse Shift Attendance Scratch Files)",
                "worker": "Patient Discharge PDF Generator Soft Recycle",
                "queue": "410 msgs (Hospital Cafeteria Meal Orders)",
                "ssl": "75 Days (Medical IoT Device Encrypted Gateway)"
            },
            "json_url": "/api/database/download-preset/healthcare",
            "sql_url": "/api/database/download-preset-sql/healthcare",
            "db_url": "/api/database/download-preset-db/healthcare"
        },
        {
            "id": "fintech",
            "name": "GlobalPay Core Banking & Financial Infrastructure",
            "domain": "High-Frequency Payments, Ledger & PCI-DSS Banking",
            "tag": "GlobalPay Core Fintech",
            "icon": "shield-check",
            "badge_color": "sky",
            "system_node": "fintech-core-cluster-01",
            "runbooks_count": 26,
            "metrics": {
                "disk": "96.8% (Core Ledger Partition - $4.2M/min at risk)",
                "worker": "8,400 Settlements - $1,420,000 USD (Recon Lock)",
                "queue": "148,000 msgs (Fraud Detection Stream - 92.4% Err)",
                "ssl": "2 Hours Left (Core Payment Gateway TLS)"
            },
            "uncritical": {
                "disk": "54.2% (Docker Build Scratch & Dev Sandbox)",
                "worker": "Image Worker Heap Trim (15,400 Tasks)",
                "queue": "1,240 msgs (Analytics Clickstream Batch)",
                "ssl": "65 Days (Internal Gateway CA Trust Audit)"
            },
            "json_url": "/api/database/download-preset/fintech",
            "sql_url": "/api/database/download-preset-sql/fintech",
            "db_url": "/api/database/download-preset-db/fintech"
        }
    ]
    return jsonify({
        "success": True,
        "active_preset": active,
        "presets": presets_data
    })

@app.route("/api/database/load-preset/<preset_name>", methods=["POST"])
def load_database_preset(preset_name):
    """Loads one of the 3 pre-packaged domain datasets into SQLite."""
    preset_name = preset_name.lower().strip()
    preset_files = {
        "ecommerce": "safeops_ecommerce.db",
        "healthcare": "safeops_healthcare.db",
        "fintech": "safeops_master.db"
    }
    if preset_name not in preset_files:
        return jsonify({"success": False, "error": f"Unknown preset '{preset_name}'. Choose 'ecommerce', 'healthcare', or 'fintech'."}), 400

    source_db = os.path.join(os.path.dirname(__file__), preset_files[preset_name])
    live_db = os.path.join(os.path.dirname(__file__), "safeops.db")

    if not os.path.exists(source_db):
        return jsonify({"success": False, "error": f"Preset file {preset_files[preset_name]} not found on disk."}), 404

    # Copy preset DB to live DB
    shutil.copyfile(source_db, live_db)

    # Set active preset in policy table
    set_active_preset(preset_name)

    # Count runbooks and metrics
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM runbooks")
    rb_count = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM system_metrics")
    m_count = cursor.fetchone()[0]

    # Record in audit trail for ITIL tracking
    preset_titles = {
        "ecommerce": "QuickCart Global E-Commerce & Delivery Cloud",
        "healthcare": "LifeCare Hospital & ICU Patient Cloud",
        "fintech": "GlobalPay Core Banking & Financial Infrastructure"
    }
    cursor.execute("""
        INSERT INTO audit_logs (
            change_id, incident_code, incident_title, actor, action_type,
            risk_tier, command_executed, blast_radius, outcome,
            itil_justification, verification_details
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"CHG-MIGRATE-{preset_name.upper()}",
        f"INC-INIT-{preset_name[:3].upper()}",
        f"Domain Migration: Activated {preset_titles[preset_name]}",
        "Lead SRE Operator",
        "DOMAIN_DATASET_MIGRATION",
        "Tier 1 (Safe Auto)",
        f"sqlite3 load {preset_files[preset_name]}",
        "ZERO: Clean profile switch with automated ITIL record.",
        "SUCCESS",
        f"Operator requested industry dataset migration to {preset_titles[preset_name]} for hackathon presentation.",
        f"Verified: {rb_count} certified runbooks and {m_count} system metrics successfully initialized."
    ))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "preset": preset_name,
        "dataset_name": preset_titles[preset_name],
        "runbooks_count": rb_count,
        "metrics_count": m_count,
        "message": f"Successfully activated {preset_titles[preset_name]}! ({rb_count} Runbooks loaded)."
    })

@app.route("/api/database/download-preset/<preset_name>", methods=["GET"])
def download_preset_json(preset_name):
    """Download the JSON dataset for a chosen preset."""
    preset_name = preset_name.lower().strip()
    files = {
        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.json", "QuickCart_ECommerce_Dataset.json"),
        "healthcare": ("DATASET_HEALTHCARE_LIFECARE.json", "LifeCare_Healthcare_Dataset.json"),
        "fintech": ("MASTER_DATABASE_DATASET.json", "GlobalPay_Fintech_Dataset.json")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = os.path.join(os.path.dirname(__file__), src)
        if os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name)
    return jsonify({"error": "Preset file not found"}), 404

@app.route("/api/database/download-preset-sql/<preset_name>", methods=["GET"])
def download_preset_sql(preset_name):
    """Download the SQL Schema & Seeds for a chosen preset."""
    preset_name = preset_name.lower().strip()
    files = {
        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.sql", "QuickCart_ECommerce_Schema.sql"),
        "healthcare": ("DATASET_HEALTHCARE_LIFECARE.sql", "LifeCare_Healthcare_Schema.sql"),
        "fintech": ("MASTER_SRE_DATABASE.sql", "GlobalPay_Fintech_Schema.sql")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = os.path.join(os.path.dirname(__file__), src)
        if os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name)
    return jsonify({"error": "Preset SQL file not found"}), 404

@app.route("/api/database/download-preset-db/<preset_name>", methods=["GET"])
def download_preset_db(preset_name):
    """Download the SQLite binary for a chosen preset."""
    preset_name = preset_name.lower().strip()
    files = {
        "ecommerce": ("safeops_ecommerce.db", "QuickCart_ECommerce.db"),
        "healthcare": ("safeops_healthcare.db", "LifeCare_Healthcare.db"),
        "fintech": ("safeops_master.db", "GlobalPay_Fintech.db")
    }
    if preset_name in files:
        src, dl_name = files[preset_name]
        p = os.path.join(os.path.dirname(__file__), src)
        if os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=dl_name)
    return jsonify({"error": "Preset DB file not found"}), 404
'''

if "/api/database/presets" not in app_code:
    # Append right above /api/subsystem-state
    idx_sub = app_code.find("@app.route(\"/api/subsystem-state")
    if idx_sub != -1:
        app_code = app_code[:idx_sub] + preset_routes + "\n" + app_code[idx_sub:]

# Now replace inject_fault with dynamic preset support!
new_inject_fault = '''@app.route("/api/inject-fault", methods=["POST"])
def inject_fault():
    """
    Injects one of the 4 core problems from Figure 3 (Disk, Worker, Queue, SSL)
    dynamically customized to the currently active industry preset (QuickCart, LifeCare, or GlobalPay).
    """
    data = request.json or {}
    fault_type = data.get("fault_type", "disk_overflow")
    sub_type = data.get("sub_type", "standard")
    
    conn = get_db()
    cursor = conn.cursor()

    active_preset = get_active_preset()

    import uuid
    code = f"INC-{datetime.now().strftime('%M%S')}-{uuid.uuid4().hex[:4].upper()}"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =========================================================================
    # PRESET 1: E-COMMERCE & FOOD DELIVERY (QUICKCART)
    # =========================================================================
    if active_preset == "ecommerce":
        if fault_type == "disk_overflow":
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                title = "QuickCart Uncritical: Restaurant Menu Image Preview Cache Hygiene (51.4%)"
                server_node = "quickcart-menu-cdn"
                severity = "LOW"
                telemetry = {
                    "disk_usage": "51.4%",
                    "partition": "/var/cache/menu_renders",
                    "free_space": "148.5 GB free",
                    "largest_file": "dish_thumb_8410.webp (420KB)",
                    "sub_type": "routine_hygiene",
                    "is_uncritical": True,
                    "notes": "Off-peak dish preview thumbnail garbage collection. Reclaims 12GB silently with zero customer impact."
                }
                cursor.execute("UPDATE system_metrics SET value = 51.4, status = 'OK' WHERE metric_key = 'disk_usage_pct'")
            elif sub_type in ["core_dump", "critical_disk"]:
                title = "QuickCart Critical: Customer Order Invoicing & Tax Ledger Partition Full (98.7%)"
                server_node = "quickcart-invoice-01"
                severity = "CRITICAL"
                telemetry = {
                    "disk_usage": "98.7%",
                    "partition": "/var/data/quickcart/invoices",
                    "free_space": "450 MB remaining",
                    "orders_blocked": 3420,
                    "largest_file": "tax_invoice_batch_2025_Q4.db (38.2GB)",
                    "sub_type": "core_dump",
                    "notes": "Only 450MB left! 3,420 customer checkouts blocked. Deleting invoices violates fiscal tax compliance; snapshot to S3 cold storage required."
                }
                cursor.execute("UPDATE system_metrics SET value = 98.7, status = 'CRITICAL' WHERE metric_key = 'disk_usage_pct'")
            else:
                title = "QuickCart Warning: Delivery Rider GPS Location Telemetry Log Overflow (89.2%)"
                server_node = "quickcart-rider-gw"
                severity = "WARN"
                telemetry = {
                    "disk_usage": "89.2%",
                    "partition": "/var/log/rider_gps",
                    "free_space": "14.2 GB remaining",
                    "largest_file": "rider_breadcrumbs_20261028.trace (6.8GB)",
                    "sub_type": "logs",
                    "notes": "GPS breadcrumb telemetry log high-water mark. Compress breadcrumbs older than 48h to reclaim 34GB safely."
                }
                cursor.execute("UPDATE system_metrics SET value = 89.2, status = 'WARN' WHERE metric_key = 'disk_usage_pct'")

        elif fault_type == "worker_stuck":
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                title = "QuickCart Uncritical: Daily Loyalty Points Worker Soft Recycle"
                server_node = "loyalty-worker-01"
                severity = "LOW"
                telemetry = {
                    "worker_id": "loyalty-worker-01 (PID 3108)",
                    "last_heartbeat": "1s ago (ACTIVE)",
                    "tasks_completed": 18200,
                    "is_uncritical": True,
                    "notes": "Worker fully healthy. Soft memory compacting during idle task lull between reward calculations."
                }
                cursor.execute("UPDATE system_metrics SET value = 1.0, status = 'OK' WHERE metric_key = 'worker_status'")
            elif sub_type in ["db_exhaustion", "critical_worker"]:
                title = "QuickCart Critical: Live Rider Auto-Dispatch Engine Threadlock (3,420 Orders Waiting!)"
                server_node = "rider-dispatch-pool"
                severity = "CRITICAL"
                telemetry = {
                    "worker_id": "rider-dispatch-daemon (PID 1904)",
                    "last_heartbeat": "410s ago (DEADLOCKED)",
                    "pending_orders": 3420,
                    "sub_type": "db_exhaustion",
                    "notes": "Dispatch daemon deadlocked with 3,420 waiting customer deliveries! Blind kill causes duplicate rider dispatch and order loss. Operator sign-off required."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.0, status = 'CRITICAL' WHERE metric_key = 'worker_status'")
            else:
                title = "QuickCart Warning: Promotional WhatsApp / SMS Notification Worker Stalled (280s)"
                server_node = "promo-sender-03"
                severity = "WARN"
                telemetry = {
                    "worker_id": "promo-sender-03 (PID 5192)",
                    "last_heartbeat": "280s ago",
                    "sub_type": "deadlock_clean",
                    "notes": "Worker hung on external Twilio SMS gateway socket timeout. Safe to restart with automatic notification retry."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.5, status = 'WARN' WHERE metric_key = 'worker_status'")

        elif fault_type == "queue_growth":
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                title = "QuickCart Uncritical: Clickstream Batch Queue Ripple (620 msgs)"
                server_node = "kafka-quickcart-analytics"
                severity = "LOW"
                telemetry = {
                    "queue_name": "quickcart.clickstream.raw",
                    "queue_depth": 620,
                    "consumer_error_rate": "0.0%",
                    "is_uncritical": True,
                    "notes": "Normal off-peak browsing ripple. Sub-150ms processing SLA maintained."
                }
                cursor.execute("UPDATE system_metrics SET value = 620.0, status = 'OK' WHERE metric_key = 'queue_backlog_depth'")
            elif sub_type in ["poison_pill", "critical_queue"]:
                title = "QuickCart Critical: Live Rider GPS Tracking Kafka Queue Crash Loop (184,000 msgs - 88.2% Err)"
                server_node = "kafka-quickcart-edge"
                severity = "CRITICAL"
                telemetry = {
                    "queue_name": "quickcart.rider.gps.telemetry",
                    "queue_depth": 184000,
                    "consumer_error_rate": "88.2%",
                    "sub_type": "poison_pill",
                    "notes": "Corrupt rider GPS payload crashing all consumer pods in infinite crash loop. Scaling pods burns $3,800/hr compute with 0 progress! Quarantining bad offset required."
                }
                cursor.execute("UPDATE system_metrics SET value = 184000.0, status = 'CRITICAL' WHERE metric_key = 'queue_backlog_depth'")
            else:
                title = "QuickCart Warning: Flash Sale Ingress Queue Backlog (32,400 msgs)"
                server_node = "kafka-quickcart-orders"
                severity = "HIGH"
                telemetry = {
                    "queue_name": "quickcart.flash.orders",
                    "queue_depth": 32400,
                    "consumer_error_rate": "0.01%",
                    "active_pods": 4,
                    "sub_type": "traffic_surge",
                    "notes": "Legitimate evening meal rush surge. Safe to autoscale from 4 to 8 pods within policy limit (max 10)."
                }
                cursor.execute("UPDATE system_metrics SET value = 32400.0, status = 'WARN' WHERE metric_key = 'queue_backlog_depth'")

        elif fault_type == "ssl_expiry":
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                title = "QuickCart Uncritical: Internal Logistics Microservices TLS Certificate Health Check (62 Days)"
                server_node = "warehouse-auth.internal"
                severity = "INFO"
                telemetry = {
                    "domain": "warehouse-auth.internal",
                    "days_remaining": 62.0,
                    "is_uncritical": True,
                    "notes": "Proactive cryptographic handshake validation probe. System 100% operational."
                }
                cursor.execute("UPDATE system_metrics SET value = 62.0, status = 'OK' WHERE metric_key = 'ssl_cert_days'")
            elif sub_type in ["root_ca_broken", "critical_ssl"]:
                title = "QuickCart Critical: Kitchen Partner Tablet API Gateway SSL Expiring (4 Hours Left!)"
                server_node = "kitchen.quickcart.com"
                severity = "CRITICAL"
                telemetry = {
                    "domain": "kitchen.quickcart.com",
                    "hours_remaining": 4.0,
                    "days_remaining": 0.16,
                    "sub_type": "root_ca_broken",
                    "notes": "Orders will stop printing in 12,000 restaurant kitchens in 4 hours! Intermediate CA revoked upstream. Immediate CISO sign-off needed."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.16, status = 'CRITICAL' WHERE metric_key = 'ssl_cert_days'")
            else:
                title = "QuickCart Warning: Customer Mobile App Push Gateway TLS Expiring (3.8 Days)"
                server_node = "push.quickcart.com"
                severity = "WARN"
                telemetry = {
                    "domain": "push.quickcart.com",
                    "days_remaining": 3.8,
                    "sub_type": "routine_renew",
                    "notes": "Automated ACME certbot renewal and seamless nginx reload ready."
                }
                cursor.execute("UPDATE system_metrics SET value = 3.8, status = 'WARN' WHERE metric_key = 'ssl_cert_days'")

    # =========================================================================
    # PRESET 2: HEALTHCARE & MEDICAL ICU (LIFECARE)
    # =========================================================================
    elif active_preset == "healthcare":
        if fault_type == "disk_overflow":
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                title = "LifeCare Uncritical: Nurse Shift Log & Attendance Scratch Hygiene (48.2%)"
                server_node = "nurse-shift-01"
                severity = "LOW"
                telemetry = {
                    "disk_usage": "48.2%",
                    "partition": "/tmp/nurse_shifts",
                    "free_space": "120.4 GB free",
                    "sub_type": "routine_hygiene",
                    "is_uncritical": True,
                    "notes": "Routine off-peak administrative scratch file cleanup. Zero bedside or clinical impact."
                }
                cursor.execute("UPDATE system_metrics SET value = 48.2, status = 'OK' WHERE metric_key = 'disk_usage_pct'")
            elif sub_type in ["core_dump", "critical_disk"]:
                title = "LifeCare Critical: ICU Cardiac Telemetry Waveform Storage Full (99.1% - 180MB Left!)"
                server_node = "icu-cardiac-srv-01"
                severity = "CRITICAL"
                telemetry = {
                    "disk_usage": "99.1%",
                    "partition": "/var/data/icu/cardiac_ecg",
                    "free_space": "180 MB remaining",
                    "icu_patients_monitored": 42,
                    "sub_type": "core_dump",
                    "notes": "Only 180MB left! Continuous ECG waveforms for 42 intensive-care patients at risk of loss. Deleting files destroys clinical diagnostic evidence; HIPAA-compliant sync to cold storage required."
                }
                cursor.execute("UPDATE system_metrics SET value = 99.1, status = 'CRITICAL' WHERE metric_key = 'disk_usage_pct'")
            else:
                title = "LifeCare Warning: Radiology PACS X-Ray Image Preview Cache High (87.6%)"
                server_node = "pacs-storage-02"
                severity = "WARN"
                telemetry = {
                    "disk_usage": "87.6%",
                    "partition": "/var/cache/xray_pacs",
                    "free_space": "16.8 GB remaining",
                    "sub_type": "logs",
                    "notes": "Local PACS DICOM image preview cache high. Safe to purge cached previews older than 72h to reclaim 45GB. Primary hospital archive unaffected."
                }
                cursor.execute("UPDATE system_metrics SET value = 87.6, status = 'WARN' WHERE metric_key = 'disk_usage_pct'")

        elif fault_type == "worker_stuck":
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                title = "LifeCare Uncritical: Patient Discharge Document PDF Generator Soft Recycle (8,000 PDFs)"
                server_node = "pdf-gen-pool-03"
                severity = "LOW"
                telemetry = {
                    "worker_id": "pdf-gen-pool-03 (PID 4112)",
                    "last_heartbeat": "1s ago (ACTIVE)",
                    "tasks_completed": 8240,
                    "is_uncritical": True,
                    "notes": "Routine soft heap compaction during night shift lull. Zero clinical impact."
                }
                cursor.execute("UPDATE system_metrics SET value = 1.0, status = 'OK' WHERE metric_key = 'worker_status'")
            elif sub_type in ["db_exhaustion", "critical_worker"]:
                title = "LifeCare Critical: Emergency Ambulance Dispatch Service Threadlock (18 Active 911 Calls!)"
                server_node = "ems-dispatch-srv"
                severity = "CRITICAL"
                telemetry = {
                    "worker_id": "ems-dispatch-srv (PID 2048)",
                    "last_heartbeat": "390s ago (DEADLOCKED)",
                    "active_911_calls": 18,
                    "sub_type": "db_exhaustion",
                    "notes": "Worker locked with 18 live incoming emergency ambulance calls! Uncoordinated process kill risks lost ambulance dispatches. Radio failover sign-off required."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.0, status = 'CRITICAL' WHERE metric_key = 'worker_status'")
            else:
                title = "LifeCare Warning: Hospital Pharmacy Medication Restock Sync Stalled (320s)"
                server_node = "pharmacy-sync-02"
                severity = "WARN"
                telemetry = {
                    "worker_id": "pharmacy-sync-02 (PID 3840)",
                    "last_heartbeat": "320s ago",
                    "sub_type": "deadlock_clean",
                    "notes": "Worker hung on wholesale supplier medication API timeout. Safe to restart with automated inventory requeue."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.5, status = 'WARN' WHERE metric_key = 'worker_status'")

        elif fault_type == "queue_growth":
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                title = "LifeCare Uncritical: Hospital Cafeteria Patient Meal Order Ripple (410 msgs)"
                server_node = "kafka-dietary-orders"
                severity = "LOW"
                telemetry = {
                    "queue_name": "dietary.meal_orders",
                    "queue_depth": 410,
                    "consumer_error_rate": "0.0%",
                    "is_uncritical": True,
                    "notes": "Minor dietary meal order ripple. Handled smoothly within sub-150ms SLA."
                }
                cursor.execute("UPDATE system_metrics SET value = 410.0, status = 'OK' WHERE metric_key = 'queue_backlog_depth'")
            elif sub_type in ["poison_pill", "critical_queue"]:
                title = "LifeCare Critical: Bedside Vital Signs Alert Stream Crash Loop (96,000 msgs - 94.1% Err)"
                server_node = "kafka-medical-vitals"
                severity = "CRITICAL"
                telemetry = {
                    "queue_name": "vitals.patient.telemetry",
                    "queue_depth": 96000,
                    "consumer_error_rate": "94.1%",
                    "sub_type": "poison_pill",
                    "notes": "Malformed pulse oximeter telemetry crashing consumer pods in infinite loop. Scaling pods risks complete hospital telemetry failure! Isolate bad offset to Medical DLQ."
                }
                cursor.execute("UPDATE system_metrics SET value = 96000.0, status = 'CRITICAL' WHERE metric_key = 'queue_backlog_depth'")
            else:
                title = "LifeCare Warning: Outpatient Blood Lab Results Notification Backlog (19,800 msgs)"
                server_node = "kafka-medical-labs"
                severity = "HIGH"
                telemetry = {
                    "queue_name": "lab.results.broadcast",
                    "queue_depth": 19800,
                    "consumer_error_rate": "0.02%",
                    "active_pods": 2,
                    "sub_type": "traffic_surge",
                    "notes": "Morning blood test surge. Safe to autoscale from 2 to 6 pods within safety ceiling (max 10)."
                }
                cursor.execute("UPDATE system_metrics SET value = 19800.0, status = 'WARN' WHERE metric_key = 'queue_backlog_depth'")

        elif fault_type == "ssl_expiry":
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                title = "LifeCare Uncritical: Medical IoT Device Encrypted Gateway Health Audit (75.0 Days)"
                server_node = "devices.lifecare.internal"
                severity = "INFO"
                telemetry = {
                    "domain": "devices.lifecare.internal",
                    "days_remaining": 75.0,
                    "is_uncritical": True,
                    "notes": "Proactive cryptographic handshake validity audit on hospital medical IoT devices."
                }
                cursor.execute("UPDATE system_metrics SET value = 75.0, status = 'OK' WHERE metric_key = 'ssl_cert_days'")
            elif sub_type in ["root_ca_broken", "critical_ssl"]:
                title = "LifeCare Critical: Telemedicine Video Gateway Root CA Revocation (5 Hours Left!)"
                server_node = "telemed.lifecare.org"
                severity = "CRITICAL"
                telemetry = {
                    "domain": "telemed.lifecare.org",
                    "hours_remaining": 5.0,
                    "days_remaining": 0.20,
                    "sub_type": "root_ca_broken",
                    "notes": "Remote doctor consultations will drop in 5 hours! Root CA revoked upstream; ACME certbot cannot renew. Emergency CISO sign-off needed."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.20, status = 'CRITICAL' WHERE metric_key = 'ssl_cert_days'")
            else:
                title = "LifeCare Warning: Patient Health Records Portal TLS Expiring (4.2 Days)"
                server_node = "portal.lifecare.org"
                severity = "WARN"
                telemetry = {
                    "domain": "portal.lifecare.org",
                    "days_remaining": 4.2,
                    "sub_type": "routine_renew",
                    "notes": "Automated certbot renewal and seamless nginx reload ready."
                }
                cursor.execute("UPDATE system_metrics SET value = 4.2, status = 'WARN' WHERE metric_key = 'ssl_cert_days'")

    # =========================================================================
    # PRESET 3: FINTECH & CLOUD BANKING (GLOBALPAY - MASTER)
    # =========================================================================
    else:
        if fault_type == "disk_overflow":
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                title = "Uncritical: Developer Sandbox & Docker Build Scratch Hygiene (54.2% Disk)"
                server_node = "ci-runner-pool-02"
                severity = "LOW"
                telemetry = {
                    "disk_usage": "54.2%",
                    "partition": "/tmp/builds",
                    "free_space": "92.0 GB free",
                    "largest_file": "docker_layer_cached_7182.tmp (1.4GB)",
                    "sub_type": "routine_hygiene",
                    "is_uncritical": True,
                    "notes": "Routine off-peak maintenance: 1.4GB of temporary scratch build layers older than 14 days. Zero blast radius."
                }
                cursor.execute("UPDATE system_metrics SET value = 54.2, status = 'OK' WHERE metric_key = 'disk_usage_pct'")
            elif sub_type in ["core_dump", "critical_disk"]:
                title = "CRITICAL: PostgreSQL Primary WAL Storage Full (99.4% Capacity - 124MB Left!)"
                server_node = "prod-db-primary-01"
                severity = "CRITICAL"
                telemetry = {
                    "disk_usage": "99.4%",
                    "partition": "/var/lib/postgresql/pg_wal",
                    "free_space": "124 MB remaining",
                    "largest_file": "0000000100000A1B0000002F (16MB x 1,840 segments)",
                    "sub_type": "core_dump",
                    "notes": "Postgres WAL replication bottleneck. Only 124MB left before emergency PANIC shutdown! Deleting WAL breaks replica cluster."
                }
                cursor.execute("UPDATE system_metrics SET value = 99.4, status = 'CRITICAL' WHERE metric_key = 'disk_usage_pct'")
            else:
                title = "Warning: Nginx Reverse Proxy Static Cache Exceeded (88.5% Capacity)"
                server_node = "edge-proxy-01"
                severity = "WARN"
                telemetry = {
                    "disk_usage": "88.5%",
                    "partition": "/var/cache/nginx",
                    "free_space": "18.2 GB remaining",
                    "largest_file": "proxy_cache_asset_pack_v4.tar (4.8GB)",
                    "sub_type": "logs",
                    "notes": "Cache storage high-water mark reached. Safe to purge expired cached static objects without downtime."
                }
                cursor.execute("UPDATE system_metrics SET value = 88.5, status = 'WARN' WHERE metric_key = 'disk_usage_pct'")

        elif fault_type == "worker_stuck":
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                title = "Uncritical: Image Worker Heap Compaction & Soft Recycle (15,400 Tasks)"
                server_node = "media-worker-05"
                severity = "LOW"
                telemetry = {
                    "worker_id": "media-worker-05 (PID 7102)",
                    "last_heartbeat": "1s ago (ACTIVE)",
                    "tasks_completed": 15400,
                    "memory_fragmentation": "14.2%",
                    "sub_type": "routine_gc_trim",
                    "is_uncritical": True,
                    "notes": "Worker fully healthy. Soft graceful heap reload during idle gap between image batches."
                }
                cursor.execute("UPDATE system_metrics SET value = 1.0, status = 'OK' WHERE metric_key = 'worker_status'")
            elif sub_type in ["db_exhaustion", "critical_worker"]:
                title = "CRITICAL: Payment Reconciliation Engine Threadlock (8,400 In-Flight Settlements)"
                server_node = "fintech-recon-01"
                severity = "CRITICAL"
                telemetry = {
                    "worker_id": "py-recon-daemon (PID 4092)",
                    "last_heartbeat": "340s ago (DEADLOCKED)",
                    "in_flight_transactions": 8400,
                    "transaction_volume": "$1,420,000 USD",
                    "db_connections": "99/100 (SATURATED)",
                    "sub_type": "db_exhaustion",
                    "notes": "Thread deadlock waiting on Redis cluster lock while holding 99 Postgres connections. Blind SIGKILL will corrupt financial ledger. Mandates human sign-off."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.0, status = 'CRITICAL' WHERE metric_key = 'worker_status'")
            else:
                title = "Warning: Customer Email Dispatcher Celery Worker Hung (310s)"
                server_node = "worker-node-03"
                severity = "WARN"
                telemetry = {
                    "worker_id": "celery-worker-03 (PID 1840)",
                    "last_heartbeat": "310s ago",
                    "sub_type": "deadlock_clean",
                    "notes": "Worker hung in external SendGrid HTTP socket read. Clean isolated deadlock. Safe to restart autonomously."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.5, status = 'WARN' WHERE metric_key = 'worker_status'")

        elif fault_type == "queue_growth":
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                title = "Uncritical: Analytics Clickstream Batch Backlog Ripple (850 msgs)"
                server_node = "kafka-broker-02"
                severity = "LOW"
                telemetry = {
                    "queue_name": "analytics.clickstream.batch",
                    "queue_depth": 850,
                    "consumer_error_rate": "0.0%",
                    "sub_type": "routine_queue_balance",
                    "is_uncritical": True,
                    "notes": "Minor transient ripple well within SLA thresholds (<5,000 msgs). Auto-handled silently."
                }
                cursor.execute("UPDATE system_metrics SET value = 850.0, status = 'OK' WHERE metric_key = 'queue_backlog_depth'")
            elif sub_type in ["poison_pill", "critical_queue"]:
                title = "CRITICAL: Fraud Detection Real-Time Stream Consumer Crash Loop (148,000 msgs - 92.4% Err)"
                server_node = "kafka-broker-01"
                severity = "CRITICAL"
                telemetry = {
                    "queue_name": "fraud.transactions.stream",
                    "queue_depth": 148000,
                    "consumer_error_rate": "92.4%",
                    "active_pods": 3,
                    "sub_type": "poison_pill",
                    "notes": "Poison pill crashing consumer pods in infinite loop. Scaling pods burns compute with 0 progress! Must isolate bad offset to DLQ."
                }
                cursor.execute("UPDATE system_metrics SET value = 148000.0, status = 'CRITICAL' WHERE metric_key = 'queue_backlog_depth'")
            else:
                title = "Warning: Flash Sale Order Checkout Queue Influx (28,500 msgs)"
                server_node = "kafka-cluster-orders"
                severity = "HIGH"
                telemetry = {
                    "queue_name": "checkout.flash.events",
                    "queue_depth": 28500,
                    "consumer_error_rate": "0.02%",
                    "active_pods": 4,
                    "sub_type": "traffic_surge",
                    "notes": "Clean high volume promotional traffic surge. Safe to autoscale from 4 to 8 pods within policy limit (max 10)."
                }
                cursor.execute("UPDATE system_metrics SET value = 28500.0, status = 'WARN' WHERE metric_key = 'queue_backlog_depth'")

        elif fault_type == "ssl_expiry":
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                title = "Uncritical: Internal Microservice Mutual TLS Health Audit (58.0 Days)"
                server_node = "mTLS-auth.internal"
                severity = "INFO"
                telemetry = {
                    "domain": "mTLS-auth.internal",
                    "days_remaining": 58.0,
                    "ca_trust_status": "VALID_INTERNAL_CA",
                    "sub_type": "routine_audit_check",
                    "is_uncritical": True,
                    "notes": "Proactive cryptographic handshake cipher audit & OCSP check. Zero service changes."
                }
                cursor.execute("UPDATE system_metrics SET value = 58.0, status = 'OK' WHERE metric_key = 'ssl_cert_days'")
            elif sub_type in ["root_ca_broken", "critical_ssl"]:
                title = "CRITICAL: Edge API Gateway TLS Root CA Revocation (6 Hours Remaining!)"
                server_node = "api.globalpay.com"
                severity = "CRITICAL"
                telemetry = {
                    "domain": "api.globalpay.com",
                    "hours_remaining": 6.2,
                    "days_remaining": 0.25,
                    "ca_trust_status": "REVOKED / INTERMEDIATE CRL DRIFT",
                    "sub_type": "root_ca_broken",
                    "notes": "Intermediate CA key compromised & revoked upstream! Automated ACME renewals will fail. Operator must manually import re-signed bundle."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.25, status = 'CRITICAL' WHERE metric_key = 'ssl_cert_days'")
            else:
                title = "Warning: Customer Web Portal TLS Certificate Expiring (4.5 Days)"
                server_node = "portal.production.io"
                severity = "WARN"
                telemetry = {
                    "domain": "portal.production.io",
                    "days_remaining": 4.5,
                    "ca_trust_status": "VALID_LETS_ENCRYPT",
                    "sub_type": "routine_renew",
                    "notes": "Standard renewal policy window. DNS HTTP-01 challenge ready. Safe for automated key rotation and nginx reload."
                }
                cursor.execute("UPDATE system_metrics SET value = 4.5, status = 'WARN' WHERE metric_key = 'ssl_cert_days'")

    cursor.execute("""
        INSERT INTO incidents (
            incident_code, title, fault_type, server_node, severity, status,
            current_step, telemetry_snapshot, requires_human_approval, verification_status
        ) VALUES (?, ?, ?, ?, ?, 'DETECTED', 'detect', ?, 0, 'PENDING')
    """, (code, title, fault_type, server_node, severity, json.dumps(telemetry)))
    
    incident_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "incident_id": incident_id,
        "incident_code": code,
        "title": title,
        "telemetry": telemetry,
        "active_preset": active_preset,
        "message": f"Fault '{title}' successfully injected and detected in monitoring tool!"
    })
'''

# Replace old inject_fault in app_code
idx_inj_start = app_code.find("@app.route(\"/api/inject-fault")
idx_diag_start = app_code.find("@app.route(\"/api/diagnose/<int:incident_id>")
if idx_inj_start != -1 and idx_diag_start != -1:
    app_code = app_code[:idx_inj_start] + new_inject_fault + "\n\n" + app_code[idx_diag_start:]

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(app_code)

print("Updated app.py successfully!")
