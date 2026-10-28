with open(r'C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean showcase section at bottom
clean_start = text.rfind('<div class="bg-cyber-card border border-cyber-border rounded-xl p-5 shadow-2xl relative overflow-hidden"', 0, 90301)
# include comment if exists
c_idx = text.rfind('<!--', 0, clean_start)
if 'Section 1.5' in text[c_idx:clean_start]:
    clean_start = c_idx

clean_end = text.find('</main>', clean_start)
clean_showcase_html = text[clean_start:clean_end].strip()

# 2. Table section at top
table_start = text.find('<!-- Section 1.5: Interactive Problem Solver & Judge Showcase')
workflow_start = text.find('<div class="flex items-center space-x-2 overflow-x-auto')
# find comment before workflow_start
step_comment = text.rfind('<!--', 0, workflow_start)

print('table_start:', table_start)
print('step_comment (before workflow):', step_comment)
print('Length of clean_showcase_html:', len(clean_showcase_html))

# Build new HTML:
# Part 1: from 0 to table_start
part1 = text[:table_start]
# Part 2: clean_showcase_html + newline
part2 = clean_showcase_html + '\n\n    '
# Part 3: from step_comment to clean_start (everything in between: Stepper, Telemetry, Scenarios, AI Diagnosis, Terminal, Subsystem, Audit)
part3 = text[step_comment:clean_start].rstrip()
# Part 4: from clean_end to end of file (</main> + modals + scripts)
part4 = '\n\n  ' + text[clean_end:]

new_html = part1 + part2 + part3 + part4

# Remove 'Upload Runbook' button from header so it matches the image exactly
old_rb_btn = '''<!-- Upload Runbook Button -->
        <button onclick="openRunbookUploadModal()" class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition shadow-md shadow-emerald-600/30 text-xs" title="Upload custom runbook or parse prose">
          <i data-lucide="book-plus" class="w-4 h-4"></i>
          <span>Upload Runbook</span>
        </button>

        '''
new_html = new_html.replace(old_rb_btn, '')

with open(r'C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('SUCCESS! New HTML length:', len(new_html))
