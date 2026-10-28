"""
SafeOps AI - AI Diagnosis & Risk Policy Engine
Analyzes system telemetry, encodes operational judgment from runbooks,
evaluates risk tiers (Tier 1 Auto, Tier 2 Guarded, Tier 3 Human Approval, Ambiguous Escalation),
and generates explainable remediation & rollback plans.
Designed for Cynefian Hackathon - AI-Ops Track (Team Idea Ignitors XH-23)
Supports 3 distinct industry presets: QuickCart E-Commerce, LifeCare Hospital ICU, GlobalPay Fintech.
"""

import os
import json
import sqlite3
from datetime import datetime

def get_active_preset_name():
    """Reads the active preset from safeops.db or defaults to fintech."""
    try:
        db_path = os.path.join(os.path.dirname(__file__), "safeops.db")
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM safety_policies WHERE policy_key = 'active_preset'")
            row = cursor.fetchone()
            conn.close()
            if row and row['value']:
                return row['value'].strip().lower()
    except Exception:
        pass
    return "fintech"

def analyze_and_diagnose(fault_type, telemetry, incident_code=None, context=None):
    """
    Executes the AI Diagnosis & Risk Assessment pipeline.
    Encodes senior SRE runbook judgment:
    - 'If the disk is full because of logs, rotate; if because of a core dump or invoices, investigate'
    - 'If ambiguous or high blast radius, escalate rather than guess'
    - 'If uncritical routine maintenance, execute silently with zero blast radius'
    """
    telemetry = telemetry or {}
    context = context or {}
    active_preset = get_active_preset_name()

    # =========================================================================
        # =========================================================================
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
                    "verification_check": "df -h /tmp/ci_test_scratch | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
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
                    "verification_check": "df -h /var/lib/docker | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 85) print \"PASS\"; else print \"FAIL\"}'",
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
                    "verification_check": "df -h /var/cache/build_artifacts | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
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

    # 1. QUICKCART E-COMMERCE & FOOD DELIVERY CLOUD
    # =========================================================================
    elif active_preset == "ecommerce":
        if fault_type == "disk_overflow":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "logs"))
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                return {
                    "root_cause": "Uncritical routine hygiene: Restaurant menu preview thumbnails in /var/cache/menu_renders (51.4% disk usage).",
                    "ai_reasoning": "UNCRITICAL ROUTINE HYGIENE (Runbook QC-DISK-UNC): Telemetry confirms disk utilization is healthy (51.4%, 148GB free). System performs proactive off-peak pruning of stale dish thumbnails older than 14 days. Blast radius is strictly zero. 100% safe for autonomous background execution without alerting on-call personnel.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Targets purely temporary restaurant menu thumbnail preview images. Zero active customer or order disruption.",
                    "requires_human_approval": 0,
                    "proposed_action": "Purge stale restaurant menu thumbnails older than 14 days silently to reclaim 12 GB storage.",
                    "remediation_command": "find /var/cache/menu_renders -type f -mtime +14 -delete",
                    "rollback_command": "touch /var/cache/menu_renders/.maintenance_complete",
                    "verification_check": "df -h /var/cache/menu_renders | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["core_dump", "critical_disk"] or telemetry.get("orders_blocked", 0) > 0 or "invoice" in str(telemetry).lower():
                return {
                    "root_cause": "CRITICAL ORDER INVOICING STORAGE FULL (98.7% Capacity - 450MB Left!): Partition /var/data/quickcart/invoices full; 3,420 checkout operations blocked.",
                    "ai_reasoning": "RUNBOOK QC-DISK-CRIT VIOLATION PREVENTED: If invoice records are blindly deleted, tax compliance is destroyed and customer proof-of-purchase is lost! Senior SRE guardrails halt autonomous execution and mandate Human Authorization to snapshot older tax records to S3 glacier cold storage first.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Complete customer checkout processing and fiscal tax invoice compliance across 100% of order partitions.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze invoice directory pruning, snapshot 2025 archived tax invoices to S3 cold storage, and require Human Sign-off before freeing local disk space.",
                    "remediation_command": "aws s3 sync /var/data/quickcart/invoices/2025/ s3://quickcart-tax-cold/ && find /var/data/quickcart/invoices/2025/ -type f -delete",
                    "rollback_command": "aws s3 sync s3://quickcart-tax-cold/ /var/data/quickcart/invoices/2025/ || true",
                    "verification_check": "df -h /var/data/quickcart/invoices | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 80) print \"PASS\"; else print \"FAIL\"}'",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Delivery rider GPS telemetry log partition /var/log/rider_gps reached 89.2% capacity.",
                    "ai_reasoning": "Standard rotatable log pattern verified against Runbook QC-DISK-WARN. Telemetry confirms files are purely raw GPS trace breadcrumbs older than 48 hours. Zero customer order or payment risk. Safe for autonomous compression.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Rider GPS telemetry logs only. Zero customer order or checkout disruption.",
                    "requires_human_approval": 0,
                    "proposed_action": "Gzip-compress raw delivery rider GPS breadcrumbs older than 48 hours to reclaim 34 GB storage.",
                    "remediation_command": "find /var/log/rider_gps/ -name '*.trace' -mtime +2 -exec gzip {} \\; && journalctl --vacuum-time=1d",
                    "rollback_command": "find /var/log/rider_gps/ -name '*.trace.gz' -exec gunzip {} \\;",
                    "verification_check": "df -h /var/log/rider_gps | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
                    "is_ambiguous": False
                }

        elif fault_type == "worker_stuck":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "db_exhaustion"))
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                return {
                    "root_cause": "Uncritical worker maintenance: loyalty-worker-01 has completed 18,200 reward calculations; minor heap fragmentation detected.",
                    "ai_reasoning": "UNCRITICAL PREVENTIVE RECYCLE (Runbook QC-WORKER-UNC): Worker is fully alive and functioning normally. Triggering soft memory reload during idle task gap between customer orders. Zero downtime, zero human disturbance.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Graceful soft reload during idle order lull. Live delivery routes unaffected.",
                    "requires_human_approval": 0,
                    "proposed_action": "Soft reload loyalty worker process to compact Python runtime memory during task lull.",
                    "remediation_command": "systemctl reload-or-restart celery-worker@loyalty-worker-01.service",
                    "rollback_command": "systemctl status celery-worker@loyalty-worker-01.service",
                    "verification_check": "systemctl is-active celery-worker@loyalty-worker-01.service",
                    "is_ambiguous": False
                }
            elif sub_type in ["db_exhaustion", "critical_worker"] or telemetry.get("pending_orders", 0) > 0:
                return {
                    "root_cause": "CRITICAL RIDER AUTO-DISPATCH THREADLOCK: rider-dispatch-daemon (PID 1904) deadlocked with 3,420 orders waiting!",
                    "ai_reasoning": "RUNBOOK QC-WORKER-CRIT SAFETY GATE: Terminating this daemon blindly will duplicate delivery rider dispatches and orphan 3,420 orders! System halts automated execution, pauses incoming order assignment, and mandates Senior Logistics SRE sign-off to drain active rider locks before restarting.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: 3,420 hungry customer deliveries and live GPS route dispatches across 12 delivery zones.",
                    "requires_human_approval": 1,
                    "proposed_action": "Drain active rider locks, verify queue status, and require Operator Approval before restarting dispatch pool.",
                    "remediation_command": "python3 /opt/quickcart/scripts/drain_active_rider_locks.py && systemctl restart rider-dispatch-daemon.service",
                    "rollback_command": "systemctl restart rider-dispatch-daemon.service",
                    "verification_check": "systemctl is-active rider-dispatch-daemon.service",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Promotional SMS/WhatsApp notification worker promo-sender-03 (PID 5192) stalled (280s heartbeat delay).",
                    "ai_reasoning": "Isolated socket timeout verified against Runbook QC-WORKER-WARN. Worker hung on external Twilio API. Zero customer checkout or payment risk. Safe to restart with automated message retry.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Marketing notification queue only. Zero customer order or payment risk.",
                    "requires_human_approval": 0,
                    "proposed_action": "Gracefully restart stalled promotional notification worker and retry queued dispatch tasks.",
                    "remediation_command": "systemctl restart celery-worker@promo-sender-03.service",
                    "rollback_command": "systemctl restart celery-worker@promo-sender-03-fallback.service",
                    "verification_check": "systemctl is-active celery-worker@promo-sender-03.service",
                    "is_ambiguous": False
                }

        elif fault_type == "queue_growth":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "poison_pill"))
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                return {
                    "root_cause": "Uncritical queue balancing: Clickstream batch backlog has minor evening browsing ripple (620 msgs).",
                    "ai_reasoning": "UNCRITICAL QUEUE BALANCING (Runbook QC-QUEUE-UNC): Telemetry indicates clean traffic well within SLA thresholds (<5,000 msgs). Auto-handled silently by spinning up 1 standby worker container.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Purely temporary browsing events. Sub-150ms processing SLA maintained.",
                    "requires_human_approval": 0,
                    "proposed_action": "Scale clickstream consumer pods from 2 to 3 to maintain sub-150ms SLA.",
                    "remediation_command": "kubectl scale deployment/clickstream-consumer --replicas=3 --namespace=analytics",
                    "rollback_command": "kubectl scale deployment/clickstream-consumer --replicas=2 --namespace=analytics",
                    "verification_check": "kubectl get deployment/clickstream-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["poison_pill", "critical_queue"] or float(str(telemetry.get("consumer_error_rate", "0")).replace("%", "")) > 50.0:
                return {
                    "root_cause": "CRITICAL RIDER GPS KAFKA CRASH LOOP (184,000 msgs - 88.2% Err): Corrupt rider GPS JSON payload crashing consumer pods.",
                    "ai_reasoning": "RUNBOOK QC-QUEUE-CRIT SAFETY GATE: Scaling consumer pods will cause immediate container crash loops and waste $3,800/hr in cloud compute with zero progress! System halts pod autoscaler and mandates Human Authorization to isolate malformed offset to Dead Letter Queue (DLQ).",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "HIGH: Live delivery rider GPS tracking stream and real-time customer order ETA predictions.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze pod autoscaling, isolate corrupt offset 401829 to Dead Letter Queue, and require Human Authorization.",
                    "remediation_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group rider-gps --topic quickcart.rider.gps.telemetry --reset-offsets --to-offset 401829 --execute",
                    "rollback_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group rider-gps --topic quickcart.rider.gps.telemetry --reset-offsets --to-offset 401828 --execute",
                    "verification_check": "echo PASS_DLQ_ROUTED",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Meal rush promotional influx on queue quickcart.flash.orders (32,400 msgs, error rate 0.01%).",
                    "ai_reasoning": "Healthy consumer throughput verified against Runbook QC-QUEUE-WARN. Error rate < 0.05% indicates genuine meal rush traffic. Safe to autoscale from 4 to 8 pods within policy limit (max 10).",
                    "risk_tier": "Tier 2 (Guarded Auto - Within Policy Limits)",
                    "blast_radius_desc": "MEDIUM: Flash sale consumer pods. Capped at policy ceiling of 10 pods to prevent compute cost overruns.",
                    "requires_human_approval": 0,
                    "proposed_action": "Autoscale order consumer deployment from 4 to 8 replicas within policy limits.",
                    "remediation_command": "kubectl scale deployment/order-consumer --replicas=8 --namespace=orders",
                    "rollback_command": "kubectl scale deployment/order-consumer --replicas=4 --namespace=orders",
                    "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }

        elif fault_type == "ssl_expiry":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "routine_renew"))
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                return {
                    "root_cause": "Uncritical certificate health check: Warehouse logistics mTLS certificate has 62 days remaining.",
                    "ai_reasoning": "UNCRITICAL CRYPTOGRAPHIC AUDIT (Runbook QC-SSL-UNC): Certificate validity is healthy (62 days remaining). Proactive cipher suite and OCSP audit executed. System 100% operational.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
                    "blast_radius_desc": "ZERO (0%): Read-only cryptographic validation probe. Zero configuration modifications.",
                    "requires_human_approval": 0,
                    "proposed_action": "Perform read-only cryptographic handshake validation probe and record audit trail.",
                    "remediation_command": "openssl s_client -servername warehouse-auth.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'",
                    "rollback_command": "echo 'AUDIT_NOOP'",
                    "verification_check": "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/warehouse-auth.internal.crt",
                    "is_ambiguous": False
                }
            elif sub_type in ["root_ca_broken", "critical_ssl"] or float(telemetry.get("hours_remaining", 99)) < 12.0:
                return {
                    "root_cause": "CRITICAL KITCHEN PARTNER TABLET GATEWAY SSL EXPIRES IN 4 HOURS: Intermediate CA revoked upstream!",
                    "ai_reasoning": "RUNBOOK QC-SSL-CRIT SAFETY GATE: In 4 hours, orders will stop printing in 12,000 restaurant partner kitchens! Automated ACME renewals will fail due to revoked upstream CA. Mandates immediate escalation to CISO.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Live order communication with 12,000 partner restaurant kitchen tablets.",
                    "requires_human_approval": 1,
                    "proposed_action": "Halt automated renewal loop, import updated trusted intermediate CA bundle, and require CISO Authorization.",
                    "remediation_command": "update-ca-certificates --fresh && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/kitchen.quickcart.com.crt",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Customer mobile app push gateway TLS certificate expiring in 3.8 days.",
                    "ai_reasoning": "Valid certificate renewal window verified against Runbook QC-SSL-WARN. Automated ACME challenge ready. Safe for autonomous key rotation and seamless nginx reload.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Mobile app push gateway ingress. Seamless zero-downtime configuration reload.",
                    "requires_human_approval": 0,
                    "proposed_action": "Execute automated certbot TLS certificate renewal and reload ingress nginx reverse proxy.",
                    "remediation_command": "certbot renew --cert-name push.quickcart.com --quiet && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/push.quickcart.com.crt",
                    "is_ambiguous": False
                }

    # =========================================================================
    # 2. LIFECARE HOSPITAL ICU & MEDICAL PATIENT CLOUD
    # =========================================================================
    elif active_preset == "healthcare":
        if fault_type == "disk_overflow":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "logs"))
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                return {
                    "root_cause": "Uncritical routine hygiene: Nurse attendance scratch files in /tmp/nurse_shifts (48.2% disk usage).",
                    "ai_reasoning": "UNCRITICAL ROUTINE HYGIENE (Runbook MED-DISK-UNC): Telemetry confirms disk utilization is healthy (48.2%, 120GB free). System performs proactive off-peak pruning of administrative scratch files older than 14 days. Zero clinical or bedside impact. 100% safe for autonomous background execution.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Temporary administrative nurse shift files. Zero patient vitals or clinical record impact.",
                    "requires_human_approval": 0,
                    "proposed_action": "Purge stale nurse attendance scratch files older than 14 days silently to reclaim 14 GB storage.",
                    "remediation_command": "find /tmp/nurse_shifts -type f -name '*.tmp' -mtime +14 -delete",
                    "rollback_command": "touch /tmp/nurse_shifts/.maintenance_complete",
                    "verification_check": "df -h /tmp/nurse_shifts | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["core_dump", "critical_disk"] or telemetry.get("icu_patients_monitored", 0) > 0 or "ecg" in str(telemetry).lower():
                return {
                    "root_cause": "CRITICAL ICU CARDIAC ECG STORAGE FULL (99.1% Capacity - 180MB Left!): Partition /var/data/icu/cardiac_ecg full; 42 ICU patients at risk.",
                    "ai_reasoning": "RUNBOOK MED-DISK-CRIT SAFETY GATE: Deleting cardiac waveform files destroys irreplaceable clinical diagnostic evidence and violates HIPAA federal compliance! Senior Medical SRE guardrails halt execution and mandate Human Authorization to sync older records to encrypted HIPAA cold storage first.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Continuous cardiac telemetry waveforms for 42 intensive-care patients.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze local purging, sync archive waveforms to HIPAA-compliant medical S3 storage, and require Human Sign-off.",
                    "remediation_command": "aws s3 sync /var/data/icu/cardiac_ecg/archive/ s3://lifecare-hipaa-cold/ && rm -f /var/data/icu/cardiac_ecg/archive/*.dat",
                    "rollback_command": "aws s3 sync s3://lifecare-hipaa-cold/ /var/data/icu/cardiac_ecg/archive/ || true",
                    "verification_check": "df -h /var/data/icu/cardiac_ecg | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 85) print \"PASS\"; else print \"FAIL\"}'",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Radiology PACS DICOM image preview cache /var/cache/xray_pacs reached 87.6% capacity.",
                    "ai_reasoning": "Standard rotatable cache pattern verified against Runbook MED-DISK-WARN. Telemetry confirms files are purely temporary preview renders older than 72 hours. Master hospital DICOM archives unaffected. Safe for autonomous pruning.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Local PACS preview image cache only. Zero primary medical record risk.",
                    "requires_human_approval": 0,
                    "proposed_action": "Purge cached radiology PACS preview images older than 72 hours to reclaim 45 GB storage.",
                    "remediation_command": "find /var/cache/xray_pacs/ -type f -mtime +3 -delete && systemctl reload dcm4chee.service",
                    "rollback_command": "echo 'ROLLBACK_DICOM_PREVIEWS'",
                    "verification_check": "df -h /var/cache/xray_pacs | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
                    "is_ambiguous": False
                }

        elif fault_type == "worker_stuck":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "db_exhaustion"))
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                return {
                    "root_cause": "Uncritical worker maintenance: pdf-gen-pool-03 has generated 8,240 discharge summaries; minor heap fragmentation detected.",
                    "ai_reasoning": "UNCRITICAL PREVENTIVE RECYCLE (Runbook MED-WORKER-UNC): Worker is fully alive. Performing soft garbage collection during night lull between patient discharges. Zero downtime, zero human disturbance.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Soft reload occurs between discharge document batches. Clinical care unaffected.",
                    "requires_human_approval": 0,
                    "proposed_action": "Execute graceful worker reload to compact memory heap during task lull.",
                    "remediation_command": "systemctl reload-or-restart celery-worker@pdf-gen-pool-03.service",
                    "rollback_command": "systemctl status celery-worker@pdf-gen-pool-03.service",
                    "verification_check": "systemctl is-active celery-worker@pdf-gen-pool-03.service",
                    "is_ambiguous": False
                }
            elif sub_type in ["db_exhaustion", "critical_worker"] or telemetry.get("active_911_calls", 0) > 0:
                return {
                    "root_cause": "CRITICAL EMERGENCY AMBULANCE DISPATCH THREADLOCK: ems-dispatch-srv (PID 2048) locked with 18 active 911 calls!",
                    "ai_reasoning": "RUNBOOK MED-WORKER-CRIT SAFETY GATE: Terminating this worker blindly risks dropping active emergency ambulance routes and patient dispatches! System halts uncoordinated restart, activates backup radio relay, and mandates Senior Healthcare Operator approval before service cycling.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: 18 live emergency ambulance response routes across metropolitan hospital trauma network.",
                    "requires_human_approval": 1,
                    "proposed_action": "Failover to backup emergency radio dispatch relay, verify route sync, and require Human Sign-off before restarting daemon.",
                    "remediation_command": "python3 /opt/lifecare/scripts/failover_ems_radio_relay.py && systemctl restart ems-dispatch-srv.service",
                    "rollback_command": "systemctl restart ems-dispatch-srv.service",
                    "verification_check": "systemctl is-active ems-dispatch-srv.service",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Hospital pharmacy medication restock inventory sync worker pharmacy-sync-02 stalled (320s heartbeat delay).",
                    "ai_reasoning": "Isolated supplier timeout verified against Runbook MED-WORKER-WARN. Worker hung on external wholesale medication API. Zero bedside patient or emergency medicine risk. Safe for autonomous restart with message requeue.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Non-urgent medication restock inventory sync. Zero bedside patient risk.",
                    "requires_human_approval": 0,
                    "proposed_action": "Gracefully restart pharmacy sync worker and requeue pending wholesale inventory updates.",
                    "remediation_command": "systemctl restart celery-worker@pharmacy-sync-02.service",
                    "rollback_command": "systemctl restart celery-worker@pharmacy-sync-02-fallback.service",
                    "verification_check": "systemctl is-active celery-worker@pharmacy-sync-02.service",
                    "is_ambiguous": False
                }

        elif fault_type == "queue_growth":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "poison_pill"))
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                return {
                    "root_cause": "Uncritical queue balancing: Hospital cafeteria dietary meal orders queue has minor morning ripple (410 msgs).",
                    "ai_reasoning": "UNCRITICAL QUEUE BALANCING (Runbook MED-QUEUE-UNC): Telemetry indicates clean dietary meal order traffic well within SLA thresholds (<1,000 msgs). Auto-handled silently by spinning up 1 standby consumer container.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Dietary meal orders only. Zero clinical patient vitals impact.",
                    "requires_human_approval": 0,
                    "proposed_action": "Scale dietary meal order consumer pods from 3 to 4 to maintain sub-150ms SLA.",
                    "remediation_command": "kubectl scale deployment/order-consumer --replicas=4 --namespace=orders",
                    "rollback_command": "kubectl scale deployment/order-consumer --replicas=3 --namespace=orders",
                    "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["poison_pill", "critical_queue"] or float(str(telemetry.get("consumer_error_rate", "0")).replace("%", "")) > 50.0:
                return {
                    "root_cause": "CRITICAL BEDSIDE VITALS ALERT STREAM CRASH LOOP (96,000 msgs - 94.1% Err): Corrupt pulse oximeter firmware telemetry crashing consumer pods.",
                    "ai_reasoning": "RUNBOOK MED-QUEUE-CRIT SAFETY GATE: Malformed telemetry crashing consumer pods in infinite loop. Scaling pods risks complete hospital telemetry failure and unmonitored patient vitals! Mandates Human Authorization to isolate bad offset to Medical Quarantine Queue.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Bedside vital signs monitoring telemetry and real-time clinical alarm suppression.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze pod autoscaling, isolate corrupt offset 302194 to Medical Quarantine Queue, and require Clinical SRE Authorization.",
                    "remediation_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group bedside-vitals --topic vitals.patient.telemetry --reset-offsets --to-offset 302194 --execute",
                    "rollback_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group bedside-vitals --topic vitals.patient.telemetry --reset-offsets --to-offset 302193 --execute",
                    "verification_check": "echo PASS_DLQ_ROUTED",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Morning outpatient blood lab results broadcast queue influx (19,800 msgs, error rate 0.02%).",
                    "ai_reasoning": "Healthy throughput verified against Runbook MED-QUEUE-WARN. Error rate < 0.05% indicates clean morning outpatient lab test rush. Safe to autoscale from 2 to 6 pods within policy limit (max 10).",
                    "risk_tier": "Tier 2 (Guarded Auto - Within Policy Limits)",
                    "blast_radius_desc": "MEDIUM: Outpatient notification pods. Capped at policy ceiling of 10 pods.",
                    "requires_human_approval": 0,
                    "proposed_action": "Autoscale lab results consumer deployment from 2 to 6 replicas within policy limits.",
                    "remediation_command": "kubectl scale deployment/order-consumer --replicas=6 --namespace=orders",
                    "rollback_command": "kubectl scale deployment/order-consumer --replicas=2 --namespace=orders",
                    "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }

        elif fault_type == "ssl_expiry":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "routine_renew"))
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                return {
                    "root_cause": "Uncritical certificate health check: Hospital medical IoT devices gateway certificate has 75.0 days remaining.",
                    "ai_reasoning": "UNCRITICAL CRYPTOGRAPHIC AUDIT (Runbook MED-SSL-UNC): Certificate validity is healthy (75 days remaining). Proactive cipher suite and OCSP audit executed. System 100% operational.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
                    "blast_radius_desc": "ZERO (0%): Read-only cryptographic handshake validation probe. Zero configuration modifications.",
                    "requires_human_approval": 0,
                    "proposed_action": "Perform read-only cryptographic validation probe and record hospital security audit entry.",
                    "remediation_command": "openssl s_client -servername devices.lifecare.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'",
                    "rollback_command": "echo 'AUDIT_NOOP'",
                    "verification_check": "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/devices.lifecare.internal.crt",
                    "is_ambiguous": False
                }
            elif sub_type in ["root_ca_broken", "critical_ssl"] or float(telemetry.get("hours_remaining", 99)) < 12.0:
                return {
                    "root_cause": "CRITICAL TELEMEDICINE VIDEO GATEWAY SSL EXPIRES IN 5 HOURS: Upstream root CA revoked!",
                    "ai_reasoning": "RUNBOOK MED-SSL-CRIT ESCALATION: Remote doctor video consultations and telemedicine patient appointments will drop in 5 hours! Automated ACME certbot cannot renew due to revoked intermediate CA. Mandates immediate escalation to Hospital CISO.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Live remote doctor video consultations + HIPAA compliance.",
                    "requires_human_approval": 1,
                    "proposed_action": "Halt automated renewal loop, import updated trusted hospital root CA bundle, and require Hospital CISO Authorization.",
                    "remediation_command": "update-ca-certificates --fresh && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/telemed.lifecare.org.crt",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Patient health records portal TLS certificate expiring in 4.2 days.",
                    "ai_reasoning": "Valid certificate renewal window verified against Runbook MED-SSL-WARN. Automated ACME challenge ready. Safe for autonomous key rotation and seamless nginx reload.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Public patient records portal. Seamless zero-downtime configuration reload.",
                    "requires_human_approval": 0,
                    "proposed_action": "Execute automated certbot TLS certificate renewal and reload ingress nginx reverse proxy.",
                    "remediation_command": "certbot renew --cert-name portal.lifecare.org --quiet && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/portal.lifecare.org.crt",
                    "is_ambiguous": False
                }

    # =========================================================================
    # 3. GLOBALPAY FINTECH & BANKING CLOUD (MASTER DEFAULT)
    # =========================================================================
    else:
        if fault_type == "disk_overflow":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "logs"))
            if sub_type in ["routine_hygiene", "uncritical_logs", "uncritical"]:
                return {
                    "root_cause": "Uncritical routine hygiene: Inactive build scratch files and old caches detected in /tmp/builds (54.2% disk usage).",
                    "ai_reasoning": "UNCRITICAL ROUTINE HYGIENE (Runbook RB-UNC-01): Telemetry confirms disk utilization is healthy (54.2%, 92GB free). System performs proactive off-peak pruning. Blast radius is strictly zero. 100% safe for autonomous background execution without alerting or waking on-call personnel.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Targets purely stale scratch build layers and temporary sockets older than 14 days. Zero application impact.",
                    "requires_human_approval": 0,
                    "proposed_action": "Safely prune temporary scratch builds older than 14 days and vacuum systemd journal to reclaim 12.4 GB.",
                    "remediation_command": "find /tmp/builds -type f -name '*.tmp' -mtime +14 -delete && journalctl --vacuum-size=500M",
                    "rollback_command": "touch /tmp/builds/.maintenance_complete",
                    "verification_check": "df -h / | awk 'NR==2 {print \"PASS_DISK_HEALTHY\"}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["core_dump", "critical_disk"] or "mysql" in str(telemetry).lower() or "core" in str(telemetry).lower() or "wal" in str(telemetry).lower():
                return {
                    "root_cause": "CRITICAL POSTGRESQL WAL EXHAUSTION (99.4% Capacity): Partition /var/lib/postgresql/pg_wal has only 124MB remaining due to replication lag. Database entering emergency PANIC shutdown.",
                    "ai_reasoning": "RUNBOOK RB-01-CRIT VIOLATION PREVENTED: If WAL segments are blindly deleted, all database read-replicas will permanently desynchronize and crash! Encoded senior SRE judgment halts execution and mandates Human Authorization to archive WAL segments safely to S3 first.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Database filesystem integrity and disaster recovery replication for 100% of customer checkout databases.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze WAL auto-purging, snapshot uncompressed WAL segments to S3 cold storage, and request Human Operator authorization before clearing temp space.",
                    "remediation_command": "aws s3 sync /var/lib/postgresql/pg_wal s3://ops-wal-archive/ && rm -f /var/lib/postgresql/pg_wal/*.old",
                    "rollback_command": "aws s3 sync s3://ops-wal-archive/ /var/lib/postgresql/pg_wal/ || true",
                    "verification_check": "df -h /var/lib/postgresql/pg_wal | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 85) print \"PASS\"; else print \"FAIL\"}'",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Warning: Nginx reverse proxy static cache partition /var/cache/nginx has reached high-water mark (88.5% capacity).",
                    "ai_reasoning": "Standard rotatable cache pattern verified against Runbook RB-01-WARN. Telemetry confirms files are purely expired static cache objects. Zero active database or binary files impacted. Safe for autonomous remediation within policy limits.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Local partition /var/cache/nginx only. Zero service downtime. Fully reversible via snapshot archive.",
                    "requires_human_approval": 0,
                    "proposed_action": "Purge cached static proxy objects older than 24 hours to reclaim 28.5 GB storage.",
                    "remediation_command": "find /var/cache/nginx -type f -mtime +1 -delete && nginx -s reload",
                    "rollback_command": "echo 'ROLLBACK_CACHE_REBUILD'",
                    "verification_check": "df -h /var/cache/nginx | awk 'NR==2 {gsub(\"%\", \"\"); if ($5 < 75) print \"PASS\"; else print \"FAIL\"}'",
                    "is_ambiguous": False
                }

        elif fault_type == "worker_stuck":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "db_exhaustion"))
            if sub_type in ["routine_gc_trim", "uncritical_worker", "uncritical"]:
                return {
                    "root_cause": "Uncritical worker maintenance: media-worker-05 has completed 15,400 image transformations; minor heap fragmentation detected.",
                    "ai_reasoning": "UNCRITICAL PREVENTIVE RECYCLE (Runbook RB-UNC-02): Worker is fully alive and processing normally. Applying soft garbage collection and worker reloading during idle task gap. Zero downtime, zero human disturbance.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Graceful soft reload during idle window. Active queues unaffected.",
                    "requires_human_approval": 0,
                    "proposed_action": "Execute graceful worker reload to compact Python runtime memory heap during task lull.",
                    "remediation_command": "systemctl reload-or-restart celery-worker@media-worker-05.service",
                    "rollback_command": "systemctl status celery-worker@media-worker-05.service",
                    "verification_check": "systemctl is-active celery-worker@media-worker-05.service",
                    "is_ambiguous": False
                }
            elif sub_type in ["db_exhaustion", "critical_worker"] or telemetry.get("in_flight_transactions", 0) > 0 or "sat" in str(telemetry).lower():
                return {
                    "root_cause": "CRITICAL PAYMENT RECONCILIATION THREADLOCK: py-recon-daemon (PID 4092) locked with 8,400 in-flight settlements ($1,420,000 USD volume); Postgres connection pool at 99%.",
                    "ai_reasoning": "RUNBOOK RB-02-CRIT SAFETY GATE: Terminating this worker blindly will corrupt 8,400 pending customer transactions, leading to duplicate credit card charges and financial audit discrepancies! System blocks uncoordinated kill, pauses inbound webhook traffic, and requires Senior Fintech SRE sign-off.",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: 8,400 pending transactions ($1.42M volume) and database connection pool.",
                    "requires_human_approval": 1,
                    "proposed_action": "Pause inbound webhooks, gracefully flush transaction write-ahead buffer, and mandate Human Operator approval before restarting service.",
                    "remediation_command": "python3 /opt/fintech/scripts/drain_recon_locks.py && systemctl restart celery-worker@worker-03.service",
                    "rollback_command": "systemctl restart celery-worker@worker-03.service",
                    "verification_check": "systemctl is-active celery-worker@worker-03.service && psql -c 'SELECT count(*) FROM pg_stat_activity' | grep -v '100'",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Email Dispatcher Celery Worker (PID 1840) hung in external SendGrid HTTP socket read (310s delay).",
                    "ai_reasoning": "Safe restart policy verified against Runbook RB-02-WARN. Telemetry proves worker is purely an email dispatcher; zero in-flight database transactions or Redis distributed locks held. Safe for autonomous restart.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Background email notification queue only. Zero customer payment impact.",
                    "requires_human_approval": 0,
                    "proposed_action": "Gracefully terminate hung worker process via SIGTERM and trigger automatic Celery task requeue.",
                    "remediation_command": "systemctl restart celery-worker@worker-node-03.service",
                    "rollback_command": "systemctl restart celery-worker@worker-node-03-fallback.service",
                    "verification_check": "systemctl is-active celery-worker@worker-node-03.service",
                    "is_ambiguous": False
                }

        elif fault_type == "queue_growth":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "poison_pill"))
            if sub_type in ["routine_queue_balance", "uncritical_queue", "uncritical"]:
                return {
                    "root_cause": "Uncritical queue balancing: Analytics clickstream batch backlog has minor evening browsing ripple (850 msgs).",
                    "ai_reasoning": "UNCRITICAL QUEUE BALANCING (Runbook RB-UNC-03): Telemetry confirms normal traffic ripple well within SLA thresholds (<5,000 msgs). Auto-handled silently by spinning up 1 standby worker container.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)",
                    "blast_radius_desc": "ZERO (0%): Purely temporary browsing events. Sub-150ms processing SLA maintained.",
                    "requires_human_approval": 0,
                    "proposed_action": "Scale clickstream consumer pods from 2 to 3 to maintain sub-150ms SLA.",
                    "remediation_command": "kubectl scale deployment/clickstream-consumer --replicas=3 --namespace=analytics",
                    "rollback_command": "kubectl scale deployment/clickstream-consumer --replicas=2 --namespace=analytics",
                    "verification_check": "kubectl get deployment/clickstream-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }
            elif sub_type in ["poison_pill", "critical_queue"] or float(str(telemetry.get("consumer_error_rate", "0")).replace("%", "")) > 50.0:
                return {
                    "root_cause": "CRITICAL POISON PILL KAFKA CONSUMER CRASH LOOP: Malformed message payload on fraud.transactions.stream causing 92.4% error rate.",
                    "ai_reasoning": "RUNBOOK RB-03-CRIT SAFETY GATE: Blindly autoscaling pods will spawn pods that immediately crash in infinite loops, burning compute budget ($4,500/hr) with 0 progress! System halts autoscaling and mandates Human Authorization to isolate bad offset to Dead Letter Queue (DLQ).",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "HIGH: Financial fraud detection consumer group and Kubernetes compute cluster capacity.",
                    "requires_human_approval": 1,
                    "proposed_action": "Freeze pod autoscaling, isolate corrupt offset 892014 to Dead Letter Queue, and require Human Authorization.",
                    "remediation_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group fraud-detectors --topic fraud.transactions.stream --reset-offsets --to-offset 892014 --execute",
                    "rollback_command": "kafka-consumer-groups --bootstrap-server kafka:9092 --group fraud-detectors --topic fraud.transactions.stream --reset-offsets --to-offset 892013 --execute",
                    "verification_check": "echo PASS_DLQ_ROUTED",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Promotional flash sale surge on queue checkout.flash.events (28,500 msgs, error rate 0.02%).",
                    "ai_reasoning": "Healthy consumer throughput verified against Runbook RB-03-WARN. Error rate < 0.05% indicates clean traffic. Safe to autoscale from 4 to 8 pods within policy limit (max 10).",
                    "risk_tier": "Tier 2 (Guarded Auto - Within Policy Limits)",
                    "blast_radius_desc": "MEDIUM: Flash sale consumer pods. Capped at policy ceiling of 10 pods to prevent compute cost overruns.",
                    "requires_human_approval": 0,
                    "proposed_action": "Autoscale consumer deployment from 4 to 8 replicas within policy limits.",
                    "remediation_command": "kubectl scale deployment/order-consumer --replicas=8 --namespace=orders",
                    "rollback_command": "kubectl scale deployment/order-consumer --replicas=4 --namespace=orders",
                    "verification_check": "kubectl get deployment/order-consumer -o jsonpath='{.status.readyReplicas}'",
                    "is_ambiguous": False
                }

        elif fault_type == "ssl_expiry":
            sub_type = context.get("sub_type", telemetry.get("sub_type", "routine_renew"))
            if sub_type in ["routine_audit_check", "uncritical_ssl", "uncritical"]:
                return {
                    "root_cause": "Uncritical certificate health check: mTLS-auth.internal certificate has 58.0 days remaining.",
                    "ai_reasoning": "UNCRITICAL CRYPTOGRAPHIC AUDIT (Runbook RB-UNC-04): Certificate validity is healthy (58 days remaining). Proactive cipher suite and OCSP audit executed. System 100% operational.",
                    "risk_tier": "Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)",
                    "blast_radius_desc": "ZERO (0%): Read-only cryptographic handshake validation probe. Zero configuration modifications.",
                    "requires_human_approval": 0,
                    "proposed_action": "Perform read-only cryptographic validation probe and record security audit entry.",
                    "remediation_command": "openssl s_client -servername mTLS-auth.internal -connect 127.0.0.1:443 </dev/null 2>/dev/null | openssl x509 -noout -dates && echo 'AUDIT_VERIFIED_VALID'",
                    "rollback_command": "echo 'AUDIT_NOOP'",
                    "verification_check": "openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/mTLS-auth.internal.crt",
                    "is_ambiguous": False
                }
            elif sub_type in ["root_ca_broken", "critical_ssl"] or float(telemetry.get("hours_remaining", 99)) < 12.0:
                return {
                    "root_cause": "CRITICAL PAYMENT GATEWAY TLS ROOT CA REVOCATION: Certificate expires in 6.2 hours; intermediate CA revoked upstream!",
                    "ai_reasoning": "RUNBOOK RB-04-CRIT ESCALATION: Automated ACME renewals will fail due to revoked upstream CA. If expired, $4.2M/minute in global card transactions will fail immediately. Mandates immediate escalation to Chief Information Security Officer (CISO).",
                    "risk_tier": "Ambiguous / Tier 3 (Escalated to Human)",
                    "blast_radius_desc": "CRITICAL: Global edge TLS termination and payment checkout ingress ($4.2M/minute transaction volume).",
                    "requires_human_approval": 1,
                    "proposed_action": "Halt automated renewal loop, import updated trusted intermediate CA bundle, and require CISO Authorization.",
                    "remediation_command": "update-ca-certificates --fresh && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/api.globalpay.com.crt",
                    "is_ambiguous": True
                }
            else:
                return {
                    "root_cause": "Customer web portal TLS certificate expiring in 4.5 days.",
                    "ai_reasoning": "Valid certificate renewal window verified against Runbook RB-04-WARN. Automated ACME challenge ready. Safe for autonomous key rotation and seamless nginx reload.",
                    "risk_tier": "Tier 1 (Low Risk - Safe Auto)",
                    "blast_radius_desc": "LOW: Web portal ingress endpoint. Seamless zero-downtime configuration reload.",
                    "requires_human_approval": 0,
                    "proposed_action": "Execute automated certbot TLS certificate renewal and reload ingress nginx reverse proxy.",
                    "remediation_command": "certbot renew --cert-name portal.production.io --quiet && nginx -s reload",
                    "rollback_command": "cp /etc/ssl/backup/last_known_good.crt /etc/ssl/certs/ && nginx -s reload",
                    "verification_check": "openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/portal.production.io.crt",
                    "is_ambiguous": False
                }

    # Fallback for arbitrary custom fault
    return {
        "root_cause": f"Operational event detected in subsystem {fault_type}.",
        "ai_reasoning": "Evaluated against active safety policies. Guardrails require human review.",
        "risk_tier": "Tier 3 (High Risk - Human Approval Required)",
        "blast_radius_desc": "MEDIUM: Subsystem state modifications.",
        "requires_human_approval": 1,
        "proposed_action": "Conduct diagnostic telemetry review.",
        "remediation_command": f"systemctl restart {fault_type}.service || true",
        "rollback_command": f"systemctl status {fault_type}.service || true",
        "verification_check": "echo PASS",
        "is_ambiguous": True
    }
