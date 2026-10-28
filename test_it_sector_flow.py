from app import app
import json

client = app.test_client()

print("==================================================================")
print("TESTING IT SECTOR / DEVOPSCORP DATASET ENDPOINTS")
print("==================================================================")

# 1. Test /api/database/presets includes it_sector
res = client.get("/api/database/presets")
assert res.status_code == 200
presets = res.get_json()["presets"]
it_p = next((p for p in presets if p["id"] == "it_sector"), None)
assert it_p is not None, "it_sector preset not found in presets list!"
print(f"1. Presets endpoint: Found '{it_p['name']}' ({it_p['domain']})")

# 2. Test Loading IT Sector Preset
res = client.post("/api/database/load-preset/it_sector")
assert res.status_code == 200
data = res.get_json()
print(f"2. Loaded IT Sector: {data['message']}")

# Verify Metrics
res = client.get("/api/metrics")
metrics = res.get_json()
print(f"   IT Sector Metrics ({len(metrics)} total):")
for m in metrics:
    print(f"   - {m['name']}: {m['value']} {m['unit']}")

# Verify Runbooks
res = client.get("/api/runbooks")
rbs = res.get_json()
print(f"   IT Sector Runbooks ({len(rbs)} total):")
for rb in rbs:
    print(f"   - [{rb['runbook_id']}] {rb['title']}")

# 3. Test Injecting IT Critical Disk Fault
res = client.post("/api/inject-fault", json={"fault_type": "disk_overflow", "sub_type": "core_dump"})
inc = res.get_json()
print(f"\n3. Injected IT Critical Disk Fault: {inc['title']}")
assert "Docker Registry" in inc["title"] or "DevOpsCorp" in inc["title"]

# Test AI Diagnosis
res = client.post(f"/api/diagnose/{inc['incident_id']}")
diag = res.get_json()["diagnosis"]
print(f"   Diagnosis: {diag['root_cause']}")
print(f"   AI Reasoning: {diag['ai_reasoning'][:90]}...")
print(f"   Approval Required: {diag['requires_human_approval']} (Principal DevOps SRE Gate)")
assert diag["requires_human_approval"] == 1

# 4. Test Injecting IT Uncritical Disk Fault
res = client.post("/api/inject-fault", json={"fault_type": "disk_overflow", "sub_type": "routine_hygiene"})
inc_unc = res.get_json()
print(f"\n4. Injected IT Uncritical Disk Fault: {inc_unc['title']}")
assert "JUnit" in inc_unc["title"] or "Scratch" in inc_unc["title"]

# Test AI Diagnosis for Uncritical
res = client.post(f"/api/diagnose/{inc_unc['incident_id']}")
diag_unc = res.get_json()["diagnosis"]
print(f"   Diagnosis: {diag_unc['root_cause']}")
print(f"   Approval Required: {diag_unc['requires_human_approval']} (Tier 0/1 Safe Auto)")
assert diag_unc["requires_human_approval"] == 0

# 5. Test Injecting IT Critical GitOps Worker Fault
res = client.post("/api/inject-fault", json={"fault_type": "worker_stuck", "sub_type": "db_exhaustion"})
inc_worker = res.get_json()
print(f"\n5. Injected IT Critical Worker Fault: {inc_worker['title']}")
assert "Terraform" in inc_worker["title"] or "GitOps" in inc_worker["title"]

res = client.post(f"/api/diagnose/{inc_worker['incident_id']}")
diag_worker = res.get_json()["diagnosis"]
print(f"   Diagnosis: {diag_worker['root_cause']}")
print(f"   Approval Required: {diag_worker['requires_human_approval']} (Distributed Lock Gate)")
assert diag_worker["requires_human_approval"] == 1

# 6. Test Downloads for IT Sector
print("\n6. Testing Direct IT Sector Downloads:")
res_json = client.get("/api/database/download-preset/it_sector")
assert res_json.status_code == 200
print(f"   - /api/database/download-preset/it_sector (JSON): {len(res_json.data)} bytes OK")

res_sql = client.get("/api/database/download-preset-sql/it_sector")
assert res_sql.status_code == 200
print(f"   - /api/database/download-preset-sql/it_sector (SQL): {len(res_sql.data)} bytes OK")

res_db = client.get("/api/database/download-preset-db/it_sector")
assert res_db.status_code == 200
print(f"   - /api/database/download-preset-db/it_sector (SQLite DB): {len(res_db.data)} bytes OK")

print("\n==================================================================")
print("ALL IT SECTOR DATASET TESTS PASSED FLAWLESSLY!")
print("==================================================================")
