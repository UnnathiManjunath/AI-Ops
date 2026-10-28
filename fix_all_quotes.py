import py_compile

AI_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\ai_engine.py"

with open(AI_PATH, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('print("Terminated 42 idle DB connections");', 'print(\\"Terminated 42 idle DB connections\\");')

with open(AI_PATH, "w", encoding="utf-8") as f:
    f.write(text)

try:
    py_compile.compile(AI_PATH, doraise=True)
    print("ai_engine.py compiled cleanly with zero syntax errors!")
except Exception as e:
    print("Compilation error:", e)
