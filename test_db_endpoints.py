from app import app
import json
import os
import io

def test_database_routes():
    client = app.test_client()

    print("\n--- 1. Testing 1-Click Master Database Reset ---")
    res = client.post('/api/database/reset-master')
    assert res.status_code == 200, f"Reset failed: {res.data}"
    data = res.get_json()
    print("  [+] Success:", data.get('success'), "| Message:", data.get('message'))
    print("  [+] Active Runbooks Count:", data.get('runbooks_count'))
    assert data.get('runbooks_count') >= 14

    print("\n--- 2. Testing Database Export (.db) ---")
    res = client.get('/api/database/export')
    assert res.status_code == 200, f"Export DB failed: {res.status_code}"
    print(f"  [+] Downloaded DB bytes: {len(res.data)} bytes")

    print("\n--- 3. Testing Database Export JSON ---")
    res = client.get('/api/database/export-json')
    assert res.status_code == 200, f"Export JSON failed: {res.status_code}"
    json_data = json.loads(res.data)
    print("  [+] JSON dataset title:", json_data['metadata']['dataset_name'])
    print("  [+] Runbooks in JSON:", len(json_data['runbooks']))

    print("\n--- 4. Testing Upload JSON Dataset ---")
    sample_json = {
        "runbooks": [
            {
                "runbook_id": "RB-TEST-01",
                "title": "Custom Test Imported Runbook",
                "category": "Testing",
                "target_subsystem": "test-cluster",
                "trigger_condition": "test_metric > 90",
                "safe_action_tier": "Tier 1 (Low Risk - Safe Auto)",
                "blast_radius": "0%",
                "judgment_rules": "Test judgment policy",
                "remediation_command": "echo 'Testing'",
                "rollback_command": "echo 'Rollback'",
                "verification_check": "echo PASS"
            }
        ]
    }
    res = client.post('/api/database/upload', json=sample_json)
    assert res.status_code == 200, f"Upload JSON failed: {res.data}"
    upload_res = res.get_json()
    print("  [+] Upload JSON result:", upload_res.get('message'))

    print("\n--- 5. Testing Upload SQLite Binary (.db) ---")
    db_path = os.path.join(os.path.dirname(__file__), "safeops_master.db")
    with open(db_path, "rb") as f:
        db_bytes = f.read()
    
    data = {
        'file': (io.BytesIO(db_bytes), 'uploaded_test.db')
    }
    res = client.post('/api/database/upload', data=data, content_type='multipart/form-data')
    assert res.status_code == 200, f"Upload SQLite failed: {res.data}"
    sqlite_res = res.get_json()
    print("  [+] Upload SQLite result:", sqlite_res.get('message'))
    print("  [+] Restored Runbooks:", sqlite_res.get('runbooks_count'))

    print("\nALL DATABASE UPLOAD & EXPORT TESTS PASSED 100% PERFECTLY!")

if __name__ == "__main__":
    test_database_routes()
