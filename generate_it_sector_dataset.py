import json
import sqlite3
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"

# =========================================================================
# IT SECTOR & DEVOPS CLOUD DATASET (DEVOPSCORP)
# =========================================================================
it_dataset = {
    "metadata": {
        "dataset_name": "DevOpsCorp Enterprise IT & Cloud Infrastructure",
        "domain": "IT Sector, Enterprise DevOps CI/CD, Kubernetes & Software Engineering Cloud",
        "system_id": "devops-cloud-prod-01",
        "version": "3.2.0-IT-SECTOR",
        "team": "Idea Ignitors (XH-23) - Cynefian Hackathon"
    },
    "system_metrics": [
        {
            "metric_key": "disk_usage_pct",
            "name": "CI/CD Docker Registry & Artifact Storage (/var/lib/docker)",
            "value": 49.6,
            "unit": "%",
            "threshold_warn": 80.0,
            "threshold_crit": 95.0,
            "status": "OK",
            "server_node": "ci-runner-cluster-01"
        },
        {
            "metric_key": "worker_status",
            "name": "GitOps Terraform & Kubernetes Deployment Controller",
            "value": 1.0,
            "unit": "State (0=Locked, 1=Alive)",
            "threshold_warn": 0.5,
            "threshold_crit": 0.0,
            "status": "OK",
            "server_node": "gitops-controller-pool"
        },
        {
            "metric_key": "queue_backlog_depth",
            "name": "GitHub Enterprise Code Merge & Webhook Queue",
            "value": 580.0,
            "unit": "msgs",
            "threshold_warn": 10000.0,
            "threshold_crit": 50000.0,
            "status": "OK",
            "server_node": "kafka-devops-telemetry"
        },
        {
            "metric_key": "ssl_cert_days",
            "name": "Enterprise Single Sign-On (SSO / Okta SAML) Ingress TLS",
            "value": 60.0,
            "unit": "days",
            "threshold_warn": 14.0,
            "threshold_crit": 5.0,
            "status": "OK",
            "server_node": "sso.corp-it.internal"
        },
        {
            "metric_key": "cpu_utilization",
            "name": "Kubernetes CI/CD Worker Node Pool CPU Load",
            "value": 28.4,
            "unit": "%",
            "threshold_warn": 75.0,
            "threshold_crit": 90.0,
            "status": "OK",
            "server_node": "k8s-devops-workers"
        },
        {
            "metric_key": "memory_utilization",
            "name": "Kubernetes CI/CD Worker Node Pool RAM Usage",
            "value": 42.1,
            "unit": "%",
            "threshold_warn": 80.0,
            "threshold_crit": 90.0,
            "status": "OK",
            "server_node": "k8s-devops-workers"
        }
    ],
    "safety_policies": [
        {"policy_key": "active_preset", "policy_name": "Active Operational Preset", "value": "it_sector", "description": "DevOpsCorp Enterprise IT & Cloud Infrastructure"},
        {"policy_key": "kill_switch_active", "policy_name": "Emergency Master Kill Switch", "value": "false", "description": "Instant freeze for all enterprise IT automated remediation jobs across clusters."},
        {"policy_key": "rate_limit_per_minute", "policy_name": "Action Rate Limiter", "value": "5", "description": "Maximum 5 automated remediations per minute to prevent runaway build loops."},
        {"policy_key": "max_scaling_instances", "policy_name": "Max CI/CD Build Pods", "value": "10", "description": "Strict Kubernetes node compute ceiling to prevent runaway AWS/GCP cloud billing ($4,200/hr risk)."},
        {"policy_key": "disk_safety_floor_gb", "policy_name": "Artifact Storage Safety Floor", "value": "5.0", "description": "Minimum free disk buffer below which high-risk escalation is mandated."},
        {"policy_key": "tier1_auto_enabled", "policy_name": "Tier 1 Safe Auto-Remediation", "value": "true", "description": "Autonomous execution of non-destructive cache pruning without deployment risk."},
        {"policy_key": "tier3_requires_approval", "policy_name": "Tier 3 Principal DevOps Human Gate", "value": "true", "description": "Mandatory Principal SRE sign-off before modifying production container registries or live clusters."}
    ],
    "runbooks": [
        {
            "runbook_id": "IT-DISK-CRIT",
            "title": "DevOpsCorp Critical: Production Docker Registry & Container Image Layer Partition Full (99.3% - 210MB Left!)",
            "category": "IT Cloud Storage",
            "target_subsystem": "/var/lib/docker/overlay2",
            "trigger_condition": "Docker storage partition > 99% (Only 210MB remaining, 84 production deployments blocked!)",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: 84 enterprise production software deployments blocked + container daemon freeze.",
            "judgment_rules": "IF Docker storage partition is at 99.3%, software releases cannot deploy! DO NOT run 'docker system prune -a' blindly (destroys active base images and prevents rollback tags). Snapshot production release image tags to AWS ECR / Google Artifact Registry with Principal DevOps sign-off.",
            "remediation_command": "aws ecr sync-images /var/lib/docker/production-tags/ && docker image prune --filter 'until=72h' --force",
            "rollback_command": "docker pull registry.corp-it.internal:5000/base-images/production:v3.2.0",
            "verification_check": "df -h /var/lib/docker | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 85) print \"PASS\"; else print \"FAIL\"}'",
            "documentation": "Safeguards production container base images and release tags against accidental deletion during emergency disk exhaustion."
        },
        {
            "runbook_id": "IT-DISK-WARN",
            "title": "DevOpsCorp Warning: Developer Build Cache & Gradle/NPM Artifact High-Water Mark (86.4%)",
            "category": "IT Cloud Storage",
            "target_subsystem": "/var/cache/build_artifacts",
            "trigger_condition": "Artifact cache usage > 85%",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Local builder temporary NPM/Maven cache only. Zero production service impact.",
            "judgment_rules": "IF build cache partition exceeds 85%, purge unreferenced dependency tarballs and intermediate compiler outputs older than 7 days to reclaim 32 GB. Safe for autonomous execution.",
            "remediation_command": "find /var/cache/build_artifacts/ -name '*.tar.gz' -mtime +7 -delete && journalctl --vacuum-time=2d",
            "rollback_command": "touch /var/cache/build_artifacts/.cache_rebuild_ready",
            "verification_check": "df -h /var/cache/build_artifacts | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
            "documentation": "Clears stale dependency caches safely without interrupting active developer compilation jobs."
        },
        {
            "runbook_id": "IT-DISK-UNC",
            "title": "DevOpsCorp Uncritical: Stale CI Unit Test Report XML & SonarQube Scratch Hygiene (49.6%)",
            "category": "IT Cloud Hygiene",
            "target_subsystem": "/tmp/ci_test_scratch",
            "trigger_condition": "Off-peak nightly schedule OR scratch storage between 40% and 55%",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "ZERO (0%): Temporary JUnit XML test results and coverage heatmaps older than 14 days.",
            "judgment_rules": "IF disk utilization is non-critical (49.6%), silently prune old JUnit test results and code coverage scratch files older than 14 days without alerting on-call engineers.",
            "remediation_command": "find /tmp/ci_test_scratch -type f -name '*.xml' -mtime +14 -delete",
            "rollback_command": "touch /tmp/ci_test_scratch/.maintenance_complete",
            "verification_check": "df -h /tmp/ci_test_scratch | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
            "documentation": "Routine nightly housekeeping for CI/CD test runner ephemeral scratch disks."
        },
        {
            "runbook_id": "IT-WORKER-CRIT",
            "title": "DevOpsCorp Critical: GitOps Terraform Cloud Sync Controller Threadlock (48 Active Microservice Rollouts!)",
            "category": "IT DevOps Compute",
            "target_subsystem": "gitops-sync-controller",
            "trigger_condition": "GitOps sync controller heartbeat missing > 300s while 48 microservice deployments in-flight",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: 48 live production microservice Kubernetes deployments + AWS cloud infrastructure state lock.",
            "judgment_rules": "IF GitOps controller is locked during live rollout, DO NOT kill worker process (prevents split-brain Terraform cloud state and orphaned Kubernetes deployments). Human SRE authorization required to release distributed DynamoDB state lock safely before restarting.",
            "remediation_command": "terraform force-unlock -force 8a2f-109b-c43e && systemctl restart gitops-sync-controller.service",
            "rollback_command": "systemctl restart gitops-sync-controller.service",
            "verification_check": "systemctl is-active gitops-sync-controller.service",
            "documentation": "Prevents catastrophic split-brain cloud state in enterprise Terraform GitOps pipelines."
        },
        {
            "runbook_id": "IT-WORKER-WARN",
            "title": "DevOpsCorp Warning: Enterprise Slack / Jira CI/CD Notification Webhook Worker Stalled (260s)",
            "category": "IT Notifications",
            "target_subsystem": "slack-jira-notifier-02",
            "trigger_condition": "Worker heartbeat missed for > 240s (Slack API rate limit socket wait)",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Developer notification channel only. Zero production software deployment risk.",
            "judgment_rules": "IF notification worker is stalled on external Slack webhook rate limits, perform graceful SIGTERM restart with automatic event backoff and retry.",
            "remediation_command": "systemctl restart celery-worker@slack-jira-notifier-02.service",
            "rollback_command": "systemctl restart celery-worker@slack-jira-notifier-02-fallback.service",
            "verification_check": "systemctl is-active celery-worker@slack-jira-notifier-02.service",
            "documentation": "Graceful cycling of developer Slack/Jira notification dispatchers without message loss."
        },
        {
            "runbook_id": "IT-WORKER-UNC",
            "title": "DevOpsCorp Uncritical: Static Code Linter & AST Syntax Analyzer Soft Memory Recycle (25,000 Commits)",
            "category": "IT Code Analysis",
            "target_subsystem": "code-linter-daemon-04",
            "trigger_condition": "Worker processed > 20,000 commits (Worker Alive and Processing)",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "ZERO (0%): Soft reload occurs between pull request linting batches.",
            "judgment_rules": "IF linter worker is healthy but has minor Python/Go memory heap fragmentation, trigger graceful soft reload during nightly sprint lull.",
            "remediation_command": "systemctl reload-or-restart celery-worker@code-linter-daemon-04.service",
            "rollback_command": "systemctl status celery-worker@code-linter-daemon-04.service",
            "verification_check": "systemctl is-active celery-worker@code-linter-daemon-04.service",
            "documentation": "Compacts memory on automated static code analysis and security AST parsing daemons."
        },
        {
            "runbook_id": "IT-QUEUE-CRIT",
            "title": "DevOpsCorp Critical: OpenTelemetry Distributed Trace Kafka Ingress Crash Loop (172,000 msgs - 91.5% Err)",
            "category": "IT Observability",
            "target_subsystem": "otel.traces.ingress",
            "trigger_condition": "Queue backlog > 100,000 and consumer error rate > 80%",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "HIGH: Enterprise observability pipeline + Kubernetes cluster compute capacity.",
            "judgment_rules": "IF error rate is > 80% (malformed OpenTelemetry span JSON payload crashing collector pods in infinite loops), DO NOT autoscale pods (burns $4,200/hr compute with 0 progress); isolate corrupt offset to Observability Dead Letter Queue (DLQ) with human sign-off.",
            "remediation_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group otel-collectors --topic otel.traces.ingress --reset-offsets --to-offset 602819 --execute",
            "rollback_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group otel-collectors --topic otel.traces.ingress --reset-offsets --to-offset 602818 --execute",
            "verification_check": "echo PASS_DLQ_ROUTED",
            "documentation": "Isolates corrupt OpenTelemetry tracing payloads to protect enterprise APM monitoring from brownouts."
        },
        {
            "runbook_id": "IT-QUEUE-WARN",
            "title": "DevOpsCorp Warning: GitHub Enterprise Pull Request Merge Webhook Queue Backlog (38,000 msgs)",
            "category": "IT Developer Tools",
            "target_subsystem": "github.pr.merges",
            "trigger_condition": "Queue backlog > 25,000 and consumer error rate < 0.05%",
            "safe_action_tier": "Tier 2 (Guarded Auto - Within Policy Limits)",
            "blast_radius": "MEDIUM: GitHub webhook consumers. Capped at policy ceiling of 10 pods.",
            "judgment_rules": "IF consumer error rate is low (<0.05% during 5:00 PM sprint code freeze / merge rush), autoscale webhook processing pods from 3 to 9 pods within safety ceiling (max 10).",
            "remediation_command": "kubectl scale deployment/github-webhook-consumer --replicas=9 --namespace=ci",
            "rollback_command": "kubectl scale deployment/github-webhook-consumer --replicas=3 --namespace=ci",
            "verification_check": "kubectl get deployment/github-webhook-consumer -o jsonpath='{.status.readyReplicas}'",
            "documentation": "Autoscales GitHub webhook delivery pods during end-of-sprint code merge rushes."
        },
        {
            "runbook_id": "IT-QUEUE-UNC",
            "title": "DevOpsCorp Uncritical: Engineering DORA Metrics Analytics Batch Queue Ripple (580 msgs)",
            "category": "IT Queues",
            "target_subsystem": "engineering.dora.metrics",
            "trigger_condition": "Backlog between 400 and 1,000 messages (Minor Off-Peak Ripple)",
            "safe_action_tier": "Tier 1 (Uncritical - Silent Safe Auto)",
            "blast_radius": "LOW (< 5%): Spins up 1 standby consumer container.",
            "judgment_rules": "IF backlog has minor evening ripple (580 msgs), activate 1 standby pod to maintain sub-150ms processing SLA on developer velocity dashboards.",
            "remediation_command": "kubectl scale deployment/dora-consumer --replicas=3 --namespace=ci",
            "rollback_command": "kubectl scale deployment/dora-consumer --replicas=2 --namespace=ci",
            "verification_check": "kubectl get deployment/dora-consumer -o jsonpath='{.status.readyReplicas}'",
            "documentation": "Maintains sub-second delivery for developer productivity and DORA analytics metrics."
        },
        {
            "runbook_id": "IT-SSL-CRIT",
            "title": "DevOpsCorp Critical: Corporate Single Sign-On (SSO / Okta SAML) Ingress TLS Expiring in 3 Hours (15,000 Engineers Locked Out!)",
            "category": "IT Security & IAM",
            "target_subsystem": "sso.corp-it.internal",
            "trigger_condition": "SSO certificate validity < 6 hours and internal HashiCorp Vault root CA revoked upstream",
            "safe_action_tier": "Tier 3 (High Risk - Human Approval Required)",
            "blast_radius": "CRITICAL: 15,000 enterprise software engineers and staff access to GitHub, AWS, Jira & Slack.",
            "judgment_rules": "IF SSO gateway certificate expires in 3 hours and internal Vault intermediate CA is revoked, automated certbot renewals will fail! 15,000 engineers will lose access to all cloud systems. Escalate immediately to Enterprise CISO and Lead IAM Architect.",
            "remediation_command": "vault write auth/cert/config certificate=@/etc/ssl/certs/vault-root-renewed.crt && nginx -s reload",
            "rollback_command": "cp /etc/ssl/backup/last_known_good_sso.crt /etc/ssl/certs/ && nginx -s reload",
            "verification_check": "openssl verify -CAfile /etc/ssl/certs/vault-root.crt /etc/ssl/certs/sso.corp-it.internal.crt",
            "documentation": "Protects enterprise IAM Single Sign-On infrastructure against authentication lockout."
        },
        {
            "runbook_id": "IT-SSL-WARN",
            "title": "DevOpsCorp Warning: Staging Kubernetes Cluster Wildcard Ingress TLS Certificate Expiring (4.1 Days)",
            "category": "IT Ingress Security",
            "target_subsystem": "*.staging.corp-it.io",
            "trigger_condition": "Certificate validity <= 5 days (ACME DNS-01 challenge ready)",
            "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
            "blast_radius": "LOW: Staging microservices ingress only. Zero production service downtime.",
            "judgment_rules": "IF certificate is within 5 days of expiry and DNS records valid, trigger automated certbot DNS-01 renewal and seamless ingress nginx reload.",
            "remediation_command": "certbot renew --cert-name staging.corp-it.io --preferred-challenges dns-01 --quiet && nginx -s reload",
            "rollback_command": "cp /etc/ssl/backup/last_known_good_staging.crt /etc/ssl/certs/ && nginx -s reload",
            "verification_check": "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/staging.corp-it.io.crt",
            "documentation": "Automated renewal of staging cluster wildcard TLS certificates."
        },
        {
            "runbook_id": "IT-SSL-UNC",
            "title": "DevOpsCorp Uncritical: Internal Kubernetes Istio Service Mesh Mutual TLS (mTLS) Audit (60.0 Days)",
            "category": "IT Security Audit",
            "target_subsystem": "cluster.local",
            "trigger_condition": "Scheduled audit OR certificate validity at 60 days remaining",
            "safe_action_tier": "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
            "blast_radius": "ZERO (0%): Read-only cryptographic handshake validation probe.",
            "judgment_rules": "IF internal service mesh certificate validity is healthy (60 days remaining), execute routine cipher suite verification. No human intervention needed.",
            "remediation_command": "istioctl proxy-config secret deployment/ingressgateway.istio-system && echo 'AUDIT_VERIFIED_VALID'",
            "rollback_command": "echo 'AUDIT_NOOP'",
            "verification_check": "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/istio-mtls.crt",
            "documentation": "Proactive cryptographic validity audit across internal Kubernetes microservice mTLS sidecars."
        }
    ]
}

# 1. Write JSON File
json_path = os.path.join(PROJECT_DIR, "DATASET_IT_SECTOR_DEVOPS.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(it_dataset, f, indent=2)

print(f"Generated {json_path} successfully!")

# 2. Build SQLite DB and SQL schema file
db_path = os.path.join(PROJECT_DIR, "safeops_it_sector.db")
sql_path = os.path.join(PROJECT_DIR, "DATASET_IT_SECTOR_DEVOPS.sql")

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

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

cur.executescript(schema_sql)

sql_statements = [
    "-- ============================================================================",
    "-- SafeOps AI - Operational Database: DevOpsCorp Enterprise IT & Cloud Infrastructure",
    "-- Track: Cynefian 24-Hour Student Hackathon - AI-Ops Track (Problem AO-04)",
    "-- Team: Idea Ignitors (XH-23) - Unnathi T M, Chaithanya N S, M Eshwar, Babitha M",
    "-- Domain: IT Sector, Enterprise CI/CD, Kubernetes & Software Engineering Cloud",
    "-- ============================================================================",
    schema_sql
]

for m in it_dataset.get('system_metrics', []):
    cur.execute("""INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (m['metric_key'], m['name'], m['value'], m['unit'], m['threshold_warn'], m['threshold_crit'], m['status'], m['server_node']))
    sql_statements.append(f"INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('{m['metric_key']}', '{m['name']}', {m['value']}, '{m['unit']}', {m['threshold_warn']}, {m['threshold_crit']}, '{m['status']}', '{m['server_node']}');")

for p in it_dataset.get('safety_policies', []):
    cur.execute("""INSERT INTO safety_policies (policy_key, policy_name, value, description)
                   VALUES (?, ?, ?, ?)""",
                (p['policy_key'], p['policy_name'], p['value'], p['description']))
    clean_desc = p['description'].replace("'", "''")
    sql_statements.append(f"INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('{p['policy_key']}', '{p['policy_name']}', '{p['value']}', '{clean_desc}');")

for rb in it_dataset.get('runbooks', []):
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

with open(sql_path, "w", encoding="utf-8") as f:
    f.write('\n\n'.join(sql_statements))

print(f"Generated {db_path} and {sql_path} successfully!")
