import os

AI_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\ai_engine.py"

with open(AI_PATH, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('"verification_check": "df -h / | awk \'NR==2 {print "PASS_DISK_HEALTHY"}\'",', '"verification_check": "df -h / | awk \'NR==2 {print \\"PASS_DISK_HEALTHY\\"}\'",')

with open(AI_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Escaped quote in ai_engine.py!")
