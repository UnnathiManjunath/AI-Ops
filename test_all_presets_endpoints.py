import os
import json
from app import app

client = app.test_client()

print("==================================================================")
print("TESTING MULTI-DATASET & PRESET SYSTEM ENDPOINTS")
print("==================================================================")

# 1. Test /api/database/presets
res = client.get("/api/database/presets")
assert res.status_code == 200, f"Failed presets GET: {res.status_code}"
data = res.get_json()
print(f"1. /api/database/presets: Found {len(data['presets'])} presets! Active: {data['active_preset']}")

# 2. Test Loading QuickCart E-Commerce Preset
res = client.post("/api/database/load-preset/ecommerce")
assert res.status_code == 200, f"Failed load ecommerce: {res.status_code}"
data = res.get_json()
print(f"2. Loaded QuickCart: {data['message']}")

# Verify Metrics for QuickCart
res = client.get("/api/metrics")
metrics = res.get_json()
print(f"   QuickCart Metrics count: {len(metrics)}")
for m in metrics:
    print(f"   - {m['name']}: {m['value']} {m['unit']}")

# Verify Runbooks for QuickCart
res = client.get("/api/runbooks")
rbs = res.get_json()
print(f"   QuickCart Runbooks count: {len(rbs)}")
for rb in rbs[:3]:
    print(f"   - [{rb['runbook_id']}] {rb['title']}")

# Test Injecting QuickCart Critical Fault
res = client.post("/api/inject-fault", json={"fault_type": "disk_overflow", "sub_type": "core_dump"})
inc = res.get_json()
print(f"3. Injected QuickCart Critical Fault: {inc['title']}")
assert "Invoicing" in inc["title"] or "QuickCart" in inc["title"]

# Test AI Diagnosis for QuickCart Critical Fault
res = client.post(f"/api/diagnose/{inc['incident_id']}")
resp_diag = res.get_json()
diag = resp_diag['diagnosis']
print(f"   Diagnosis: {diag['root_cause']}")
print(f"   AI Reasoning: {diag['ai_reasoning'][:80]}...")
print(f"   Approval Required: {diag['requires_human_approval']}")
assert diag['requires_human_approval'] == 1

# Test Injecting QuickCart Uncritical Fault
res = client.post("/api/inject-fault", json={"fault_type": "disk_overflow", "sub_type": "routine_hygiene"})
inc_unc = res.get_json()
print(f"4. Injected QuickCart Uncritical Fault: {inc_unc['title']}")
res = client.post(f"/api/diagnose/{inc_unc['incident_id']}")
diag_unc = res.get_json()['diagnosis']
print(f"   Diagnosis: {diag_unc['root_cause']}")
print(f"   Approval Required: {diag_unc['requires_human_approval']} (Tier 0/1 Safe Auto)")
assert diag_unc['requires_human_approval'] == 0

# 3. Test Loading LifeCare Healthcare Preset
res = client.post("/api/database/load-preset/healthcare")
assert res.status_code == 200
data = res.get_json()
print(f"\n5. Loaded LifeCare: {data['message']}")

# Test Injecting LifeCare Critical Worker Fault
res = client.post("/api/inject-fault", json={"fault_type": "worker_stuck", "sub_type": "db_exhaustion"})
inc_med = res.get_json()
print(f"6. Injected LifeCare Worker Critical: {inc_med['title']}")
assert "Ambulance" in inc_med["title"] or "911" in inc_med["title"]

# Test AI Diagnosis for LifeCare
res = client.post(f"/api/diagnose/{inc_med['incident_id']}")
diag_med = res.get_json()['diagnosis']
print(f"   Diagnosis: {diag_med['root_cause']}")
print(f"   Approval Required: {diag_med['requires_human_approval']}")
assert diag_med['requires_human_approval'] == 1

# 4. Test Downloads
print("\n7. Testing Direct Download Endpoints:")
for preset in ["ecommerce", "healthcare", "fintech"]:
    res_json = client.get(f"/api/database/download-preset/{preset}")
    assert res_json.status_code == 200, f"JSON download failed for {preset}"
    print(f"   - /api/database/download-preset/{preset}: {len(res_json.data)} bytes OK")

    res_sql = client.get(f"/api/database/download-preset-sql/{preset}")
    assert res_sql.status_code == 200, f"SQL download failed for {preset}"
    print(f"   - /api/database/download-preset-sql/{preset}: {len(res_sql.data)} bytes OK")

    res_db = client.get(f"/api/database/download-preset-db/{preset}")
    assert res_db.status_code == 200, f"DB download failed for {preset}"
    print(f"   - /api/database/download-preset-db/{preset}: {len(res_db.data)} bytes OK")

# 5. Restore Fintech Preset
client.post("/api/database/load-preset/fintech")
print("\n8. Restored GlobalPay Fintech Master Preset!")
print("\n==================================================================")
print("ALL MULTI-DATASET & PRESET SYSTEM ENDPOINTS PASSED PERFECTLY!")
print("==================================================================")
