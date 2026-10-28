with open(r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html", "r", encoding="utf-8") as f:
    text = f.read()

m2 = text.find('runbooksModal')
print('runbooksModal pos:', m2)

m3_1 = text.find('uploadRunbookModal')
print('first uploadRunbookModal pos:', m3_1)

m3_2 = text.find('uploadRunbookModal', m3_1 + 20)
print('second uploadRunbookModal pos:', m3_2)

m_end = text.find('</body>')
print('body end:', m_end)
