import json
from app import app

client = app.test_client()

print("Testing /api/filesystem/inventory...")
r1 = client.get("/api/filesystem/inventory")
assert r1.status_code == 200, f"Error {r1.status_code}"
d1 = r1.get_json()
print(f"Inventory: {len(d1['files'])} files. Base path: {d1['base_path']}")
assert len(d1['files']) > 0, "No files found!"

print("\nTesting /api/filesystem/execute-zip...")
r2 = client.post("/api/filesystem/execute-zip")
assert r2.status_code == 200, f"Error {r2.status_code}"
d2 = r2.get_json()
print(f"Zipped: Reclaimed {d2['reclaimed_mb']}. Archive: {d2['archive_directory']}")

print("\nTesting /api/filesystem/inventory after zip...")
r3 = client.get("/api/filesystem/inventory")
d3 = r3.get_json()
gz_files = [f for f in d3['files'] if f['is_compressed']]
print(f"Found {len(gz_files)} compressed .gz files in archive!")
assert len(gz_files) >= 1, "Expected .gz files!"

print("\nTesting /api/filesystem/execute-rollback...")
r4 = client.post("/api/filesystem/execute-rollback")
assert r4.status_code == 200
d4 = r4.get_json()
print(f"Rollback: Restored {len(d4['restored_files'])} files.")

print("\nTesting /api/subsystem-architecture...")
r5 = client.get("/api/subsystem-architecture")
assert r5.status_code == 200
d5 = r5.get_json()
print(f"Architecture Matrix: {len(d5['matrix'])} problem layers detailed.")

print("\nTesting /api/subsystem-state/disk_overflow...")
r6 = client.get("/api/subsystem-state/disk_overflow")
assert r6.status_code == 200
d6 = r6.get_json()
print(f"Subsystem disk state: {d6['type']} - {d6['metric_val']}")
print(f"Layer: {d6['subsystem_layer']['os_layer']}")

print("\nTesting /api/subsystem-state/worker_stuck...")
r7 = client.get("/api/subsystem-state/worker_stuck")
assert r7.status_code == 200
d7 = r7.get_json()
print(f"Subsystem worker state: {d7['type']} - {d7['metric_val']}")
print(f"Layer: {d7['subsystem_layer']['os_layer']}")

print("\nALL BACKEND SUBSYSTEM & REAL FILESYSTEM TESTS PASSED WITH 100% SUCCESS!")
