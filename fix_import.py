import os

APP_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("import zipfile\n", "import zipfile\nimport shutil\n")

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("import shutil added!")
