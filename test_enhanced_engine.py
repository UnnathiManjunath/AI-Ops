import os, gzip, shutil, subprocess, math, collections

PROJECT_DIR = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai"
FS_BASE = os.path.join(PROJECT_DIR, "simulated_system", "var_log_app")
ARCHIVE_DIR = os.path.join(FS_BASE, "archive")

os.makedirs(FS_BASE, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

def calculate_entropy(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read(65536) # inspect first 64KB
        if not data:
            return 0.0
        counter = collections.Counter(data)
        length = len(data)
        entropy = 0.0
        for count in counter.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy / 8.0, 3) # normalized 0.0 to 1.0
    except Exception:
        return 0.5

print("Shannon entropy calculation defined successfully.")
