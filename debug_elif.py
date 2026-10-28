with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('active_preset in ["it_sector", "it"]')
idx2 = text.find('PRESET 1: E-COMMERCE', idx)
print(text[idx2-50:idx2+200])
