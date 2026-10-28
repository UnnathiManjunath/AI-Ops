-- ============================================================================

-- SafeOps AI - Operational Database: LifeCare Hospital & ICU Patient Cloud

-- Team: Idea Ignitors (XH-23) - Cynefian Hackathon Problem AO-04

-- ============================================================================

CREATE TABLE IF NOT EXISTS system_metrics (
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
);

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('disk_usage_pct', 'ICU Cardiac Waveform Storage (/var/data/icu)', 48.2, '%', 80.0, 95.0, 'OK', 'icu-cardiac-srv-01');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('worker_status', 'Emergency Ambulance Dispatch Health', 1.0, 'State (0=Locked, 1=Alive)', 0.5, 0.0, 'OK', 'ems-dispatch-srv');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('queue_backlog_depth', 'Patient Bedside Vital Signs Queue', 410.0, 'msgs', 10000.0, 50000.0, 'OK', 'kafka-medical-vitals');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('ssl_cert_days', 'Telemedicine Video Gateway TLS Validity', 75.0, 'days', 14.0, 5.0, 'OK', 'telemed.lifecare.org');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('cpu_utilization', 'Hospital Core Telemetry CPU Load', 24.5, '%', 75.0, 90.0, 'OK', 'k8s-med-nodes');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('memory_utilization', 'Hospital Core Telemetry RAM Usage', 39.8, '%', 80.0, 90.0, 'OK', 'k8s-med-nodes');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('kill_switch_active', 'Emergency Master Kill Switch', 'false', 'Instant freeze for all hospital automation threads across medical cluster.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('rate_limit_per_minute', 'Action Rate Limiter', '5', 'Strict rate limit of max 5 automated actions per minute to prevent loops.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('max_scaling_instances', 'Max Hospital Telemetry Pods', '10', 'Strict ceiling on hospital Kubernetes pods to prevent network congestion.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('disk_safety_floor_gb', 'ICU Storage Safety Floor', '5.0', 'Minimum free space buffer below which high-risk clinical escalation is forced.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('tier1_auto_enabled', 'Tier 1 Safe Auto-Remediation', 'true', 'Autonomous execution of non-clinical administrative fixes.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('tier3_requires_approval', 'Tier 3 Clinical Human Gate', 'true', 'Mandatory human physician/SRE approval before touching clinical vitals or medical state.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-DISK-CRIT', 'LifeCare Critical: ICU Cardiac Telemetry Waveform Storage Full (99.1% - 180MB Left!)', 'Medical Storage', '/var/data/icu/cardiac_ecg', 'Cardiac waveform partition > 99% (Only 180MB remaining!)', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: Continuous ECG waveforms for 42 intensive-care patients.', 'IF cardiac waveform partition is at 99.1%, deleting files destroys clinical diagnostic evidence! Safely sync older records to HIPAA-compliant medical cold storage with human sign-off.', 'aws s3 sync /var/data/icu/cardiac_ecg/archive/ s3://lifecare-hipaa-cold/ && rm -f /var/data/icu/cardiac_ecg/archive/*.dat', 'aws s3 sync s3://lifecare-hipaa-cold/ /var/data/icu/cardiac_ecg/archive/ || true', 'df -h /var/data/icu/cardiac_ecg | awk 'NR==2 {gsub("%", ""); if ($5 < 85) print "PASS"; else print "FAIL"}'', 'Preserves continuous patient ECG clinical records under strict HIPAA compliance.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-DISK-WARN', 'LifeCare Warning: Radiology PACS X-Ray Image Preview Cache High (87.6%)', 'Medical Storage', '/var/cache/xray_pacs', 'Radiology cache usage > 85%', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Local PACS preview image cache only. Zero primary medical record risk.', 'IF radiology cache exceeds 85%, purge cached DICOM preview images older than 72h. Primary hospital archive remains intact. Reclaims 45 GB.', 'find /var/cache/xray_pacs/ -type f -mtime +3 -delete && systemctl reload dcm4chee.service', 'echo 'ROLLBACK_DICOM_PREVIEWS'', 'df -h /var/cache/xray_pacs | awk 'NR==2 {gsub("%", ""); if ($5 < 75) print "PASS"; else print "FAIL"}'', 'Purges temporary PACS preview images without affecting master patient X-rays.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-DISK-UNC', 'LifeCare Uncritical: Nurse Shift Log & Attendance Scratch Hygiene (48.2%)', 'Medical Hygiene', '/tmp/nurse_shifts', 'Off-peak schedule OR disk between 40% and 55%', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Temporary administrative nurse attendance scratch files.', 'IF disk utilization is non-critical (48.2%), purge stale nurse attendance scratch files older than 14 days silently without waking hospital staff.', 'find /tmp/nurse_shifts -type f -name '*.tmp' -mtime +14 -delete', 'touch /tmp/nurse_shifts/.maintenance_complete', 'df -h /tmp/nurse_shifts | awk 'NR==2 {print "PASS_DISK_HEALTHY"}'', 'Routine administrative scratch cleanup with zero clinical impact.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-WORKER-CRIT', 'LifeCare Critical: Emergency Ambulance Dispatch Service Threadlock (18 Active 911 Calls!)', 'Medical EMS', 'ems-dispatch-srv', 'EMS dispatch worker locked with > 10 active ambulance dispatches', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: 18 live emergency ambulance response routes.', 'IF EMS dispatch worker is locked with 18 incoming ambulance calls, DO NOT kill worker process (prevents lost ambulance dispatches). Human operator sign-off required to failover to backup radio relay before restart.', 'python3 /opt/lifecare/scripts/failover_ems_radio_relay.py && systemctl restart ems-dispatch-srv.service', 'systemctl restart ems-dispatch-srv.service', 'systemctl is-active ems-dispatch-srv.service', 'Guarantees continuous 911 emergency ambulance dispatch routing.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-WORKER-WARN', 'LifeCare Warning: Hospital Pharmacy Medication Restock Sync Stalled (320s)', 'Medical Pharmacy', 'pharmacy-sync-02', 'Worker heartbeat missed for > 300s (Supplier wholesale API timeout)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Non-urgent medication restock inventory sync. Zero bedside patient risk.', 'IF worker is hung waiting on supplier wholesale API, perform graceful SIGTERM restart with automatic inventory message requeue.', 'systemctl restart celery-worker@pharmacy-sync-02.service', 'systemctl restart celery-worker@pharmacy-sync-02-fallback.service', 'systemctl is-active celery-worker@pharmacy-sync-02.service', 'Restores hospital pharmacy inventory background sync safely.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-WORKER-UNC', 'LifeCare Uncritical: Patient Discharge Document PDF Generator Soft Recycle (8,000 PDFs)', 'Medical Compute', 'pdf-gen-pool-03', 'Worker processed > 5,000 PDFs (Worker Healthy)', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Soft reload occurs between discharge document batches.', 'IF PDF generator worker is healthy but has minor heap fragmentation, trigger graceful reload during off-peak night lull.', 'systemctl reload-or-restart celery-worker@pdf-gen-pool-03.service', 'systemctl status celery-worker@pdf-gen-pool-03.service', 'systemctl is-active celery-worker@pdf-gen-pool-03.service', 'Compacts memory on hospital discharge document generation daemons.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-QUEUE-CRIT', 'LifeCare Critical: Bedside Vital Signs Alert Stream Crash Loop (96,000 msgs - 94.1% Err)', 'Medical Vitals', 'vitals.patient.telemetry', 'Queue backlog > 50,000 and consumer error rate > 80%', 'Tier 3 (High Risk - Human Approval Required)', 'HIGH: Bedside vital signs monitoring telemetry and false alarm suppression.', 'IF consumer error rate is > 80% (malformed pulse oximeter firmware telemetry crashing pods), DO NOT scale pods; isolate bad offset to Medical Quarantine Queue with human sign-off.', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group bedside-vitals --topic vitals.patient.telemetry --reset-offsets --to-offset 302194 --execute', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group bedside-vitals --topic vitals.patient.telemetry --reset-offsets --to-offset 302193 --execute', 'echo PASS_DLQ_ROUTED', 'Quarantines malformed pulse oximeter telemetry to restore vital signs alerting.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-QUEUE-WARN', 'LifeCare Warning: Outpatient Blood Lab Results Notification Backlog (19,800 msgs)', 'Medical Labs', 'lab.results.broadcast', 'Queue backlog > 15,000 and error rate < 0.1%', 'Tier 2 (Guarded Auto - Within Policy Limits)', 'MEDIUM: Outpatient notification pods. Capped at max 10 pods.', 'IF error rate < 0.1% (morning blood test rush), autoscale consumer pods from 2 to 6 pods within policy limit 10.', 'kubectl scale deployment/order-consumer --replicas=6 --namespace=orders', 'kubectl scale deployment/order-consumer --replicas=2 --namespace=orders', 'kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'', 'Autoscales outpatient lab notification consumers to deliver test results.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-QUEUE-UNC', 'LifeCare Uncritical: Hospital Cafeteria Patient Meal Order Ripple (410 msgs)', 'Medical Queues', 'dietary.meal_orders', 'Backlog between 300 and 800 messages (Minor Transient Ripple)', 'Tier 1 (Uncritical - Silent Safe Auto)', 'LOW (< 5%): Spins up 1 standby consumer container.', 'IF backlog has minor morning ripple (410 msgs), activate 1 standby pod to maintain sub-150ms processing SLA.', 'kubectl scale deployment/order-consumer --replicas=4 --namespace=orders', 'kubectl scale deployment/order-consumer --replicas=3 --namespace=orders', 'kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'', 'Smooths out hospital dietary meal order notifications silently.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-SSL-CRIT', 'LifeCare Critical: Telemedicine Video Gateway Root CA Revocation (5 Hours Left!)', 'Medical Security', 'telemed.lifecare.org', 'Certificate validity < 12 hours and CA revoked upstream', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: Live remote doctor video consultations + HIPAA compliance.', 'IF intermediate CA is revoked upstream, automated ACME renewal cannot succeed. Escalate immediately to Hospital Chief Information Security Officer (CISO).', 'update-ca-certificates --fresh && nginx -s reload', 'cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload', 'openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/telemed.lifecare.org.crt', 'Protects live telemedicine remote patient video consultations from disconnection.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-SSL-WARN', 'LifeCare Warning: Patient Health Records Portal TLS Expiring (4.2 Days)', 'Medical Ingress', 'portal.lifecare.org', 'Certificate validity <= 5 days (ACME HTTP-01 valid)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Public patient records portal. Seamless configuration reload.', 'IF certificate is within 5 days of expiry and DNS records valid, trigger automated certbot renewal and seamless nginx reload.', 'certbot renew --cert-name portal.lifecare.org --quiet && nginx -s reload', 'cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload', 'openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/portal.lifecare.org.crt', 'Automated seamless TLS rotation for patient records portal.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('MED-SSL-UNC', 'LifeCare Uncritical: Medical IoT Device Encrypted Gateway Health Audit (75.0 Days)', 'Medical Auditing', 'devices.lifecare.internal', 'Scheduled audit OR certificate validity at 75 days remaining', 'Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)', 'ZERO (0%): Read-only cryptographic handshake validation probe.', 'IF certificate validity is healthy (75 days remaining), execute routine cryptographic trust check. No human action required.', 'openssl s_client -servername devices.lifecare.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'', 'echo 'AUDIT_NOOP'', 'openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/devices.lifecare.internal.crt', 'Proactive cryptographic validity audit on hospital medical IoT devices.');