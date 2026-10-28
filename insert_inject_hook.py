p = r'C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\app.py'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")'
addition = '''
    if fault_type == "disk_overflow":
        try:
            real_filesystem_engine.execute_real_rollback()
            real_filesystem_engine.generate_sample_files()
        except Exception:
            pass'''

if target in text:
    text = text.replace(target, target + addition, 1)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully inserted disk_overflow hook into inject_fault!')
else:
    print('Target not found')
