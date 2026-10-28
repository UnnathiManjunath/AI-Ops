p = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py"

with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = "app.config['TEMPLATES_AUTO_RELOAD'] = True"
addition = """app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_cache_control_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response"""

if target in text and "add_cache_control_headers" not in text:
    text = text.replace(target, addition, 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print("Added anti-cache headers to app.py!")
else:
    print("Target already present or not found")
