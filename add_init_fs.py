p = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\static\js\app.js"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = "fetchAuditLogs();"
addition = "\n  loadRealFilesystem();"

if target in text:
    text = text.replace(target, target + addition, 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print("Added loadRealFilesystem() to DOMContentLoaded!")
else:
    print("Target not found")
