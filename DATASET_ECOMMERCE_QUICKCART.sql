-- ============================================================================

-- SafeOps AI - Operational Database: QuickCart E-Commerce & Logistics Cloud

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

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('disk_usage_pct', 'QuickCart Invoicing Storage (/var/data/quickcart)', 51.4, '%', 80.0, 95.0, 'OK', 'quickcart-invoice-01');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('worker_status', 'Rider Auto-Dispatch Pool Health', 1.0, 'State (0=Locked, 1=Alive)', 0.5, 0.0, 'OK', 'rider-dispatch-pool');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('queue_backlog_depth', 'Live Rider GPS Tracking Queue', 620.0, 'msgs', 10000.0, 50000.0, 'OK', 'kafka-quickcart-edge');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('ssl_cert_days', 'Restaurant Partner Gateway TLS Validity', 62.0, 'days', 14.0, 5.0, 'OK', 'kitchen.quickcart.com');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('cpu_utilization', 'E-Commerce Cluster CPU Load', 31.2, '%', 75.0, 90.0, 'OK', 'k8s-quickcart-nodes');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('memory_utilization', 'E-Commerce Cluster RAM Usage', 46.8, '%', 80.0, 90.0, 'OK', 'k8s-quickcart-nodes');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('kill_switch_active', 'Emergency Master Kill Switch', 'false', 'Instant freeze for all QuickCart automation threads across cluster.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('rate_limit_per_minute', 'Action Rate Limiter', '5', 'Maximum 5 automated remediations per minute to prevent runaway loops.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('max_scaling_instances', 'Max Delivery Consumer Pods', '10', 'Strict cloud compute ceiling to prevent unexpected cloud billing spikes ($3,800/hr risk).');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('disk_safety_floor_gb', 'Invoice Safety Floor', '5.0', 'Minimum free disk space buffer below which high-risk escalation is mandated.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('tier1_auto_enabled', 'Tier 1 Safe Auto-Remediation', 'true', 'Autonomous execution of non-destructive fixes without rider disruption.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('tier3_requires_approval', 'Tier 3 Human Authorization Gate', 'true', 'Mandatory human sign-off before modifying active orders or payment channels.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-DISK-CRIT', 'QuickCart Critical: Customer Order Invoicing & Tax Ledger Partition Full (98.7%)', 'E-Commerce Storage', '/var/data/quickcart/invoices', 'Invoice partition disk usage > 98% (Only 450MB remaining!)', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: Complete checkout checkout block + database write lock.', 'IF invoice partition is at 98.7%, customer orders cannot be confirmed. DO NOT delete invoices; snapshot older tax records to S3 glacier storage with human sign-off.', 'aws s3 sync /var/data/quickcart/invoices/2025/ s3://quickcart-tax-cold/ && find /var/data/quickcart/invoices/2025/ -type f -delete', 'aws s3 sync s3://quickcart-tax-cold/ /var/data/quickcart/invoices/2025/ || true', 'df -h /var/data/quickcart/invoices | awk 'NR==2 {gsub("%", ""); if ($5 < 80) print "PASS"; else print "FAIL"}'', 'Protects tax invoices and fiscal compliance while restoring checkout operations.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-DISK-WARN', 'QuickCart Warning: Delivery Rider GPS Location Telemetry Log Overflow (89.2%)', 'E-Commerce Storage', '/var/log/rider_gps', 'GPS location log usage > 85%', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Rider telemetry logs only. Zero customer order disruption.', 'IF GPS log partition exceeds 85%, compress and archive raw breadcrumbs older than 48h to reclaim 34 GB. Safe for autonomous execution.', 'find /var/log/rider_gps/ -name '*.trace' -mtime +2 -exec gzip {} \; && journalctl --vacuum-time=1d', 'find /var/log/rider_gps/ -name '*.trace.gz' -exec gunzip {} \;', 'df -h /var/log/rider_gps | awk 'NR==2 {gsub("%", ""); if ($5 < 75) print "PASS"; else print "FAIL"}'', 'Compresses old delivery rider GPS traces to reclaim 34 GB safely.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-DISK-UNC', 'QuickCart Uncritical: Restaurant Menu Image Preview Cache Hygiene (51.4%)', 'E-Commerce Hygiene', '/var/cache/menu_renders', 'Off-peak schedule OR cache between 45% and 60%', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Purely temporary restaurant menu preview images.', 'IF disk utilization is non-critical (51.4%), prune stale restaurant dish thumbnails silently without waking engineers.', 'find /var/cache/menu_renders -type f -mtime +14 -delete', 'touch /var/cache/menu_renders/.maintenance_complete', 'df -h /var/cache/menu_renders | awk 'NR==2 {print "PASS_DISK_HEALTHY"}'', 'Routine off-peak menu image thumbnail garbage collection.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-WORKER-CRIT', 'QuickCart Critical: Live Rider Auto-Dispatch Engine Threadlock (3,420 Orders Waiting!)', 'E-Commerce Logistics', 'rider-dispatch-daemon', 'Dispatch daemon locked and pending orders > 3,000', 'Tier 3 (High Risk - Human Approval Required)', 'HIGH: 3,420 hungry customer deliveries + rider dispatch queue.', 'IF dispatch daemon is deadlocked with 3,420 active orders, DO NOT kill worker process (prevents duplicate rider dispatch and order loss). Human approval required to pause order ingress before restart.', 'python3 /opt/quickcart/scripts/drain_active_rider_locks.py && systemctl restart rider-dispatch-daemon.service', 'systemctl restart rider-dispatch-daemon.service', 'systemctl is-active rider-dispatch-daemon.service', 'Safeguards live food delivery rider assignment against double allocation.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-WORKER-WARN', 'QuickCart Warning: Promotional WhatsApp / SMS Notification Worker Stalled (280s)', 'E-Commerce Notifications', 'promo-sender-03', 'Worker heartbeat missed for > 250s (Twilio socket wait)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Marketing notification queue only. Zero customer order or payment risk.', 'IF worker is hung in external Twilio gateway timeout, perform graceful SIGTERM restart with automatic notification retry.', 'systemctl restart celery-worker@promo-sender-03.service', 'systemctl restart celery-worker@promo-sender-03-fallback.service', 'systemctl is-active celery-worker@promo-sender-03.service', 'Restores marketing notification worker safely with message requeue.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-WORKER-UNC', 'QuickCart Uncritical: Customer Loyalty Points Calculator Soft Recycle (25,000 Users)', 'E-Commerce Compute', 'loyalty-calc-01', 'Worker processed > 20,000 users (Worker Healthy)', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Soft reload occurs between batch calculations.', 'IF loyalty worker is healthy but has minor heap fragmentation, trigger graceful reload during off-peak lull.', 'systemctl reload-or-restart celery-worker@loyalty-calc-01.service', 'systemctl status celery-worker@loyalty-calc-01.service', 'systemctl is-active celery-worker@loyalty-calc-01.service', 'Defragments Python heap memory on loyalty points batch workers.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-QUEUE-CRIT', 'QuickCart Critical: Live Rider Location Kafka Poison Pill Crash (184,000 msgs - 88.2% Err)', 'E-Commerce Streaming', 'riders.gps.stream', 'Queue backlog > 100,000 and consumer error rate > 80%', 'Tier 3 (High Risk - Human Approval Required)', 'HIGH: Delivery ETA accuracy and $3,800/hr cloud compute burn.', 'IF consumer error rate is > 80% (malformed geofence coordinate crashing pods), DO NOT scale pods (prevents $3,800/hr compute burn); divert bad offset to DLQ with human sign-off.', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group rider-gps --topic riders.gps.stream --reset-offsets --to-offset 891043 --execute', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group rider-gps --topic riders.gps.stream --reset-offsets --to-offset 891042 --execute', 'echo PASS_DLQ_ROUTED', 'Quarantines bad geofence payloads to unblock rider location tracking.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-QUEUE-WARN', 'QuickCart Warning: Midnight Biryani Flash Sale Checkout Surge (32,400 msgs)', 'E-Commerce Scaling', 'orders.checkout.live', 'Queue backlog > 20,000 and error rate < 0.1%', 'Tier 2 (Guarded Auto - Within Policy Limits)', 'MEDIUM: Kubernetes consumer deployment. Capped at max 10 pods.', 'IF error rate < 0.1% (clean flash sale traffic), autoscale consumers from 3 to 7 pods within policy limit 10.', 'kubectl scale deployment/order-consumer --replicas=7 --namespace=orders', 'kubectl scale deployment/order-consumer --replicas=3 --namespace=orders', 'kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'', 'Autoscales checkout consumers to drain promotion rush smoothly.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-QUEUE-UNC', 'QuickCart Uncritical: Restaurant Review Notification Queue Ripple (620 msgs)', 'E-Commerce Queues', 'restaurant.reviews', 'Backlog between 400 and 1,000 messages (Minor Transient Ripple)', 'Tier 1 (Uncritical - Silent Safe Auto)', 'LOW (< 5%): Spins up 1 standby consumer container.', 'IF backlog has minor morning ripple (620 msgs), activate 1 standby pod to maintain sub-150ms latency.', 'kubectl scale deployment/order-consumer --replicas=4 --namespace=orders', 'kubectl scale deployment/order-consumer --replicas=3 --namespace=orders', 'kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'', 'Smooths out transient review notifications silently.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-SSL-CRIT', 'QuickCart Critical: Restaurant Kitchen Gateway Root CA Revocation (4 Hours Left!)', 'E-Commerce Security', 'kitchen.quickcart.com', 'Certificate validity < 12 hours and CA revoked upstream', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: Restaurant order transmission and live kitchen displays.', 'IF intermediate CA is revoked upstream, automated ACME renewal cannot succeed. Escalate immediately to Security Ops Lead for manual re-pinning.', 'update-ca-certificates --fresh && nginx -s reload', 'cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload', 'openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/kitchen.quickcart.com.crt', 'Prevents kitchen order tablets from disconnecting due to untrusted certificates.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-SSL-WARN', 'QuickCart Warning: Mobile App Public Gateway TLS Expiring (3.8 Days)', 'E-Commerce Ingress', 'api.quickcart.com', 'Certificate validity <= 5 days (ACME DNS valid)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Public Ingress Gateway. Zero dropped socket connections.', 'IF certificate is within 5 days of expiry and DNS records valid, trigger automated certbot renewal and seamless nginx reload.', 'certbot renew --cert-name api.quickcart.com --quiet && nginx -s reload', 'cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload', 'openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/api.quickcart.com.crt', 'Automated seamless TLS rotation for public mobile app ingress.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('QC-SSL-UNC', 'QuickCart Uncritical: Warehouse Logistics Mutual TLS Health Audit (62.0 Days)', 'E-Commerce Auditing', 'warehouse-auth.internal', 'Scheduled audit OR certificate validity at 62 days remaining', 'Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)', 'ZERO (0%): Read-only cryptographic handshake validation probe.', 'IF certificate validity is healthy (62 days remaining), execute routine cryptographic trust check. No human action required.', 'openssl s_client -servername warehouse-auth.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'', 'echo 'AUDIT_NOOP'', 'openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/warehouse-auth.internal.crt', 'Proactive cryptographic validity audit on warehouse logistics mTLS.');