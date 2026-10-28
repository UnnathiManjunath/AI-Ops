with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('active_preset in ["it_sector", "it"]')
print(text[idx:idx+2500])
