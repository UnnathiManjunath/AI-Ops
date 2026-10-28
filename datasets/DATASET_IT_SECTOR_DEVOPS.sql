-- ============================================================================

-- SafeOps AI - Operational Database: DevOpsCorp Enterprise IT & Cloud Infrastructure

-- Track: Cynefian 24-Hour Student Hackathon - AI-Ops Track (Problem AO-04)

-- Team: Idea Ignitors (XH-23) - Unnathi T M, Chaithanya N S, M Eshwar, Babitha M

-- Domain: IT Sector, Enterprise CI/CD, Kubernetes & Software Engineering Cloud

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

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('disk_usage_pct', 'CI/CD Docker Registry & Artifact Storage (/var/lib/docker)', 49.6, '%', 80.0, 95.0, 'OK', 'ci-runner-cluster-01');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('worker_status', 'GitOps Terraform & Kubernetes Deployment Controller', 1.0, 'State (0=Locked, 1=Alive)', 0.5, 0.0, 'OK', 'gitops-controller-pool');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('queue_backlog_depth', 'GitHub Enterprise Code Merge & Webhook Queue', 580.0, 'msgs', 10000.0, 50000.0, 'OK', 'kafka-devops-telemetry');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('ssl_cert_days', 'Enterprise Single Sign-On (SSO / Okta SAML) Ingress TLS', 60.0, 'days', 14.0, 5.0, 'OK', 'sso.corp-it.internal');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('cpu_utilization', 'Kubernetes CI/CD Worker Node Pool CPU Load', 28.4, '%', 75.0, 90.0, 'OK', 'k8s-devops-workers');

INSERT INTO system_metrics (metric_key, name, value, unit, threshold_warn, threshold_crit, status, server_node) VALUES ('memory_utilization', 'Kubernetes CI/CD Worker Node Pool RAM Usage', 42.1, '%', 80.0, 90.0, 'OK', 'k8s-devops-workers');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('active_preset', 'Active Operational Preset', 'it_sector', 'DevOpsCorp Enterprise IT & Cloud Infrastructure');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('kill_switch_active', 'Emergency Master Kill Switch', 'false', 'Instant freeze for all enterprise IT automated remediation jobs across clusters.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('rate_limit_per_minute', 'Action Rate Limiter', '5', 'Maximum 5 automated remediations per minute to prevent runaway build loops.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('max_scaling_instances', 'Max CI/CD Build Pods', '10', 'Strict Kubernetes node compute ceiling to prevent runaway AWS/GCP cloud billing ($4,200/hr risk).');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('disk_safety_floor_gb', 'Artifact Storage Safety Floor', '5.0', 'Minimum free disk buffer below which high-risk escalation is mandated.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('tier1_auto_enabled', 'Tier 1 Safe Auto-Remediation', 'true', 'Autonomous execution of non-destructive cache pruning without deployment risk.');

INSERT INTO safety_policies (policy_key, policy_name, value, description) VALUES ('tier3_requires_approval', 'Tier 3 Principal DevOps Human Gate', 'true', 'Mandatory Principal SRE sign-off before modifying production container registries or live clusters.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-DISK-CRIT', 'DevOpsCorp Critical: Production Docker Registry & Container Image Layer Partition Full (99.3% - 210MB Left!)', 'IT Cloud Storage', '/var/lib/docker/overlay2', 'Docker storage partition > 99% (Only 210MB remaining, 84 production deployments blocked!)', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: 84 enterprise production software deployments blocked + container daemon freeze.', 'IF Docker storage partition is at 99.3%, software releases cannot deploy! DO NOT run ''docker system prune -a'' blindly (destroys active base images and prevents rollback tags). Snapshot production release image tags to AWS ECR / Google Artifact Registry with Principal DevOps sign-off.', 'aws ecr sync-images /var/lib/docker/production-tags/ && docker image prune --filter 'until=72h' --force', 'docker pull registry.corp-it.internal:5000/base-images/production:v3.2.0', 'df -h /var/lib/docker | awk 'NR==2 {gsub("%", ""); if ($5 < 85) print "PASS"; else print "FAIL"}'', 'Safeguards production container base images and release tags against accidental deletion during emergency disk exhaustion.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-DISK-WARN', 'DevOpsCorp Warning: Developer Build Cache & Gradle/NPM Artifact High-Water Mark (86.4%)', 'IT Cloud Storage', '/var/cache/build_artifacts', 'Artifact cache usage > 85%', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Local builder temporary NPM/Maven cache only. Zero production service impact.', 'IF build cache partition exceeds 85%, purge unreferenced dependency tarballs and intermediate compiler outputs older than 7 days to reclaim 32 GB. Safe for autonomous execution.', 'find /var/cache/build_artifacts/ -name '*.tar.gz' -mtime +7 -delete && journalctl --vacuum-time=2d', 'touch /var/cache/build_artifacts/.cache_rebuild_ready', 'df -h /var/cache/build_artifacts | awk 'NR==2 {gsub("%", ""); if ($5 < 75) print "PASS"; else print "FAIL"}'', 'Clears stale dependency caches safely without interrupting active developer compilation jobs.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-DISK-UNC', 'DevOpsCorp Uncritical: Stale CI Unit Test Report XML & SonarQube Scratch Hygiene (49.6%)', 'IT Cloud Hygiene', '/tmp/ci_test_scratch', 'Off-peak nightly schedule OR scratch storage between 40% and 55%', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Temporary JUnit XML test results and coverage heatmaps older than 14 days.', 'IF disk utilization is non-critical (49.6%), silently prune old JUnit test results and code coverage scratch files older than 14 days without alerting on-call engineers.', 'find /tmp/ci_test_scratch -type f -name '*.xml' -mtime +14 -delete', 'touch /tmp/ci_test_scratch/.maintenance_complete', 'df -h /tmp/ci_test_scratch | awk 'NR==2 {print "PASS_DISK_HEALTHY"}'', 'Routine nightly housekeeping for CI/CD test runner ephemeral scratch disks.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-WORKER-CRIT', 'DevOpsCorp Critical: GitOps Terraform Cloud Sync Controller Threadlock (48 Active Microservice Rollouts!)', 'IT DevOps Compute', 'gitops-sync-controller', 'GitOps sync controller heartbeat missing > 300s while 48 microservice deployments in-flight', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: 48 live production microservice Kubernetes deployments + AWS cloud infrastructure state lock.', 'IF GitOps controller is locked during live rollout, DO NOT kill worker process (prevents split-brain Terraform cloud state and orphaned Kubernetes deployments). Human SRE authorization required to release distributed DynamoDB state lock safely before restarting.', 'terraform force-unlock -force 8a2f-109b-c43e && systemctl restart gitops-sync-controller.service', 'systemctl restart gitops-sync-controller.service', 'systemctl is-active gitops-sync-controller.service', 'Prevents catastrophic split-brain cloud state in enterprise Terraform GitOps pipelines.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-WORKER-WARN', 'DevOpsCorp Warning: Enterprise Slack / Jira CI/CD Notification Webhook Worker Stalled (260s)', 'IT Notifications', 'slack-jira-notifier-02', 'Worker heartbeat missed for > 240s (Slack API rate limit socket wait)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Developer notification channel only. Zero production software deployment risk.', 'IF notification worker is stalled on external Slack webhook rate limits, perform graceful SIGTERM restart with automatic event backoff and retry.', 'systemctl restart celery-worker@slack-jira-notifier-02.service', 'systemctl restart celery-worker@slack-jira-notifier-02-fallback.service', 'systemctl is-active celery-worker@slack-jira-notifier-02.service', 'Graceful cycling of developer Slack/Jira notification dispatchers without message loss.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-WORKER-UNC', 'DevOpsCorp Uncritical: Static Code Linter & AST Syntax Analyzer Soft Memory Recycle (25,000 Commits)', 'IT Code Analysis', 'code-linter-daemon-04', 'Worker processed > 20,000 commits (Worker Alive and Processing)', 'Tier 0 / Tier 1 (Uncritical - Silent Safe Auto)', 'ZERO (0%): Soft reload occurs between pull request linting batches.', 'IF linter worker is healthy but has minor Python/Go memory heap fragmentation, trigger graceful soft reload during nightly sprint lull.', 'systemctl reload-or-restart celery-worker@code-linter-daemon-04.service', 'systemctl status celery-worker@code-linter-daemon-04.service', 'systemctl is-active celery-worker@code-linter-daemon-04.service', 'Compacts memory on automated static code analysis and security AST parsing daemons.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-QUEUE-CRIT', 'DevOpsCorp Critical: OpenTelemetry Distributed Trace Kafka Ingress Crash Loop (172,000 msgs - 91.5% Err)', 'IT Observability', 'otel.traces.ingress', 'Queue backlog > 100,000 and consumer error rate > 80%', 'Tier 3 (High Risk - Human Approval Required)', 'HIGH: Enterprise observability pipeline + Kubernetes cluster compute capacity.', 'IF error rate is > 80% (malformed OpenTelemetry span JSON payload crashing collector pods in infinite loops), DO NOT autoscale pods (burns $4,200/hr compute with 0 progress); isolate corrupt offset to Observability Dead Letter Queue (DLQ) with human sign-off.', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group otel-collectors --topic otel.traces.ingress --reset-offsets --to-offset 602819 --execute', 'kafka-consumer-groups --bootstrap-server kafka:9092 --group otel-collectors --topic otel.traces.ingress --reset-offsets --to-offset 602818 --execute', 'echo PASS_DLQ_ROUTED', 'Isolates corrupt OpenTelemetry tracing payloads to protect enterprise APM monitoring from brownouts.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-QUEUE-WARN', 'DevOpsCorp Warning: GitHub Enterprise Pull Request Merge Webhook Queue Backlog (38,000 msgs)', 'IT Developer Tools', 'github.pr.merges', 'Queue backlog > 25,000 and consumer error rate < 0.05%', 'Tier 2 (Guarded Auto - Within Policy Limits)', 'MEDIUM: GitHub webhook consumers. Capped at policy ceiling of 10 pods.', 'IF consumer error rate is low (<0.05% during 5:00 PM sprint code freeze / merge rush), autoscale webhook processing pods from 3 to 9 pods within safety ceiling (max 10).', 'kubectl scale deployment/github-webhook-consumer --replicas=9 --namespace=ci', 'kubectl scale deployment/github-webhook-consumer --replicas=3 --namespace=ci', 'kubectl get deployment/github-webhook-consumer -o jsonpath='{.status.readyReplicas}'', 'Autoscales GitHub webhook delivery pods during end-of-sprint code merge rushes.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-QUEUE-UNC', 'DevOpsCorp Uncritical: Engineering DORA Metrics Analytics Batch Queue Ripple (580 msgs)', 'IT Queues', 'engineering.dora.metrics', 'Backlog between 400 and 1,000 messages (Minor Off-Peak Ripple)', 'Tier 1 (Uncritical - Silent Safe Auto)', 'LOW (< 5%): Spins up 1 standby consumer container.', 'IF backlog has minor evening ripple (580 msgs), activate 1 standby pod to maintain sub-150ms processing SLA on developer velocity dashboards.', 'kubectl scale deployment/dora-consumer --replicas=3 --namespace=ci', 'kubectl scale deployment/dora-consumer --replicas=2 --namespace=ci', 'kubectl get deployment/dora-consumer -o jsonpath='{.status.readyReplicas}'', 'Maintains sub-second delivery for developer productivity and DORA analytics metrics.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-SSL-CRIT', 'DevOpsCorp Critical: Corporate Single Sign-On (SSO / Okta SAML) Ingress TLS Expiring in 3 Hours (15,000 Engineers Locked Out!)', 'IT Security & IAM', 'sso.corp-it.internal', 'SSO certificate validity < 6 hours and internal HashiCorp Vault root CA revoked upstream', 'Tier 3 (High Risk - Human Approval Required)', 'CRITICAL: 15,000 enterprise software engineers and staff access to GitHub, AWS, Jira & Slack.', 'IF SSO gateway certificate expires in 3 hours and internal Vault intermediate CA is revoked, automated certbot renewals will fail! 15,000 engineers will lose access to all cloud systems. Escalate immediately to Enterprise CISO and Lead IAM Architect.', 'vault write auth/cert/config certificate=@/etc/ssl/certs/vault-root-renewed.crt && nginx -s reload', 'cp /etc/ssl/backup/last_known_good_sso.crt /etc/ssl/certs/ && nginx -s reload', 'openssl verify -CAfile /etc/ssl/certs/vault-root.crt /etc/ssl/certs/sso.corp-it.internal.crt', 'Protects enterprise IAM Single Sign-On infrastructure against authentication lockout.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-SSL-WARN', 'DevOpsCorp Warning: Staging Kubernetes Cluster Wildcard Ingress TLS Certificate Expiring (4.1 Days)', 'IT Ingress Security', '*.staging.corp-it.io', 'Certificate validity <= 5 days (ACME DNS-01 challenge ready)', 'Tier 1 (Low Risk - Safe Auto)', 'LOW: Staging microservices ingress only. Zero production service downtime.', 'IF certificate is within 5 days of expiry and DNS records valid, trigger automated certbot DNS-01 renewal and seamless ingress nginx reload.', 'certbot renew --cert-name staging.corp-it.io --preferred-challenges dns-01 --quiet && nginx -s reload', 'cp /etc/ssl/backup/last_known_good_staging.crt /etc/ssl/certs/ && nginx -s reload', 'openssl x509 -checkend 604800 -noout -in /etc/ssl/certs/staging.corp-it.io.crt', 'Automated renewal of staging cluster wildcard TLS certificates.');

INSERT INTO runbooks (runbook_id, title, category, target_subsystem, trigger_condition, safe_action_tier, blast_radius, judgment_rules, remediation_command, rollback_command, verification_check, documentation) VALUES ('IT-SSL-UNC', 'DevOpsCorp Uncritical: Internal Kubernetes Istio Service Mesh Mutual TLS (mTLS) Audit (60.0 Days)', 'IT Security Audit', 'cluster.local', 'Scheduled audit OR certificate validity at 60 days remaining', 'Tier 0 / Tier 1 (Uncritical - Preventive Health Audit)', 'ZERO (0%): Read-only cryptographic handshake validation probe.', 'IF internal service mesh certificate validity is healthy (60 days remaining), execute routine cipher suite verification. No human intervention needed.', 'istioctl proxy-config secret deployment/ingressgateway.istio-system && echo 'AUDIT_VERIFIED_VALID'', 'echo 'AUDIT_NOOP'', 'openssl x509 -checkend 2592000 -noout -in /etc/ssl/certs/istio-mtls.crt', 'Proactive cryptographic validity audit across internal Kubernetes microservice mTLS sidecars.');