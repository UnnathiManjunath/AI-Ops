import re
import os

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
APP_PATH = os.path.join(PROJECT_DIR, "app.py")
AI_ENGINE_PATH = os.path.join(PROJECT_DIR, "ai_engine.py")
INDEX_PATH = os.path.join(PROJECT_DIR, "templates", "index.html")
APP_JS_PATH = os.path.join(PROJECT_DIR, "static", "js", "app.js")

# =========================================================================
# 1. UPDATE app.py
# =========================================================================
with open(APP_PATH, "r", encoding="utf-8") as f:
    app_code = f.read()

# 1.1 Add it_sector to get_database_presets
it_preset_dict = '''        {
            "id": "it_sector",
            "name": "DevOpsCorp Enterprise IT & Cloud Infrastructure",
            "domain": "IT Sector, Enterprise DevOps CI/CD, Kubernetes & Software Engineering Cloud",
            "tag": "DevOpsCorp IT Sector",
            "icon": "terminal",
            "badge_color": "emerald",
            "system_node": "devops-cloud-prod-01",
            "runbooks_count": 12,
            "metrics": {
                "disk": "99.3% (Docker Registry - 210MB left, 84 production deployments blocked)",
                "worker": "48 Active Microservice Rollouts (GitOps Terraform Lock)",
                "queue": "172,000 msgs (OpenTelemetry Traces - 91.5% Err)",
                "ssl": "3 Hours Left (Corporate SSO / Okta SAML Ingress)"
            },
            "uncritical": {
                "disk": "49.6% (Stale CI JUnit Test Reports & SonarQube Scratch)",
                "worker": "Static Code Linter AST Memory Compaction (25k Commits)",
                "queue": "580 msgs (Engineering DORA Metrics Ripple)",
                "ssl": "60 Days (Kubernetes Istio Service Mesh mTLS)"
            },
            "json_url": "/api/database/download-preset/it_sector",
            "sql_url": "/api/database/download-preset-sql/it_sector",
            "db_url": "/api/database/download-preset-db/it_sector"
        },
'''

if '"id": "it_sector"' not in app_code:
    # Insert right at the top of presets_data list
    app_code = app_code.replace('presets_data = [\n', 'presets_data = [\n' + it_preset_dict)

# 1.2 Add it_sector to load_database_preset
if '"it_sector": "safeops_it_sector.db"' not in app_code:
    app_code = app_code.replace(
        'preset_files = {\n        "ecommerce": "safeops_ecommerce.db",',
        'preset_files = {\n        "it_sector": "safeops_it_sector.db",\n        "ecommerce": "safeops_ecommerce.db",'
    )
    app_code = app_code.replace(
        'preset_titles = {\n        "ecommerce": "QuickCart Global E-Commerce & Delivery Cloud",',
        'preset_titles = {\n        "it_sector": "DevOpsCorp Enterprise IT & Cloud Infrastructure",\n        "ecommerce": "QuickCart Global E-Commerce & Delivery Cloud",'
    )

# 1.3 Add it_sector to download endpoints
if '"it_sector": ("DATASET_IT_SECTOR_DEVOPS.json"' not in app_code:
    app_code = app_code.replace(
        'files = {\n        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.json", "QuickCart_ECommerce_Dataset.json"),',
        'files = {\n        "it_sector": ("DATASET_IT_SECTOR_DEVOPS.json", "DevOpsCorp_ITSector_Dataset.json"),\n        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.json", "QuickCart_ECommerce_Dataset.json"),'
    )
    app_code = app_code.replace(
        'files = {\n        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.sql", "QuickCart_ECommerce_Schema.sql"),',
        'files = {\n        "it_sector": ("DATASET_IT_SECTOR_DEVOPS.sql", "DevOpsCorp_ITSector_Schema.sql"),\n        "ecommerce": ("DATASET_ECOMMERCE_QUICKCART.sql", "QuickCart_ECommerce_Schema.sql"),'
    )
    app_code = app_code.replace(
        'files = {\n        "ecommerce": ("safeops_ecommerce.db", "QuickCart_ECommerce.db"),',
        'files = {\n        "it_sector": ("safeops_it_sector.db", "DevOpsCorp_ITSector.db"),\n        "ecommerce": ("safeops_ecommerce.db", "QuickCart_ECommerce.db"),'
    )

# 1.4 Add it_sector fault injection logic
it_fault_injection = '''    # =========================================================================
    # PRESET: IT SECTOR & DEVOPS CLOUD (DEVOPSCORP)
    # =========================================================================
    if active_preset in ["it_sector", "it"]:
        if fault_type == "disk_overflow":
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                title = "DevOpsCorp Uncritical: Stale CI Unit Test Report XML & SonarQube Scratch Hygiene (49.6%)"
                server_node = "ci-runner-pool-04"
                severity = "LOW"
                telemetry = {
                    "disk_usage": "49.6%",
                    "partition": "/tmp/ci_test_scratch",
                    "free_space": "135.2 GB free",
                    "largest_file": "junit_test_report_build_8819.xml (24MB)",
                    "sub_type": "routine_hygiene",
                    "is_uncritical": True,
                    "notes": "Nightly maintenance: 24MB of temporary XML test logs older than 14 days. Zero blast radius."
                }
                cursor.execute("UPDATE system_metrics SET value = 49.6, status = 'OK' WHERE metric_key = 'disk_usage_pct'")
            elif sub_type in ["core_dump", "critical_disk"]:
                title = "DevOpsCorp Critical: Production Docker Registry & Container Image Layer Partition Full (99.3% - 210MB Left!)"
                server_node = "ci-runner-cluster-01"
                severity = "CRITICAL"
                telemetry = {
                    "disk_usage": "99.3%",
                    "partition": "/var/lib/docker/overlay2",
                    "free_space": "210 MB remaining",
                    "deployments_blocked": 84,
                    "largest_file": "sha256_production_base_v3.tar (14.2GB)",
                    "sub_type": "core_dump",
                    "notes": "Docker storage full! 84 production deployments blocked. Blind 'docker system prune -a' will destroy active base images and rollback tags. Snapshot to AWS ECR required."
                }
                cursor.execute("UPDATE system_metrics SET value = 99.3, status = 'CRITICAL' WHERE metric_key = 'disk_usage_pct'")
            else:
                title = "DevOpsCorp Warning: Developer Build Cache & Gradle/NPM Artifact High-Water Mark (86.4%)"
                server_node = "builder-node-02"
                severity = "WARN"
                telemetry = {
                    "disk_usage": "86.4%",
                    "partition": "/var/cache/build_artifacts",
                    "free_space": "18.4 GB remaining",
                    "sub_type": "logs",
                    "notes": "Build artifact cache reached high-water mark. Safe to purge unreferenced dependencies older than 7 days to reclaim 32GB."
                }
                cursor.execute("UPDATE system_metrics SET value = 86.4, status = 'WARN' WHERE metric_key = 'disk_usage_pct'")

        elif fault_type == "worker_stuck":
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                title = "DevOpsCorp Uncritical: Static Code Linter & AST Syntax Analyzer Soft Memory Recycle (25,000 Commits)"
                server_node = "code-linter-daemon-04"
                severity = "LOW"
                telemetry = {
                    "worker_id": "code-linter-daemon-04 (PID 8192)",
                    "last_heartbeat": "1s ago (ACTIVE)",
                    "commits_analyzed": 25000,
                    "is_uncritical": True,
                    "notes": "Worker fully healthy. Soft memory reload during nightly sprint lull. Zero developer interruption."
                }
                cursor.execute("UPDATE system_metrics SET value = 1.0, status = 'OK' WHERE metric_key = 'worker_status'")
            elif sub_type in ["db_exhaustion", "critical_worker"]:
                title = "DevOpsCorp Critical: GitOps Terraform Cloud Sync Controller Threadlock (48 Active Microservice Rollouts!)"
                server_node = "gitops-controller-pool"
                severity = "CRITICAL"
                telemetry = {
                    "worker_id": "gitops-sync-controller (PID 9102)",
                    "last_heartbeat": "380s ago (DEADLOCKED)",
                    "active_rollouts": 48,
                    "sub_type": "db_exhaustion",
                    "notes": "GitOps controller deadlocked during 48 live microservice rollouts! Blind kill causes split-brain Terraform cloud state and orphaned Kubernetes pods. Principal SRE sign-off required."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.0, status = 'CRITICAL' WHERE metric_key = 'worker_status'")
            else:
                title = "DevOpsCorp Warning: Enterprise Slack / Jira CI/CD Notification Webhook Worker Stalled (260s)"
                server_node = "slack-jira-notifier-02"
                severity = "WARN"
                telemetry = {
                    "worker_id": "slack-jira-notifier-02 (PID 6310)",
                    "last_heartbeat": "260s ago",
                    "sub_type": "deadlock_clean",
                    "notes": "Worker hung on external Slack webhook rate limit socket. Safe to restart with automated event requeue."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.5, status = 'WARN' WHERE metric_key = 'worker_status'")

        elif fault_type == "queue_growth":
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                title = "DevOpsCorp Uncritical: Engineering DORA Metrics Analytics Batch Queue Ripple (580 msgs)"
                server_node = "kafka-devops-telemetry"
                severity = "LOW"
                telemetry = {
                    "queue_name": "engineering.dora.metrics",
                    "queue_depth": 580,
                    "consumer_error_rate": "0.0%",
                    "is_uncritical": True,
                    "notes": "Clean evening analytics ripple well within SLA thresholds (<1,000 msgs). Auto-handled silently."
                }
                cursor.execute("UPDATE system_metrics SET value = 580.0, status = 'OK' WHERE metric_key = 'queue_backlog_depth'")
            elif sub_type in ["poison_pill", "critical_queue"]:
                title = "DevOpsCorp Critical: OpenTelemetry Distributed Trace Kafka Ingress Crash Loop (172,000 msgs - 91.5% Err)"
                server_node = "kafka-otel-ingress"
                severity = "CRITICAL"
                telemetry = {
                    "queue_name": "otel.traces.ingress",
                    "queue_depth": 172000,
                    "consumer_error_rate": "91.5%",
                    "sub_type": "poison_pill",
                    "notes": "Malformed OpenTelemetry span JSON payload crashing all collector pods in infinite loops. Scaling pods burns $4,200/hr compute with 0 progress! Quarantining bad offset required."
                }
                cursor.execute("UPDATE system_metrics SET value = 172000.0, status = 'CRITICAL' WHERE metric_key = 'queue_backlog_depth'")
            else:
                title = "DevOpsCorp Warning: GitHub Enterprise Pull Request Merge Webhook Queue Backlog (38,000 msgs)"
                server_node = "kafka-github-webhooks"
                severity = "HIGH"
                telemetry = {
                    "queue_name": "github.pr.merges",
                    "queue_depth": 38000,
                    "consumer_error_rate": "0.01%",
                    "active_pods": 3,
                    "sub_type": "traffic_surge",
                    "notes": "End-of-sprint code freeze rush. Safe to autoscale webhook consumers from 3 to 9 pods within policy ceiling (max 10)."
                }
                cursor.execute("UPDATE system_metrics SET value = 38000.0, status = 'WARN' WHERE metric_key = 'queue_backlog_depth'")

        elif fault_type == "ssl_expiry":
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                title = "DevOpsCorp Uncritical: Internal Kubernetes Istio Service Mesh Mutual TLS (mTLS) Audit (60.0 Days)"
                server_node = "cluster.local"
                severity = "INFO"
                telemetry = {
                    "domain": "cluster.local",
                    "days_remaining": 60.0,
                    "is_uncritical": True,
                    "notes": "Proactive cryptographic handshake and cipher suite audit on internal microservice mTLS sidecars."
                }
                cursor.execute("UPDATE system_metrics SET value = 60.0, status = 'OK' WHERE metric_key = 'ssl_cert_days'")
            elif sub_type in ["root_ca_broken", "critical_ssl"]:
                title = "DevOpsCorp Critical: Corporate Single Sign-On (SSO / Okta SAML) Ingress TLS Expiring in 3 Hours (15,000 Engineers Locked Out!)"
                server_node = "sso.corp-it.internal"
                severity = "CRITICAL"
                telemetry = {
                    "domain": "sso.corp-it.internal",
                    "hours_remaining": 3.0,
                    "days_remaining": 0.12,
                    "sub_type": "root_ca_broken",
                    "notes": "15,000 software engineers will lose access to GitHub, AWS, Jira & Slack in 3 hours! HashiCorp Vault root CA revoked upstream. Immediate CISO sign-off required."
                }
                cursor.execute("UPDATE system_metrics SET value = 0.12, status = 'CRITICAL' WHERE metric_key = 'ssl_cert_days'")
            else:
                title = "DevOpsCorp Warning: Staging Kubernetes Cluster Wildcard Ingress TLS Certificate Expiring (4.1 Days)"
                server_node = "*.staging.corp-it.io"
                severity = "WARN"
                telemetry = {
                    "domain": "*.staging.corp-it.io",
                    "days_remaining": 4.1,
                    "sub_type": "routine_renew",
                    "notes": "Automated certbot DNS-01 challenge ready. Safe for automated certificate rotation and ingress nginx reload."
                }
                cursor.execute("UPDATE system_metrics SET value = 4.1, status = 'WARN' WHERE metric_key = 'ssl_cert_days'")
'''

if 'active_preset in ["it_sector", "it"]' not in app_code:
    # Insert right above PRESET 1: E-COMMERCE
    needle = '# PRESET 1: E-COMMERCE'
    app_code = app_code.replace(needle, it_fault_injection + "\n    " + needle)

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(app_code)

print("Updated app.py with IT Sector integration!")

# =========================================================================
# 2. UPDATE ai_engine.py
# =========================================================================
with open(AI_ENGINE_PATH, "r", encoding="utf-8") as f:
    ai_code = f.read()

it_ai_logic = '''    # =========================================================================
    # IT SECTOR & DEVOPS CLOUD (DEVOPSCORP)
    # =========================================================================
    if active_preset in ["it_sector", "it"]:
        if fault_type == "disk_overflow":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "logs"))
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                return {
                    "root_cause": "Uncritical routine hygiene: Stale CI unit test report XML and SonarQube scratch files in /tmp/ci_test_scratch (49.6% disk usage).",
                    "ai_reasoning": "UNCRITICAL ROUTINE HYGIENE (Runbook IT-DISK-UNC): Telemetry confirms disk utilization is healthy (49.6%, 135GB free). System performs proactive off-peak pruning of test report XML files older than 14 days. Blast radius is strictly zero. 100% safe for autonomous background execution without alerting on-call DevOps engineers.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Ephemeral JUnit test reports and coverage heatmaps older than 14 days. Zero active build or production impact.",
                    "requires_human_approval": 0,
                    "proposed_action": "Purge stale JUnit XML test report scratch files older than 14 days silently to reclaim 16 GB storage.",
                    "remediation_command": "find /tmp/ci_test_scratch -type f -name '*.xml' -mtime +14 -delete",
                    "rollback_command": "touch /tmp/ci_test_scratch/.maintenance_complete",
                    "verification_check": "df -h /tmp/ci_test_scratch | awk 'NR==2 {print \\\"PASS_DISK_HEALTHY\\\"}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["core_dump", "critical_disk"] or telemetry.get("deployments_blocked", 0) > 0 or "docker" in str(telemetry).lower():
                return {
                    "root_cause": "CRITICAL DOCKER REGISTRY STORAGE FULL (99.3% Capacity - 210MB Left!): Partition /var/lib/docker/overlay2 full; 84 production software releases blocked.",
                    "ai_reasoning": "RUNBOOK IT-DISK-CRIT VIOLATION PREVENTED: If docker images are pruned blindly with 'docker system prune -a', active production base image layers and rollback tags will be destroyed, crashing live containers! Senior DevOps guardrails halt execution and mandate Human Authorization to snapshot production release tags to AWS ECR / Google Artifact Registry first.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: 84 enterprise production software deployments and container daemon stability across all CI/CD runner nodes.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze container image pruning, sync production image tags to AWS ECR cold registry, and mandate Principal SRE Authorization before cleaning unused dangling layers.",
                    "remediation_command": "aws ecr sync-images /var/lib/docker/production-tags/ && docker image prune --filter 'until=72h' --force",
                    "rollback_command": "docker pull registry.corp-it.internal:5000/base-images/production:v3.2.0",
                    "verification_check": "df -h /var/lib/docker | awk 'NR==2 {gsub(\\\"%\\\", \\\"\\\"); if ($5 < 85) print \\\"PASS\\\"; else print \\\"FAIL\\\"}'",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Developer build cache partition /var/cache/build_artifacts reached 86.4% capacity.",
                    "ai_reasoning": "Standard rotatable build artifact pattern verified against Runbook IT-DISK-WARN. Telemetry confirms files are purely intermediate compiler outputs and cached NPM/Maven tarballs older than 7 days. Safe for autonomous pruning.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Local builder temporary cache only. Zero production service downtime.",
                    "requires_human_approval": 0,
                    "proposed_action": "Purge unreferenced dependency tarballs and build cache objects older than 7 days to reclaim 32 GB storage.",
                    "remediation_command": "find /var/cache/build_artifacts/ -name '*.tar.gz' -mtime +7 -delete && journalctl --vacuum-time=2d",
                    "rollback_command": "touch /var/cache/build_artifacts/.cache_rebuild_ready",
                    "verification_check": "df -h /var/cache/build_artifacts | awk 'NR==2 {gsub(\\\"%\\\", \\\"\\\"); if ($5 < 75) print \\\"PASS\\\"; else print \\\"FAIL\\\"}'",
                    "is_ambiguous": False
                }

        elif fault_type == "worker_stuck":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "db_exhaustion"))
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                return {
                    "root_cause": "Uncritical worker maintenance: code-linter-daemon-04 has analyzed 25,000 commits; minor AST memory heap fragmentation detected.",
                    "ai_reasoning": "UNCRITICAL PREVENTIVE RECYCLE (Runbook IT-WORKER-UNC): Worker is fully alive and functioning normally. Triggering soft memory reload during nightly sprint lull between code pull requests. Zero downtime, zero human disturbance.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Soft reload occurs between code review linting batches. Production CI pipelines unaffected.",
                    "requires_human_approval": 0,
                    "proposed_action": "Execute soft reload on code linter daemon to compact Python/Go memory heap during task lull.",
                    "remediation_command": "systemctl reload-or-restart celery-worker@code-linter-daemon-04.service",
                    "rollback_command": "systemctl status celery-worker@code-linter-daemon-04.service",
                    "verification_check": "systemctl is-active celery-worker@code-linter-daemon-04.service",
                    "is_ambiguous": False
                }
            elif sub_type in ["db_exhaustion", "critical_worker"] or telemetry.get("active_rollouts", 0) > 0:
                return {
                    "root_cause": "CRITICAL GITOPS TERRAFORM SYNC THREADLOCK: gitops-sync-controller (PID 9102) locked with 48 active microservice rollouts in-flight!",
                    "ai_reasoning": "RUNBOOK IT-WORKER-CRIT SAFETY GATE: Terminating this process blindly causes split-brain cloud state, orphaned AWS infrastructure resources, and broken Kubernetes deployments! System halts execution and mandates Principal DevOps sign-off to safely unlock DynamoDB state before service cycling.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: 48 live production microservice Kubernetes deployments + cloud infrastructure Terraform state lock.",
                    "requires_human_approval": 1,
                    "proposed_action": "Verify DynamoDB lock status, drain in-flight rollouts safely, and require Principal DevOps Authorization before restarting controller.",
                    "remediation_command": "terraform force-unlock -force 8a2f-109b-c43e && systemctl restart gitops-sync-controller.service",
                    "rollback_command": "systemctl restart gitops-sync-controller.service",
                    "verification_check": "systemctl is-active gitops-sync-controller.service",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Slack / Jira CI/CD notification webhook worker slack-jira-notifier-02 stalled (260s heartbeat delay).",
                    "ai_reasoning": "Isolated socket timeout verified against Runbook IT-WORKER-WARN. Worker hung on external Slack webhook rate limits. Zero production code deployment risk. Safe to restart with automatic event backoff and retry.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Developer notification channel only. Zero production software deployment risk.",
                    "requires_human_approval": 0,
                    "proposed_action": "Gracefully restart stalled Slack/Jira notification worker and retry queued webhook payloads.",
                    "remediation_command": "systemctl restart celery-worker@slack-jira-notifier-02.service",
                    "rollback_command": "systemctl restart celery-worker@slack-jira-notifier-02-fallback.service",
                    "verification_check": "systemctl is-active celery-worker@slack-jira-notifier-02.service",
                    "is_ambiguous": False
                }

        elif fault_type == "queue_growth":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "poison_pill"))
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                return {
                    "root_cause": "Uncritical queue balancing: Engineering DORA metrics analytics queue has minor evening ripple (580 msgs).",
                    "ai_reasoning": "UNCRITICAL QUEUE BALANCING (Runbook IT-QUEUE-UNC): Telemetry indicates clean DORA analytics traffic well within SLA thresholds (<1,000 msgs). Auto-handled silently by spinning up 1 standby consumer container.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Developer velocity metrics only. Sub-150ms processing SLA maintained.",
                    "requires_human_approval": 0,
                    "proposed_action": "Scale DORA metrics consumer pods from 2 to 3 to maintain sub-150ms SLA.",
                    "remediation_command": "kubectl scale deployment/dora-consumer --replicas=3 --namespace=ci",
                    "rollback_command": "kubectl scale deployment/dora-consumer --replicas=2 --namespace=ci",
                    "verification_check": "kubectl get deployment/dora-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["poison_pill", "critical_queue"] or float(str(telemetry.get("consumer_error_rate", "0")).replace("%", "")) > 50.0:
                return {
                    "root_cause": "CRITICAL OPENTELEMETRY TRACE KAFKA CRASH LOOP (172,000 msgs - 91.5% Err): Malformed OpenTelemetry span JSON crashing collector pods.",
                    "ai_reasoning": "RUNBOOK IT-QUEUE-CRIT SAFETY GATE: Scaling collector pods will spawn pods that immediately crash in infinite loops, burning compute budget ($4,200/hr) with zero progress! System halts autoscaling and mandates Human Authorization to isolate corrupt trace offset to Dead Letter Queue (DLQ).",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "HIGH: Enterprise observability pipeline and Kubernetes cluster node compute capacity.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze pod autoscaling, isolate corrupt offset 602819 to Observability DLQ, and require Human Authorization.",
                    "remediation_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group otel-collectors --topic otel.traces.ingress --reset-offsets --to-offset 602819 --execute",
                    "rollback_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group otel-collectors --topic otel.traces.ingress --reset-offsets --to-offset 602818 --execute",
                    "verification_check": "echo PASS_DLQ_ROUTED",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: GitHub Enterprise pull request merge webhook queue influx (38,000 msgs, error rate 0.01%).",
                    "ai_reasoning": "Healthy throughput verified against Runbook IT-QUEUE-WARN. Error rate < 0.05% indicates clean sprint code freeze merge rush. Safe to autoscale from 3 to 9 pods within policy limit (max 10).",
                    "risk_tier": "Tier 2 (Guarded Auto - Within Policy Limits)",
                    "blast_radius_desc": "MEDIUM: GitHub webhook consumers. Capped at policy ceiling of 10 pods to prevent compute cost overruns.",
                    "requires_human_approval": 0,
                    "proposed_action": "Autoscale GitHub webhook consumer deployment from 3 to 9 replicas within policy limits.",
                    "remediation_command": "kubectl scale deployment/github-webhook-consumer --replicas=9 --namespace=ci",
                    "rollback_command": "kubectl scale deployment/github-webhook-consumer --replicas=3 --namespace=ci",
                    "verification_check": "kubectl get deployment/github-webhook-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }

        elif fault_type == "ssl_expiry":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "routine_renew"))
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                return {
                    "root_cause": "Uncritical certificate health check: Kubernetes Istio service mesh internal mTLS certificate has 60.0 days remaining.",
                    "ai_reasoning": "UNCRITICAL CRYPTOGRAPHIC AUDIT (Runbook IT-SSL-UNC): Certificate validity is healthy (60 days remaining). Proactive cipher suite and proxy secret verification executed. System 100% operational.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
                    "blast_radius_desc": "ZERO (0%): Read-only cryptographic handshake validation probe. Zero configuration modifications.",
                    "requires_human_approval": 0,
                    "proposed_action": "Perform read-only cryptographic validation probe across Istio service mesh sidecars.",
                    "remediation_command": "istioctl proxy-config secret deployment/ingressgateway.istio-system && echo 'AUDIT_VERIFIED_VALID'",
                    "rollback_command": "echo 'AUDIT_NOOP'",
                    "verification_check": "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/istio-mtls.crt",
                    "is_ambiguous": False
                }
            elif sub_type in ["root_ca_broken", "critical_ssl"] or float(telemetry.get("hours_remaining", 99)) < 12.0:
                return {
                    "root_cause": "CRITICAL SINGLE SIGN-ON (SSO / OKTA SAML) INGRESS TLS EXPIRES IN 3 HOURS: HashiCorp Vault root CA revoked upstream!",
                    "ai_reasoning": "RUNBOOK IT-SSL-CRIT SAFETY GATE: In 3 hours, 15,000 enterprise software engineers will lose access to GitHub, AWS, Jira & Slack! Automated ACME renewals will fail due to revoked Vault intermediate authority. Mandates immediate escalation to Enterprise CISO.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Enterprise Identity & Access Management (IAM) for 15,000 corporate software engineers and operations personnel.",
                    "requires_human_approval": 1,
                    "proposed_action": "Halt automated renewal loop, import updated trusted HashiCorp Vault root CA bundle, and require Enterprise CISO Authorization.",
                    "remediation_command": "vault write auth/cert/config certificate=@/etc/ssl/certs/vault-root-renewed.crt && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good_sso.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl verify -CAfile /etc/ssl/certs/vault-root.crt /etc/ssl/certs/sso.corp-it.internal.crt",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Staging Kubernetes cluster wildcard ingress TLS certificate expiring in 4.1 days.",
                    "ai_reasoning": "Valid certificate renewal window verified against Runbook IT-SSL-WARN. Automated ACME DNS-01 challenge ready. Safe for autonomous key rotation and seamless ingress nginx reload.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Staging microservices ingress only. Seamless zero-downtime configuration reload.",
                    "requires_human_approval": 0,
                    "proposed_action": "Execute automated certbot DNS-01 TLS certificate renewal and reload ingress nginx reverse proxy.",
                    "remediation_command": "certbot renew --cert-name staging.corp-it.io --preferred-challenges dns-01 --quiet && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good_staging.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/staging.corp-it.io.crt",
                    "is_ambiguous": False
                }
'''

if 'active_preset in ["it_sector", "it"]' not in ai_code:
    needle_ai = '# 1. QUICKCART E-COMMERCE'
    ai_code = ai_code.replace(needle_ai, it_ai_logic + "\n    " + needle_ai)

with open(AI_ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(ai_code)

print("Updated ai_engine.py with IT Sector intelligence!")

# =========================================================================
# 3. UPDATE templates/index.html
# =========================================================================
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Add IT Sector button to Section 2 Switcher Bar
it_btn_html = '<button id="btnPreset-it_sector" onclick="loadDatasetPreset(\'it_sector\')" class="px-2.5 py-1.5 rounded-lg border border-cyber-border hover:border-emerald-500 text-slate-300 hover:text-white transition flex items-center gap-1.5 font-bold" title="Switch to DevOpsCorp Enterprise IT & Cloud Infrastructure">\n            💻 DevOpsCorp (IT Sector: 99.3% / 48 GitOps)\n          </button>\n          '

if 'id="btnPreset-it_sector"' not in html:
    html = html.replace('<button id="btnPreset-ecommerce"', it_btn_html + '<button id="btnPreset-ecommerce"')

# Add IT Sector Card in uploadDatabaseModal
it_modal_card = '''            <!-- Card 0: DevOpsCorp Enterprise IT Sector -->
            <div class="p-3 rounded-xl bg-[#070b14] border border-emerald-500/40 hover:border-emerald-400 transition flex flex-col justify-between space-y-2.5 shadow-lg">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="font-bold text-emerald-300 text-xs flex items-center gap-1.5">
                    💻 DevOpsCorp IT Sector
                  </span>
                  <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">12 Runbooks</span>
                </div>
                <div class="text-[10px] text-slate-400 mb-2">Enterprise DevOps, Kubernetes & Cloud SaaS</div>
                <div class="space-y-1 text-[10px] font-mono">
                  <div class="text-rose-400">🔴 Docker Registry: 99.3% (210MB left)</div>
                  <div class="text-rose-400">🔴 GitOps: 48 Rollouts Locked</div>
                  <div class="text-rose-400">🔴 OpenTelemetry: 172,000 msgs (91% Err)</div>
                  <div class="text-rose-400">🔴 SSO Ingress: 3 Hours Left</div>
                  <div class="text-emerald-400 pt-1 border-t border-slate-800">🟢 CI JUnit Scratch: 49.6% (Uncritical)</div>
                  <div class="text-emerald-400">🟢 DORA Metrics Queue: 580 msgs</div>
                </div>
              </div>
              <div class="space-y-1.5 pt-2 border-t border-slate-800">
                <button type="button" onclick="loadDatasetPreset('it_sector')" class="w-full py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow transition">
                  <i data-lucide="zap" class="w-3.5 h-3.5"></i> Load IT Sector
                </button>
                <div class="flex items-center gap-1 text-[10px] font-mono">
                  <a href="/api/database/download-preset/it_sector" download="DevOpsCorp_ITSector_Dataset.json" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-300 text-center transition">⬇ .JSON</a>
                  <a href="/api/database/download-preset-sql/it_sector" download="DevOpsCorp_ITSector_Schema.sql" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-300 text-center transition">⬇ .SQL</a>
                  <a href="/api/database/download-preset-db/it_sector" download="DevOpsCorp_ITSector.db" class="flex-1 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-300 text-center transition">⬇ .DB</a>
                </div>
              </div>
            </div>

'''

if 'Card 0: DevOpsCorp Enterprise IT Sector' not in html:
    # Change grid to 4 cols on lg and insert card
    html = html.replace('grid grid-cols-1 md:grid-cols-3 gap-3 pt-1', 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2.5 pt-1')
    html = html.replace('<!-- Card 1: QuickCart E-Commerce -->', it_modal_card + '            <!-- Card 1: QuickCart E-Commerce -->')

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html with IT Sector UI!")

# =========================================================================
# 4. UPDATE static/js/app.js
# =========================================================================
with open(APP_JS_PATH, "r", encoding="utf-8") as f:
    app_js = f.read()

# Update titles and presets in app.js
if "'it_sector': 'DevOpsCorp Enterprise IT & Cloud Infrastructure'" not in app_js:
    app_js = app_js.replace(
        "const titles = {\n      'ecommerce': 'QuickCart E-Commerce & Delivery Cloud',",
        "const titles = {\n      'it_sector': 'DevOpsCorp Enterprise IT & Cloud Infrastructure',\n      'ecommerce': 'QuickCart E-Commerce & Delivery Cloud',"
    )
    app_js = app_js.replace(
        "const titles = {\n    'ecommerce': '🛒 QuickCart E-Commerce (98.7% / 3,420 Riders)',",
        "const titles = {\n    'it_sector': '💻 DevOpsCorp IT Sector (99.3% / 48 GitOps)',\n    'ecommerce': '🛒 QuickCart E-Commerce (98.7% / 3,420 Riders)',"
    )
    app_js = app_js.replace(
        "const colors = {\n    'ecommerce': 'bg-amber-500/20 text-amber-300 border-amber-500/30',",
        "const colors = {\n    'it_sector': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',\n    'ecommerce': 'bg-amber-500/20 text-amber-300 border-amber-500/30',"
    )
    app_js = app_js.replace(
        "['ecommerce', 'healthcare', 'fintech'].forEach(p => {",
        "['it_sector', 'ecommerce', 'healthcare', 'fintech'].forEach(p => {"
    )

# Add it_sector buttons text in updateSection2Buttons
it_button_cases = '''  if (presetName === 'it_sector' || presetName === 'it') {
    if (diskUnc) diskUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 CI Test Reports (49.6%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (diskWarn) diskWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Build Artifacts (86.4%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (diskCrit) diskCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Docker Registry (99.3%)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">210MB Left!</span>';
    
    if (workerUnc) workerUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Code Linter GC (25k Commits)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (workerWarn) workerWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Slack/Jira Webhook (260s)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (workerCrit) workerCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 GitOps Terraform Lock (48 Rollouts)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">48 Rollouts!</span>';
    
    if (queueUnc) queueUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 DORA Metrics Ripple (580 msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (queueWarn) queueWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 GitHub Merge Influx (38,000 msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">Scale 3➔9</span>';
    if (queueCrit) queueCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 OpenTelemetry Crash (172k msgs)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">91.5% Err</span>';

    if (sslUnc) sslUnc.innerHTML = '<span class="flex items-center gap-1.5">🟢 Istio Service Mesh mTLS (60d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">Uncritical</span>';
    if (sslWarn) sslWarn.innerHTML = '<span class="flex items-center gap-1.5">🟡 Staging Cluster Ingress (4.1d)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono">Safe Tier 1</span>';
    if (sslCrit) sslCrit.innerHTML = '<span class="flex items-center gap-1.5">🔴 Corporate SSO Ingress (3 Hours!)</span><span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono">15,000 Eng</span>';
  } else '''

if "if (presetName === 'it_sector' || presetName === 'it')" not in app_js:
    app_js = app_js.replace("if (presetName === 'ecommerce') {", it_button_cases + "if (presetName === 'ecommerce') {")

with open(APP_JS_PATH, "w", encoding="utf-8") as f:
    f.write(app_js)

print("Updated app.js with IT Sector support!")
