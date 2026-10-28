with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py", "r", encoding="utf-8") as f:
    app_text = f.read()

app_text = app_text.replace(
    '# PRESET 1: E-COMMERCE & FOOD DELIVERY (QUICKCART)\n    # =========================================================================\n    if active_preset == "ecommerce":',
    '# PRESET 1: E-COMMERCE & FOOD DELIVERY (QUICKCART)\n    # =========================================================================\n    elif active_preset == "ecommerce":'
)

with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py", "w", encoding="utf-8") as f:
    f.write(app_text)

with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\ai_engine.py", "r", encoding="utf-8") as f:
    ai_text = f.read()

ai_text = ai_text.replace(
    '# 1. QUICKCART E-COMMERCE & FOOD DELIVERY CLOUD\n    # =========================================================================\n    if active_preset == "ecommerce":',
    '# 1. QUICKCART E-COMMERCE & FOOD DELIVERY CLOUD\n    # =========================================================================\n    elif active_preset == "ecommerce":'
)

with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\ai_engine.py", "w", encoding="utf-8") as f:
    f.write(ai_text)

print("Changed 'if active_preset == ecommerce' to 'elif' in both files!")
