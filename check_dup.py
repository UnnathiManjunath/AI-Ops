with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html", "r", encoding="utf-8") as f:
    text = f.read()

p = 96050
end_idx = text.find('</body>', p)
print(text[p:p+300])
print('...')
print(text[end_idx-200:end_idx])
