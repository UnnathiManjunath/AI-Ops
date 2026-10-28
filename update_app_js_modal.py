import os

JS_PATH = r"C:\Users\Babitha M\.gemini\antigravity\scratch\safeops-ai\static\js\app.js"

with open(JS_PATH, "r", encoding="utf-8") as f:
    text = f.read()

start_marker = "// 13. Runbook Upload & Custom Ingestion Modal"
end_marker = "// -------------------------------------------------------------------------\n// 14. Interactive Problem Solver & Judge Showcase Walkthrough"

p1 = text.find(start_marker)
p2 = text.find(end_marker)

new_js = """// 13. Operational Database & SRE Dataset Upload Modal
// -------------------------------------------------------------------------
let selectedDatabaseFile = null;

function openDatabaseModal(focusTab = 'upload') {
  const modal = document.getElementById('uploadDatabaseModal');
  if (modal) modal.classList.remove('hidden');
  if (window.lucide) lucide.createIcons();
}

function closeDatabaseModal() {
  const modal = document.getElementById('uploadDatabaseModal');
  if (modal) modal.classList.add('hidden');
}

// Backward compatibility alias
function openUploadModal() { openDatabaseModal(); }
function closeUploadModal() { closeDatabaseModal(); }

function handleDatabaseFileSelection(event) {
  const file = event.target.files[0];
  if (!file) return;

  selectedDatabaseFile = file;
  const infoBox = document.getElementById('fileSelectionInfo');
  const nameElem = document.getElementById('selectedFileName');
  const sizeElem = document.getElementById('selectedFileSize');

  if (infoBox && nameElem && sizeElem) {
    infoBox.classList.remove('hidden');
    nameElem.textContent = file.name;
    const kb = (file.size / 1024).toFixed(1);
    sizeElem.textContent = `${kb} KB`;
  }
}

async function submitUploadedDatabase() {
  if (!selectedDatabaseFile) {
    showToast('No File Selected', 'Please choose a .db, .sqlite, .json, or .csv file to upload.', 'warning');
    return;
  }

  const formData = new FormData();
  formData.append('file', selectedDatabaseFile);

  try {
    showToast('Uploading Database...', `Ingesting ${selectedDatabaseFile.name}...`, 'info');
    const res = await fetch('/api/database/upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    if (data.success) {
      showToast('Database Ingested Successfully!', data.message, 'success');
      closeDatabaseModal();
      await fetchMetrics();
      await fetchIncidents();
      await fetchAuditLogs();
      if (window.confetti) confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
    } else {
      showToast('Upload Error', data.error || 'Failed to import database file.', 'error');
    }
  } catch (err) {
    showToast('Network Error', err.message, 'error');
  }
}

async function loadPrepackagedMasterDatabase() {
  try {
    showToast('Loading Master Database...', 'Restoring 18 SRE Runbooks & Scenario Policies...', 'info');
    const res = await fetch('/api/database/reset-master', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();

    if (data.success) {
      showToast('Master Database Active!', data.message, 'success');
      closeDatabaseModal();
      await fetchMetrics();
      await fetchIncidents();
      await fetchAuditLogs();
      if (window.confetti) confetti({ particleCount: 90, spread: 80, origin: { y: 0.6 } });
    } else {
      showToast('Reset Error', data.error || 'Failed to reset master database.', 'error');
    }
  } catch (err) {
    showToast('Network Error', err.message, 'error');
  }
}

"""

if p1 != -1 and p2 != -1:
    updated = text[:p1] + new_js + text[p2:]
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("static/js/app.js updated successfully with database modal handlers!")
else:
    print(f"Markers not found in app.js: p1={p1}, p2={p2}")
