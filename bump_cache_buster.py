p = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('app.js?v=20261029_0130', 'app.js?v=20261029_0135')
with open(p, "w", encoding="utf-8") as f:
    f.write(text)
print("Updated cache buster query string in templates/index.html!")
