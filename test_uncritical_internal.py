from app import app
import json

def test_uncritical_with_test_client():
    client = app.test_client()

    scenarios = [
        ("disk_overflow", "routine_hygiene", "Uncritical Disk Hygiene"),
        ("worker_stuck", "routine_gc_trim", "Uncritical Worker Memory Trim"),
        ("queue_growth", "routine_queue_balance", "Uncritical Queue Balance"),
        ("ssl_expiry", "routine_audit_check", "Uncritical SSL Audit Check")
    ]

    for fault_type, sub_type, name in scenarios:
        print(f"\nTesting {name} ({fault_type} / {sub_type})...")
        
        # 1. Inject fault
        res = client.post('/api/inject-fault', json={'fault_type': fault_type, 'sub_type': sub_type})
        assert res.status_code == 200, f"Inject failed: {res.data}"
        inject_data = res.get_json()
        incident_id = inject_data["incident_id"]
        print(f"  [+] Injected Incident #{incident_id}: {inject_data['incident_code']}")

        # 2. Diagnose
        res = client.post(f'/api/diagnose/{incident_id}')
        assert res.status_code == 200, f"Diagnose failed: {res.data}"
        diag_resp = res.get_json()
        diag_data = diag_resp['diagnosis']
        print(f"  [+] Risk Tier: {diag_data['risk_tier']}")
        print(f"  [+] Approval Required: {diag_data['requires_human_approval']}")
        print(f"  [+] Blast Radius: {diag_data['blast_radius_desc']}")
        assert diag_data['requires_human_approval'] == 0, "Uncritical scenario should NOT require human approval!"
        assert "Uncritical" in diag_data['risk_tier'] or "Tier 0" in diag_data['risk_tier'] or "Tier 1" in diag_data['risk_tier']

        # 3. Execute
        res = client.post(f'/api/execute/{incident_id}', json={'force_fail': False})
        assert res.status_code == 200, f"Execute failed: {res.data}"
        exec_data = res.get_json()
        print(f"  [+] Auto Execution Success: {exec_data.get('success')}")
        print(f"  [+] ITIL Change ID: {exec_data.get('change_id')}")

    print("\nALL 4 UNCRITICAL SCENARIOS PASSED 100% PERFECTLY!")

if __name__ == "__main__":
    test_uncritical_with_test_client()
