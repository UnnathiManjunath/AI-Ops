import urllib.request
import json

BASE_URL = "http://127.0.0.1:8080"

def test_scenario(fault_type, sub_type, name):
    print(f"\n--- Testing Scenario: {name} ({fault_type} / {sub_type}) ---")
    
    # 1. Inject fault
    req = urllib.request.Request(
        f"{BASE_URL}/api/inject-fault",
        data=json.dumps({"fault_type": fault_type, "sub_type": sub_type}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        inject_data = json.loads(resp.read().decode())
    
    incident_id = inject_data["incident_id"]
    print(f"Injected Incident ID: {incident_id}, code: {inject_data['incident_code']}")

    # 2. Diagnose
    with urllib.request.urlopen(f"{BASE_URL}/api/diagnose/{incident_id}") as resp:
        diag_data = json.loads(resp.read().decode())
    
    print(f"Risk Tier: {diag_data['risk_tier']}")
    print(f"Human Approval Required: {diag_data['requires_human_approval']}")
    print(f"Blast Radius: {diag_data['blast_radius_desc']}")

    # 3. Execute
    req = urllib.request.Request(
        f"{BASE_URL}/api/execute/{incident_id}",
        data=json.dumps({"force_fail": False}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        exec_data = json.loads(resp.read().decode())

    print(f"Execution Success: {exec_data.get('success')}")
    print(f"ITIL Change ID: {exec_data.get('change_id')}")
    print("PASS!")

if __name__ == "__main__":
    test_scenario("disk_overflow", "routine_hygiene", "Uncritical Disk Hygiene")
    test_scenario("worker_stuck", "routine_gc_trim", "Uncritical Worker Memory Trim")
    test_scenario("queue_growth", "routine_queue_balance", "Uncritical Queue Balance")
    test_scenario("ssl_expiry", "routine_audit_check", "Uncritical SSL Audit")
