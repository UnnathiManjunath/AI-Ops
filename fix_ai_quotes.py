with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\ai_engine.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'print "PASS_DISK_HEALTHY"' in line:
        line = line.replace('print "PASS_DISK_HEALTHY"', 'print \\"PASS_DISK_HEALTHY\\"')
    if 'gsub("%", ""); if ($5 < 80) print "PASS"; else print "FAIL"' in line:
        line = line.replace('gsub("%", ""); if ($5 < 80) print "PASS"; else print "FAIL"', 'gsub(\\"%\\", \\"\\"); if ($5 < 80) print \\"PASS\\"; else print \\"FAIL\\"')
    if 'gsub("%", ""); if ($5 < 75) print "PASS"; else print "FAIL"' in line:
        line = line.replace('gsub("%", ""); if ($5 < 75) print "PASS"; else print "FAIL"', 'gsub(\\"%\\", \\"\\"); if ($5 < 75) print \\"PASS\\"; else print \\"FAIL\\"')
    if 'gsub("%", ""); if ($5 < 85) print "PASS"; else print "FAIL"' in line:
        line = line.replace('gsub("%", ""); if ($5 < 85) print "PASS"; else print "FAIL"', 'gsub(\\"%\\", \\"\\"); if ($5 < 85) print \\"PASS\\"; else print \\"FAIL\\"')
    new_lines.append(line)

with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\ai_engine.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Safely replaced quotes in ai_engine.py")
