<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STLS PAT Certificate Generator</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #f0f2f5;
    color: #1a1a2e;
    min-height: 100vh;
  }

  /* Header */
  header {
    background: #1a1a2e;
    padding: 16px 32px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }
  header .logo-ring {
    width: 36px; height: 36px;
    border: 3px solid #00bfff;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
  }
  header .logo-ring span {
    width: 14px; height: 14px;
    border: 2px solid #00bfff;
    border-radius: 50%;
  }
  header h1 { color: #fff; font-size: 18px; font-weight: 700; letter-spacing: 0.5px; }
  header p  { color: #8899aa; font-size: 13px; margin-top: 1px; }

  /* Main layout */
  main { max-width: 1400px; margin: 0 auto; padding: 32px 24px; }

  /* Upload zone */
  #upload-zone {
    border: 2px dashed #c0c8d8;
    border-radius: 12px;
    background: #fff;
    text-align: center;
    padding: 48px 32px;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    margin-bottom: 28px;
  }
  #upload-zone:hover, #upload-zone.drag-over {
    border-color: #00bfff;
    background: #f0fbff;
  }
  #upload-zone .icon { font-size: 40px; margin-bottom: 12px; }
  #upload-zone h2 { font-size: 17px; color: #1a1a2e; margin-bottom: 6px; }
  #upload-zone p  { font-size: 13px; color: #778899; }
  #upload-zone input { display: none; }

  /* Status bar */
  #status-bar {
    display: none;
    background: #fff;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  #status-bar.hidden { display: none !important; }
  #status-bar .dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #00c87a;
    flex-shrink: 0;
  }
  #status-bar .info { flex: 1; font-size: 13px; color: #445; }
  #status-bar .info strong { color: #1a1a2e; }

  /* Toolbar */
  #toolbar {
    display: none;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    align-items: center;
  }
  #toolbar.visible { display: flex; }

  .btn {
    padding: 9px 18px;
    border-radius: 8px;
    border: none;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.1s, box-shadow 0.1s;
  }
  .btn:active { transform: scale(0.97); }
  .btn-primary   { background: #1a1a2e; color: #fff; }
  .btn-primary:hover { background: #2a2a4e; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
  .btn-secondary { background: #fff; color: #1a1a2e; border: 1.5px solid #c0c8d8; }
  .btn-secondary:hover { border-color: #00bfff; color: #00bfff; }
  .btn-green  { background: #00c87a; color: #fff; }
  .btn-green:hover  { background: #00a864; box-shadow: 0 2px 8px rgba(0,200,122,0.3); }
  .btn-blue   { background: #00bfff; color: #fff; }
  .btn-blue:hover   { background: #009fd4; box-shadow: 0 2px 8px rgba(0,191,255,0.3); }
  .btn-danger { background: #ff4d6d; color: #fff; }

  .toolbar-sep { flex: 1; }

  /* Search box */
  #search-wrap { position: relative; }
  #search-wrap input {
    padding: 8px 12px 8px 34px;
    border-radius: 8px;
    border: 1.5px solid #c0c8d8;
    font-size: 13px;
    width: 220px;
    outline: none;
  }
  #search-wrap input:focus { border-color: #00bfff; }
  #search-wrap .search-icon {
    position: absolute; left: 10px; top: 50%;
    transform: translateY(-50%);
    color: #778899; font-size: 14px;
    pointer-events: none;
  }

  /* Table */
  #table-wrap {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    overflow: auto;
    max-height: 65vh;
    display: none;
  }
  #table-wrap.visible { display: block; }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  thead th {
    background: #1a1a2e;
    color: #fff;
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 2;
    white-space: nowrap;
  }
  thead th:first-child { border-radius: 12px 0 0 0; }
  thead th:last-child  { border-radius: 0 12px 0 0; }

  tbody tr { border-bottom: 1px solid #eef0f4; }
  tbody tr:hover { background: #f7f9fc; }
  tbody tr.fail-row td:nth-child(9) { color: #e02020; font-weight: 700; }
  tbody tr.location-row td {
    background: #e8f4ff;
    font-weight: 700;
    color: #1a1a2e;
    font-size: 12px;
    padding: 6px 12px;
  }

  td { padding: 6px 8px; vertical-align: middle; }

  /* Editable cells */
  td input, td select {
    width: 100%;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 13px;
    background: transparent;
    font-family: inherit;
    color: inherit;
    outline: none;
    transition: border-color 0.15s, background 0.15s;
  }
  td input:focus, td select:focus {
    border-color: #00bfff;
    background: #f0fbff;
  }
  td select { cursor: pointer; }
  td select.pass  { color: #1a7a40; font-weight: 600; }
  td select.fail  { color: #c0000c; font-weight: 700; }

  /* Add / delete row buttons */
  .row-del {
    background: none; border: none; cursor: pointer;
    color: #cc3333; font-size: 16px; padding: 2px 6px;
    border-radius: 4px; line-height: 1;
  }
  .row-del:hover { background: #ffecec; }

  /* Pagination / count */
  #table-footer {
    display: none;
    padding: 10px 16px;
    font-size: 12px;
    color: #778899;
    background: #fff;
    border-top: 1px solid #eef0f4;
    border-radius: 0 0 12px 12px;
  }
  #table-footer.visible { display: block; }

  /* Generate panel */
  #gen-panel {
    display: none;
    background: #fff;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
  }
  #gen-panel.visible { display: flex; }
  #gen-panel h3 { font-size: 14px; color: #1a1a2e; margin-right: 4px; }
  #gen-panel p  { font-size: 12px; color: #778899; margin-top: 2px; }

  /* Toast */
  #toast {
    position: fixed; bottom: 24px; right: 24px;
    background: #1a1a2e; color: #fff;
    padding: 12px 20px; border-radius: 10px;
    font-size: 13px; font-weight: 500;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    opacity: 0; transform: translateY(8px);
    transition: opacity 0.2s, transform 0.2s;
    pointer-events: none; z-index: 999;
  }
  #toast.show { opacity: 1; transform: translateY(0); }

  /* Loading spinner */
  .spinner {
    display: inline-block; width: 14px; height: 14px;
    border: 2px solid rgba(255,255,255,0.4);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    vertical-align: middle; margin-right: 6px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>

<header>
  <div class="logo-ring"><span></span></div>
  <div>
    <h1>STLS PAT Certificate Generator</h1>
    <p>Upload a .sss file, edit records, then generate your certificate</p>
  </div>
</header>

<main>

  <!-- Upload -->
  <div id="upload-zone">
    <input type="file" id="file-input" accept=".sss">
    <div class="icon">📂</div>
    <h2>Drop your .sss file here, or click to browse</h2>
    <p>Seaward Apollo test results file (.sss)</p>
  </div>

  <!-- Status -->
  <div id="status-bar" class="hidden">
    <div class="dot"></div>
    <div class="info">
      <strong id="status-filename"></strong>
      <span id="status-count"></span>
    </div>
    <button class="btn btn-secondary" onclick="resetApp()">Load different file</button>
  </div>

  <!-- Toolbar -->
  <div id="toolbar">
    <div id="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="search-input" placeholder="Search records..." oninput="filterTable()">
    </div>
    <button class="btn btn-secondary" onclick="addRow()">+ Add row</button>
    <div class="toolbar-sep"></div>
    <span id="record-count" style="font-size:13px;color:#778899;"></span>
  </div>

  <!-- Table -->
  <div id="table-wrap">
    <table id="records-table">
      <thead>
        <tr>
          <th style="width:32px"></th>
          <th>Asset ID</th>
          <th>Description</th>
          <th>Notes</th>
          <th>Test Date</th>
          <th>Site</th>
          <th>Sub-Location</th>
          <th>Engineer</th>
          <th>Result</th>
          <th>Earth (ohm)</th>
          <th>Insulation</th>
          <th>Test Type</th>
        </tr>
      </thead>
      <tbody id="table-body"></tbody>
    </table>
    <div id="table-footer"></div>
  </div>

  <!-- Generate panel -->
  <div id="gen-panel">
    <div>
      <h3>Generate Certificate</h3>
      <p>All edits are included in the output</p>
    </div>
    <button class="btn btn-green" onclick="generateCert('simple')">
      📄 Simple Report
    </button>
    <button class="btn btn-blue" onclick="generateCert('full')">
      📋 Full Certificate
    </button>
  </div>

</main>

<div id="toast"></div>

<script>
let allRecords = [];
let deviceModel = '';

// ---------------------------------------------------------------------------
// Upload
// ---------------------------------------------------------------------------
const zone  = document.getElementById('upload-zone');
const input = document.getElementById('file-input');

zone.addEventListener('click', () => input.click());
zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
zone.addEventListener('drop', e => {
  e.preventDefault();
  zone.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
input.addEventListener('change', () => { if (input.files[0]) handleFile(input.files[0]); });

async function handleFile(file) {
  if (!file.name.endsWith('.sss')) { toast('Please upload a .sss file', true); return; }

  toast('Parsing file...');
  const fd = new FormData();
  fd.append('file', file);

  try {
    const res  = await fetch('/upload', { method: 'POST', body: fd });
    const data = await res.json();
    if (data.error) { toast(data.error, true); return; }

    allRecords  = data.records;
    deviceModel = data.device;

    document.getElementById('status-filename').textContent = file.name + '  ';
    document.getElementById('status-count').textContent    = `${data.count} records loaded`;
    document.getElementById('status-bar').classList.remove('hidden');
    zone.style.display = 'none';

    document.getElementById('toolbar').classList.add('visible');
    document.getElementById('table-wrap').classList.add('visible');
    document.getElementById('table-footer').classList.add('visible');
    document.getElementById('gen-panel').classList.add('visible');

    renderTable(allRecords);
    toast(`${data.count} records loaded successfully`);
  } catch(e) {
    toast('Something went wrong parsing the file', true);
  }
}

// ---------------------------------------------------------------------------
// Render table
// ---------------------------------------------------------------------------
function renderTable(records) {
  const tbody = document.getElementById('table-body');
  tbody.innerHTML = '';

  records.forEach((rec, idx) => {
    const tr = document.createElement('tr');
    if (rec.result === 'Fail') tr.classList.add('fail-row');
    tr.dataset.idx = idx;

    tr.innerHTML = `
      <td><button class="row-del" title="Delete row" onclick="deleteRow(${idx})">✕</button></td>
      <td><input value="${esc(rec.rec_id)}"    onchange="updateField(${idx},'rec_id',this.value)"></td>
      <td><input value="${esc(rec.desc)}"      onchange="updateField(${idx},'desc',this.value)"></td>
      <td><input value="${esc(rec.notes)}"     onchange="updateField(${idx},'notes',this.value)"></td>
      <td><input value="${esc(rec.date)}"      onchange="updateField(${idx},'date',this.value)"></td>
      <td><input value="${esc(rec.location)}"  onchange="updateField(${idx},'location',this.value)"></td>
      <td><input value="${esc(rec.subloc)}"    onchange="updateField(${idx},'subloc',this.value)"></td>
      <td><input value="${esc(rec.engineer)}"  onchange="updateField(${idx},'engineer',this.value)"></td>
      <td>
        <select class="${rec.result === 'Pass' ? 'pass' : 'fail'}"
                onchange="updateField(${idx},'result',this.value); this.className=this.value==='Pass'?'pass':'fail'; if(this.value==='Fail'){this.closest('tr').classList.add('fail-row')}else{this.closest('tr').classList.remove('fail-row')}">
          <option ${rec.result==='Pass'?'selected':''}>Pass</option>
          <option ${rec.result==='Fail'?'selected':''}>Fail</option>
        </select>
      </td>
      <td><input value="${esc(rec.earth_ohm)}"  onchange="updateField(${idx},'earth_ohm',this.value)"></td>
      <td><input value="${esc(rec.insulation)}" onchange="updateField(${idx},'insulation',this.value)"></td>
      <td><input value="${esc(rec.test_type)}"  onchange="updateField(${idx},'test_type',this.value)"></td>
    `;
    tbody.appendChild(tr);
  });

  document.getElementById('record-count').textContent = `${records.length} records`;
  document.getElementById('table-footer').textContent  = `Showing ${records.length} of ${allRecords.length} records`;
}

function esc(v) {
  return String(v || '').replace(/"/g, '&quot;').replace(/</g, '&lt;');
}

function updateField(idx, field, value) {
  allRecords[idx][field] = value;
}

function deleteRow(idx) {
  allRecords.splice(idx, 1);
  renderTable(allRecords);
  toast('Row deleted');
}

function addRow() {
  // Clone the last record as a template
  const last = allRecords[allRecords.length - 1] || {};
  allRecords.push({
    rec_id: '', desc: '', notes: '', date: last.date || '',
    location: last.location || '', subloc: last.subloc || '',
    engineer: last.engineer || '', result: 'Pass',
    earth_ohm: '', insulation: '', test_type: last.test_type || '',
    device: deviceModel,
  });
  renderTable(allRecords);
  // Scroll to bottom and focus new row
  const tbody = document.getElementById('table-body');
  const lastRow = tbody.lastElementChild;
  lastRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
  lastRow.querySelector('input').focus();
  toast('New row added');
}

// ---------------------------------------------------------------------------
// Search / filter
// ---------------------------------------------------------------------------
function filterTable() {
  const q = document.getElementById('search-input').value.toLowerCase();
  if (!q) { renderTable(allRecords); return; }
  const filtered = allRecords.filter(r =>
    Object.values(r).some(v => String(v).toLowerCase().includes(q))
  );
  renderTable(filtered);
}

// ---------------------------------------------------------------------------
// Generate PDF
// ---------------------------------------------------------------------------
async function generateCert(type) {
  const btn = event.target;
  const orig = btn.innerHTML;
  btn.innerHTML = `<span class="spinner"></span> Generating...`;
  btn.disabled = true;

  try {
    const res = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ records: allRecords, type })
    });

    if (!res.ok) {
      const err = await res.json();
      toast(err.error || 'Failed to generate PDF', true);
      return;
    }

    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `PAT_${type}_${new Date().toISOString().slice(0,10)}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
    toast(`${type === 'simple' ? 'Simple report' : 'Full certificate'} downloaded`);
  } catch(e) {
    toast('Something went wrong generating the PDF', true);
  } finally {
    btn.innerHTML = orig;
    btn.disabled  = false;
  }
}

// ---------------------------------------------------------------------------
// Reset
// ---------------------------------------------------------------------------
function resetApp() {
  allRecords = [];
  document.getElementById('table-body').innerHTML = '';
  document.getElementById('toolbar').classList.remove('visible');
  document.getElementById('table-wrap').classList.remove('visible');
  document.getElementById('table-footer').classList.remove('visible');
  document.getElementById('gen-panel').classList.remove('visible');
  document.getElementById('status-bar').classList.add('hidden');
  zone.style.display = '';
  input.value = '';
  document.getElementById('search-input').value = '';
}

// ---------------------------------------------------------------------------
// Toast
// ---------------------------------------------------------------------------
function toast(msg, isError=false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.background = isError ? '#c0000c' : '#1a1a2e';
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}
</script>
</body>
</html>
