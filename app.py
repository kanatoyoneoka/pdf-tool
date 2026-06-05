<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌸 PDFツール</title>
<script src="https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>
<script src="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.min.js"></script>
<script src="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #fff8fb; font-family: 'Helvetica Neue', Arial, sans-serif; color: #7a2e5e; min-height: 100vh; }
  h1 { text-align: center; color: #d96ea0; padding: 28px 0 6px; font-size: 1.8rem; }
  .subtitle { text-align: center; color: #b07aad; font-size: 0.9rem; margin-bottom: 24px; }
  .container { max-width: 960px; margin: 0 auto; padding: 0 16px; }
  .tabs { display: flex; gap: 8px; margin-bottom: 28px; justify-content: center; }
  .tab-btn { background: #fde8f3; border: 2px solid #f9b8d8; border-radius: 24px; padding: 10px 32px; font-size: 1rem; font-weight: bold; color: #b07aad; cursor: pointer; transition: all 0.2s; }
  .tab-btn.active { background: #f9b8d8; color: #7a2e5e; border-color: #f490c0; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }
  .drop-zone { border: 3px dashed #f9b8d8; border-radius: 20px; background: #fde8f3; padding: 40px 24px; text-align: center; max-width: 600px; margin: 0 auto 32px; transition: all 0.2s; }
  .drop-zone.dragover { background: #fcd0e8; border-color: #f490c0; }
  .drop-zone-title { color: #c762a0; font-size: 1.1rem; font-weight: bold; margin-bottom: 8px; }
  .drop-zone-sub { color: #b07aad; font-size: 0.85rem; display: block; margin-bottom: 16px; }
  .select-btn { display: inline-block; background: #f9b8d8; color: #7a2e5e; border: none; border-radius: 20px; padding: 8px 28px; font-size: 0.95rem; font-weight: bold; cursor: pointer; }
  .select-btn:hover { background: #f490c0; color: white; }
  .section-title { color: #c762a0; font-size: 1.1rem; font-weight: bold; border-left: 5px solid #f9b8d8; padding-left: 10px; margin-bottom: 12px; }

  /*操作バー */
  .sel-bar { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; background: #fde8f3; border: 2px solid #f9b8d8; border-radius: 14px; padding: 9px 14px; margin-bottom: 10px; }
  .sel-bar-label { color: #c762a0; font-size: 0.88rem; font-weight: bold; }
  .sel-bar-btn { background: white; border: 2px solid #f9b8d8; border-radius: 16px; padding: 4px 14px; font-size: 0.85rem; font-weight: bold; color: #b07aad; cursor: pointer; }
  .sel-bar-btn:hover { background: #f9b8d8; color: #7a2e5e; }
  .sel-rotate-btn { background: white; border: 2px solid #f9b8d8; border-radius: 16px; padding: 4px 14px; font-size: 0.88rem; font-weight: bold; color: #c762a0; cursor: pointer; }
  .sel-rotate-btn:hover { background: #f9b8d8; color: #7a2e5e; }
  .sel-count { color: #d96ea0; font-size: 0.85rem; font-weight: bold; margin-left: auto; }
  .hint-text { color: #b07aad; font-size: 0.8rem; margin-bottom: 14px; }

  .pages-grid { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 32px; }

  .page-card { background: white; border: 2px solid #f9b8d8; border-radius: 16px; width: 160px; padding: 10px; text-align: center; user-select: none; position: relative; transition: box-shadow 0.2s, border-color 0.15s; }
  .page-card:hover { box-shadow: 0 4px 16px #f9b8d840; }
  .page-card.selected { border-color: #f490c0; background: #fff0f8; box-shadow: 0 0 0 3px #f9b8d8; }
  .page-card.drag-over { border-color: #f490c0; background: #fde8f3; }
  .page-card.dragging { opacity: 0.4; }

  /* チェックボックス */
  .page-checkbox-wrap { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; }
  .page-checkbox { width: 18px; height: 18px; accent-color: #f490c0; cursor: pointer; flex-shrink: 0; }
  .page-checkbox-label { color: #c762a0; font-size: 0.75rem; cursor: pointer; }

  /* ドラッグハンドル */
  .drag-handle { position: absolute; top: 8px; right: 8px; color: #d9b8d0; font-size: 0.85rem; cursor: grab; padding: 2px 3px; line-height: 1; }
  .drag-handle:active { cursor: grabbing; }

  .page-canvas-wrap { width: 100%; min-height: 80px; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; pointer-events: none; }
  .page-canvas-wrap canvas { width: 100%; border-radius: 8px; display: block; }

  .rotate-buttons { display: flex; justify-content: center; gap: 8px; }
  .rotate-btn { background: #fde8f3; border: 1px solid #f9b8d8; border-radius: 50%; width: 32px; height: 32px; font-size: 1rem; cursor: pointer; color: #c762a0; display: flex; align-items: center; justify-content: center; }
  .rotate-btn:hover { background: #f9b8d8; color: #7a2e5e; }

  /* 結合タブ */
  .merge-file-section { background: white; border: 2px solid #f9b8d8; border-radius: 16px; padding: 16px; margin-bottom: 20px; }
  .merge-file-header { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; cursor: grab; padding: 6px 8px; border-radius: 10px; background: #fde8f3; }
  .merge-file-header:hover { background: #fcd0e8; }
  .merge-file-header.dragging { opacity: 0.4; }
  .merge-file-header.drag-over { outline: 2px dashed #f490c0; }
  .merge-file-name { font-weight: bold; color: #c762a0; font-size: 0.95rem; flex: 1; }
  .merge-file-pages { color: #b07aad; font-size: 0.8rem; }
  .remove-file-btn { background: #fde8f3; border: 1px solid #f9b8d8; border-radius: 50%; width: 28px; height: 28px; font-size: 0.9rem; cursor: pointer; color: #c762a0; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .remove-file-btn:hover { background: #f9b8d8; color: #7a2e5e; }

  .btn-area { text-align: center; margin-bottom: 24px; }
  .download-btn { background: #f9b8d8; color: #7a2e5e; border: none; border-radius: 24px; padding: 14px 48px; font-size: 1.1rem; font-weight: bold; cursor: pointer; }
  .download-btn:hover:not(:disabled) { background: #f490c0; color: white; }
  .download-btn:disabled { opacity: 0.6; cursor: not-allowed; }

  #loading { display: none; text-align: center; color: #c762a0; font-size: 1rem; margin: 24px 0; }
  .spinner { display: inline-block; width: 32px; height: 32px; border: 4px solid #f9b8d8; border-top-color: #d96ea0; border-radius: 50%; animation: spin 0.8s linear infinite; vertical-align: middle; margin-right: 8px; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .success-msg { display: none; text-align: center; color: #2e7a52; background: #e8f8ee; border: 1px solid #a0e0bc; border-radius: 12px; padding: 12px 24px; margin: 16px auto; max-width: 500px; font-weight: bold; }
  .error-msg { display: none; text-align: center; color: #7a2e2e; background: #f8e8e8; border: 1px solid #e0a0a0; border-radius: 12px; padding: 12px 24px; margin: 16px auto; max-width: 500px; font-weight: bold; word-break: break-all; }
</style>
</head>
<body>
<div class="container">
  <h1>🌸 PDFツール 🌸</h1>
  <p class="subtitle">並び替え・回転・PDF結合ができます</p>

  <div class="tabs">
    <button class="tab-btn active" type="button" onclick="switchTab('sort')">🔀 並び替え・回転</button>
    <button class="tab-btn" type="button" onclick="switchTab('merge')">📎 PDF結合</button>
  </div>

  <div id="loading"><span class="spinner"></span>読み込み中...🌸</div>

  <!-- 並び替えタブ -->
  <div id="tab-sort" class="tab-content active">
    <div class="drop-zone" id="sort-drop-zone">
      <div class="drop-zone-title">📄ここにPDFをドロップ</div>
      <span class="drop-zone-sub">またはボタンからファイルを選択</span>
      <button class="select-btn" type="button" onclick="document.getElementById('sort-file-input').click()">📂ファイルを選択</button><input type="file" id="sort-file-input" accept=".pdf" style="display:none;">
    </div>
    <div id="sort-pages-section" style="display:none;">
      <p class="section-title">📋 ページ一覧</p>
      <div class="sel-bar">
        <span class="sel-bar-label">選択：</span>
        <button class="sel-bar-btn" type="button" onclick="sortSelectAll()">全選択</button>
        <button class="sel-bar-btn" type="button" onclick="sortDeselectAll()">全解除</button>
        <span style="width:1px;height:20px;background:#f9b8d8;display:inline-block;margin:0 4px;"></span>
        <button class="sel-rotate-btn" type="button" onclick="sortRotateSelected(-90)">↺ 選択を左回転</button>
        <button class="sel-rotate-btn" type="button" onclick="sortRotateSelected(90)">↻ 選択を右回転</button>
        <span class="sel-count" id="sort-sel-count">0ページ選択中</span>
      </div>
      <p class="hint-text">💡 チェックボックスで複数選択 → 上のバーで回転。☰ をドラッグで並び替え。</p>
      <div class="pages-grid" id="sort-pages-grid"></div>
      <div class="btn-area">
        <button class="download-btn" id="sort-download-btn" type="button" onclick="generateSortPDF()">📥 PDFを出力する</button>
      </div><div class="success-msg" id="sort-success-msg">🌸 ダウンロードを開始しました！</div>
      <div class="error-msg" id="sort-error-msg"></div>
    </div>
  </div>

  <!-- 結合タブ -->
  <div id="tab-merge" class="tab-content">
    <div class="drop-zone" id="merge-drop-zone">
      <div class="drop-zone-title">📄 PDFを複数ドロップ orボタンから追加</div>
      <span class="drop-zone-sub">何度でも追加できます</span>
      <button class="select-btn" type="button" onclick="document.getElementById('merge-file-input').click()">📂 ファイルを選択</button>
      <input type="file" id="merge-file-input" accept=".pdf" multiple style="display:none;">
    </div>
    <div id="merge-pages-section" style="display:none;">
      <p class="section-title">📋 ファイル一覧</p>
      <div id="merge-files-list"></div>
      <div class="btn-area">
        <button class="download-btn" id="merge-download-btn" type="button" onclick="generateMergePDF()">📎 結合してダウンロード</button>
      </div>
      <div class="success-msg" id="merge-success-msg">🌸 結合完了！ダウンロードを開始しました！</div>
      <div class="error-msg" id="merge-error-msg"></div>
    </div>
  </div>
</div>

<script>
pdfjsLib.GlobalWorkerOptions.workerSrc = '';

//=====================
// タブ切り替え
// =====================
function switchTab(name) {
  document.querySelectorAll('.tab-btn')[0].classList.toggle('active', name === 'sort');
  document.querySelectorAll('.tab-btn')[1].classList.toggle('active', name === 'merge');
  document.getElementById('tab-sort').classList.toggle('active', name === 'sort');
  document.getElementById('tab-merge').classList.toggle('active', name === 'merge');
}

// =====================
// 並び替えタブ
// =====================
var sortPdfjsDoc = null;
var sortPageOrder = [];
var sortRotations = {};
var sortRawBuffer = null;
var sortOriginalFileName = '';
var sortDragSrc = null;

document.getElementById('sort-drop-zone').addEventListener('dragover', function(e){ e.preventDefault(); this.classList.add('dragover'); });
document.getElementById('sort-drop-zone').addEventListener('dragleave', function(){ this.classList.remove('dragover'); });
document.getElementById('sort-drop-zone').addEventListener('drop', function(e){
  e.preventDefault(); this.classList.remove('dragover');
  var f = e.dataTransfer.files[0]; if(f) loadSortPDF(f);
});
document.getElementById('sort-file-input').addEventListener('change', function(){
  if(this.files && this.files[0]) loadSortPDF(this.files[0]); this.value='';
});

function loadSortPDF(file) {
  document.getElementById('loading').style.display = 'block';
  document.getElementById('sort-pages-section').style.display = 'none';
  hideMsg('sort-success-msg'); hideMsg('sort-error-msg');
  var reader = new FileReader();
  reader.onload = function(e) {
    sortRawBuffer = e.target.result;
    sortOriginalFileName = file.name.replace(/\.pdf$/i, '');
    var copy = new Uint8Array(sortRawBuffer.slice(0));
    pdfjsLib.getDocument({ data: copy }).promise.then(function(doc) {
      sortPdfjsDoc = doc;
      var total = doc.numPages;
      sortPageOrder = []; sortRotations = {};
      for(var i = 0; i < total; i++) { sortPageOrder.push(i); sortRotations[i] = 0; }
      return renderSortAllPages();
    }).then(function() {
      document.getElementById('sort-pages-section').style.display = 'block';
      document.getElementById('loading').style.display = 'none';
      updateSortSelCount();
    }).catch(function(err) {
      showError('sort-error-msg', err);
      document.getElementById('loading').style.display = 'none';
    });
  };
  reader.onerror = function(e) { showError('sort-error-msg', e); document.getElementById('loading').style.display = 'none'; };
  reader.readAsArrayBuffer(file);
}

function renderSortAllPages() {
  var grid = document.getElementById('sort-pages-grid');
  grid.innerHTML = '';
  var promises = [];
  for(var i = 0; i < sortPageOrder.length; i++) {
    var card = createSortCard(i, sortPageOrder[i]);
    grid.appendChild(card);
    promises.push(renderSortCanvas(card, sortPageOrder[i]));
  }
  return Promise.all(promises);
}

function createSortCard(orderIdx, originalIdx) {
  var card = document.createElement('div');
  card.className = 'page-card';
  card.draggable = false;
  card.dataset.originalIdx = String(originalIdx);

  //ドラッグハンドル
  var handle = document.createElement('div');
  handle.className = 'drag-handle';
  handle.textContent = '☰';
  handle.title = 'ドラッグで並び替え';

  // チェックボックス
  var cbWrap = document.createElement('div');
  cbWrap.className = 'page-checkbox-wrap';
  var cb = document.createElement('input');
  cb.type = 'checkbox';
  cb.className = 'page-checkbox';
  cb.id = 'sort-cb-' + originalIdx;
  var cbLabel = document.createElement('label');
  cbLabel.className = 'page-checkbox-label';
  cbLabel.htmlFor = 'sort-cb-' + originalIdx;
  cbLabel.textContent = 'p.' + (orderIdx + 1) + '（元:' + (originalIdx + 1) + '）';
  cbWrap.appendChild(cb);
  cbWrap.appendChild(cbLabel);

  var wrap = document.createElement('div');
  wrap.className = 'page-canvas-wrap';

  var btnArea = document.createElement('div');
  btnArea.className = 'rotate-buttons';
  var btnL = document.createElement('button');
  btnL.type = 'button'; btnL.className = 'rotate-btn'; btnL.textContent = '↺'; btnL.title = '左に90°回転';
  var btnR = document.createElement('button');
  btnR.type = 'button'; btnR.className = 'rotate-btn'; btnR.textContent = '↻'; btnR.title = '右に90°回転';

  (function(c, idx, cbEl) {
    cbEl.addEventListener('change', function() { updateSortSelCount(); });
    btnL.addEventListener('click', function(e) {
      e.stopPropagation();
      sortRotations[idx] = ((sortRotations[idx] || 0) - 90+ 360) % 360;
      renderSortCanvas(c, idx);
    });
    btnR.addEventListener('click', function(e) {
      e.stopPropagation();
      sortRotations[idx] = ((sortRotations[idx] || 0) + 90) % 360;
      renderSortCanvas(c, idx);
    });handle.addEventListener('mousedown', function() { c.draggable = true; });
    handle.addEventListener('mouseleave', function() { if(!sortDragSrc) c.draggable = false; });
  })(card, originalIdx, cb);

  btnArea.appendChild(btnL); btnArea.appendChild(btnR);
  card.appendChild(handle);
  card.appendChild(cbWrap);
  card.appendChild(wrap);
  card.appendChild(btnArea);
  setupSortCardDrag(card);
  return card;
}

function updateSortSelCount() {
  var count = document.querySelectorAll('#sort-pages-grid .page-checkbox:checked').length;
  document.getElementById('sort-sel-count').textContent = count +'ページ選択中';
}
function sortSelectAll() {
  document.querySelectorAll('#sort-pages-grid .page-checkbox').forEach(function(cb) { cb.checked = true; });
  updateSortSelCount();
}
function sortDeselectAll() {
  document.querySelectorAll('#sort-pages-grid .page-checkbox').forEach(function(cb) { cb.checked = false; });
  updateSortSelCount();
}
function sortRotateSelected(deg) {
  var cards = document.querySelectorAll('#sort-pages-grid .page-card');
  var any = false;
  cards.forEach(function(card) {
    var cb = card.querySelector('.page-checkbox');
    if(cb && cb.checked) {
      any = true;
      var idx = parseInt(card.dataset.originalIdx, 10);
      sortRotations[idx] = ((sortRotations[idx] || 0) + deg + 360) % 360;
      renderSortCanvas(card, idx);
    }
  });
  if(!any) alert('ページを選択してから回転してください🌸');
}

function renderSortCanvas(card, originalIdx) {
  var wrap = card.querySelector('.page-canvas-wrap');
  var rotation = sortRotations[originalIdx] || 0;
  return sortPdfjsDoc.getPage(originalIdx + 1).then(function(page) {
    var viewport = page.getViewport({ scale: 0.4, rotation: rotation });
    var canvas = wrap.querySelector('canvas');
    if(!canvas) { canvas = document.createElement('canvas'); wrap.appendChild(canvas); }
    canvas.width = viewport.width; canvas.height = viewport.height;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return page.render({ canvasContext: ctx, viewport: viewport }).promise;
  });
}

function setupSortCardDrag(card) {
  card.addEventListener('dragstart', function() {
    sortDragSrc = card;
    setTimeout(function() { card.classList.add('dragging'); }, 0);
  });
  card.addEventListener('dragend', function() {
    card.classList.remove('dragging');
    card.draggable = false;
    sortDragSrc = null;rebuildSortPageOrder();
    updateSortLabels();
  });
  card.addEventListener('dragover', function(e) {
    e.preventDefault();
    if(sortDragSrc && sortDragSrc !== card) card.classList.add('drag-over');
  });
  card.addEventListener('dragleave', function() { card.classList.remove('drag-over'); });
  card.addEventListener('drop', function(e) {
    e.preventDefault(); card.classList.remove('drag-over');
    if(!sortDragSrc || sortDragSrc === card) return;
    var grid = document.getElementById('sort-pages-grid');
    var cards = Array.from(grid.querySelectorAll('.page-card'));
    var si = cards.indexOf(sortDragSrc), ti = cards.indexOf(card);
    if(si < ti) grid.insertBefore(sortDragSrc, card.nextSibling);
    else grid.insertBefore(sortDragSrc, card);});
}

function rebuildSortPageOrder() {
  sortPageOrder = Array.from(document.querySelectorAll('#sort-pages-grid .page-card'))
    .map(function(c) { return parseInt(c.dataset.originalIdx, 10); });
}
function updateSortLabels() {
  Array.from(document.querySelectorAll('#sort-pages-grid .page-card')).forEach(function(card, i) {
    var lbl = card.querySelector('.page-checkbox-label');
    if(lbl) lbl.textContent = 'p.' + (i + 1) + '（元:' + (parseInt(card.dataset.originalIdx, 10) + 1) + '）';
  });
}

function generateSortPDF() {
  var btn = document.getElementById('sort-download-btn');
  btn.textContent = '⏳ 生成中...'; btn.disabled = true;
  hideMsg('sort-success-msg'); hideMsg('sort-error-msg');
  rebuildSortPageOrder();
  var copy = new Uint8Array(sortRawBuffer.slice(0));
  PDFLib.PDFDocument.load(copy, { ignoreEncryption: true }).then(function(srcDoc) {
    return PDFLib.PDFDocument.create().then(function(newDoc) {
      var chain = Promise.resolve();
      sortPageOrder.forEach(function(idx) {
        chain = chain.then(function() {
          return newDoc.copyPages(srcDoc, [idx]).then(function(copied) {
            var p = copied[0];
            var rot = sortRotations[idx] || 0;
            if(rot !== 0) p.setRotation(PDFLib.degrees(rot));
            newDoc.addPage(p);
          });
        });
      });
      return chain.then(function() { return newDoc.save({ useObjectStreams: false }); });
    });
  }).then(function(bytes) {
    downloadBlob(bytes, sortOriginalFileName + '_sorted.pdf');
    showMsg('sort-success-msg');
  }).catch(function(err) {
    showError('sort-error-msg', err);}).finally(function() {
    btn.textContent = '📥 PDFを出力する'; btn.disabled = false;
  });
}

// =====================
// 結合タブ
// =====================
var mergeFiles = [];
var mergeFileIdSeq = 0;
var mergeFileDragSrc = null;
var mergePageDragSrc = null;

document.getElementById('merge-drop-zone').addEventListener('dragover', function(e){ e.preventDefault(); this.classList.add('dragover'); });
document.getElementById('merge-drop-zone').addEventListener('dragleave', function(){ this.classList.remove('dragover'); });
document.getElementById('merge-drop-zone').addEventListener('drop', function(e){
  e.preventDefault(); this.classList.remove('dragover');
  var files = Array.from(e.dataTransfer.files).filter(function(f){ return f.name.toLowerCase().endsWith('.pdf'); });
  if(files.length) loadMergeFiles(files);
});
document.getElementById('merge-file-input').addEventListener('change', function(){
  var files = Array.from(this.files).filter(function(f){ return f.name.toLowerCase().endsWith('.pdf'); });
  if(files.length) loadMergeFiles(files); this.value = '';
});

function loadMergeFiles(files) {
  document.getElementById('loading').style.display = 'block';
  hideMsg('merge-success-msg'); hideMsg('merge-error-msg');
  var chain = Promise.resolve();
  files.forEach(function(file) {
    chain = chain.then(function() {
      return new Promise(function(resolve, reject) {
        var reader = new FileReader();
        reader.onload = function(e) {
          var raw = e.target.result;
          var copy = new Uint8Array(raw.slice(0));
          pdfjsLib.getDocument({ data: copy }).promise.then(function(doc) {
            var count = doc.numPages, order = [], rots = {};
            for(var i = 0; i < count; i++) { order.push(i); rots[i] = 0; }
            var fd = { id: mergeFileIdSeq++, name: file.name, rawBuffer: raw, pdfjsDoc: doc,
                       pageCount: count, pageOrder: order, rotations: rots, canvasCache: {} };
            mergeFiles.push(fd);
            return appendMergeSection(fd);
          }).then(resolve).catch(reject);
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
      });
    });
  });
  chain.then(function() {
    document.getElementById('merge-pages-section').style.display = 'block';
  }).catch(function(err) {
    showError('merge-error-msg', err);
  }).finally(function() {
    document.getElementById('loading').style.display = 'none';
  });
}

function appendMergeSection(fd) {
  var list = document.getElementById('merge-files-list');
  var result = buildMergeSection(fd);
  list.appendChild(result.section);
  var promises = [];
  fd.pageOrder.forEach(function(originalIdx, i) {
    var card = createMergeCard(fd, i, originalIdx, result.grid, result.countSpan);
    result.grid.appendChild(card);
    promises.push(renderMergeCanvas(card, fd, originalIdx));
  });
  return Promise.all(promises);
}

function buildMergeSection(fd) {
  var section = document.createElement('div');
  section.className = 'merge-file-section';
  section.dataset.fileId = String(fd.id);

  var header = document.createElement('div');
  header.className = 'merge-file-header'; header.draggable = true;
  var icon = document.createElement('span'); icon.textContent = '☰'; icon.style.color = '#d96ea0';
  var nameSpan = document.createElement('span'); nameSpan.className = 'merge-file-name'; nameSpan.textContent = '📄 ' + fd.name;
  var pagesSpan = document.createElement('span'); pagesSpan.className = 'merge-file-pages'; pagesSpan.textContent = fd.pageCount + 'ページ';
  var removeBtn = document.createElement('button'); removeBtn.type = 'button'; removeBtn.className = 'remove-file-btn'; removeBtn.textContent = '✕';
  header.appendChild(icon); header.appendChild(nameSpan); header.appendChild(pagesSpan); header.appendChild(removeBtn);

  //選択バー
  var selBar = document.createElement('div'); selBar.className = 'sel-bar';
  var selLabel = document.createElement('span'); selLabel.className = 'sel-bar-label'; selLabel.textContent = '選択：';
  var btnAll = document.createElement('button'); btnAll.type = 'button'; btnAll.className = 'sel-bar-btn'; btnAll.textContent = '全選択';
  var btnNone = document.createElement('button'); btnNone.type = 'button'; btnNone.className = 'sel-bar-btn'; btnNone.textContent = '全解除';
  var sep = document.createElement('span'); sep.style.cssText = 'width:1px;height:20px;background:#f9b8d8;display:inline-block;margin:0 4px;';
  var rotL = document.createElement('button'); rotL.type = 'button'; rotL.className = 'sel-rotate-btn'; rotL.textContent = '↺ 選択を左回転';
  var rotR = document.createElement('button'); rotR.type = 'button'; rotR.className = 'sel-rotate-btn'; rotR.textContent = '↻ 選択を右回転';
  var countSpan = document.createElement('span'); countSpan.className = 'sel-count'; countSpan.textContent = '0ページ選択中';
  selBar.appendChild(selLabel); selBar.appendChild(btnAll); selBar.appendChild(btnNone);
  selBar.appendChild(sep); selBar.appendChild(rotL); selBar.appendChild(rotR); selBar.appendChild(countSpan);

  var hint = document.createElement('p'); hint.className = 'hint-text';
  hint.textContent = '💡 チェックボックスで複数選択 → 上のバーで回転。☰ をドラッグで並び替え。';

  var grid = document.createElement('div'); grid.className = 'pages-grid'; grid.style.marginTop = '4px';

  (function(fileData, g, cs) {
    btnAll.onclick = function() {
      g.querySelectorAll('.page-checkbox').forEach(function(cb) { cb.checked = true; });
      updateMergeSelCount(g, cs);
    };
    btnNone.onclick = function() {
      g.querySelectorAll('.page-checkbox').forEach(function(cb) { cb.checked = false; });
      updateMergeSelCount(g, cs);
    };
    rotL.onclick = function() { mergeRotateSelected(fileData, g, cs, -90); };
    rotR.onclick = function() { mergeRotateSelected(fileData, g, cs, 90); };
    removeBtn.onclick = function() {
      mergeFiles = mergeFiles.filter(function(f) { return f.id !== fileData.id; });
      section.remove();
      if(mergeFiles.length === 0) document.getElementById('merge-pages-section').style.display = 'none';
    };
  })(fd, grid, countSpan);

  section.appendChild(header); section.appendChild(selBar); section.appendChild(hint); section.appendChild(grid);
  setupMergeFileDrag(header, section);
  return { section: section, grid: grid, countSpan: countSpan };
}

function updateMergeSelCount(grid, countSpan) {
  var count = grid.querySelectorAll('.page-checkbox:checked').length;
  countSpan.textContent = count + 'ページ選択中';
}

function mergeRotateSelected(fd, grid, countSpan, deg) {
  var cards = Array.from(grid.querySelectorAll('.page-card'));
  var any = false;
  cards.forEach(function(card) {
    var cb = card.querySelector('.page-checkbox');
    if(cb && cb.checked) {
      any = true;
      var idx = parseInt(card.dataset.originalIdx, 10);
      var prev = fd.rotations[idx] || 0;
      fd.rotations[idx] = (prev + deg + 360) % 360;
      delete fd.canvasCache[idx + '_' + prev];
      renderMergeCanvas(card, fd, idx);
    }
  });
  if(!any) alert('ページを選択してから回転してください🌸');
}

function createMergeCard(fd, orderIdx, originalIdx, grid, countSpan) {
  var card = document.createElement('div');
  card.className = 'page-card'; card.draggable = false;
  card.dataset.fileId = String(fd.id); card.dataset.originalIdx = String(originalIdx);

  var handle = document.createElement('div'); handle.className = 'drag-handle'; handle.textContent = '☰'; handle.title = 'ドラッグで並び替え';

  var cbWrap = document.createElement('div'); cbWrap.className = 'page-checkbox-wrap';
  var cb = document.createElement('input'); cb.type = 'checkbox'; cb.className = 'page-checkbox';
  cb.id = 'merge-cb-' + fd.id + '-' + originalIdx;
  var cbLabel = document.createElement('label'); cbLabel.className = 'page-checkbox-label';
  cbLabel.htmlFor = 'merge-cb-' + fd.id + '-' + originalIdx;
  cbLabel.textContent = 'p.' + (orderIdx + 1);
  cbWrap.appendChild(cb); cbWrap.appendChild(cbLabel);

  var wrap = document.createElement('div'); wrap.className = 'page-canvas-wrap';

  var btnArea = document.createElement('div'); btnArea.className = 'rotate-buttons';
  var btnL = document.createElement('button'); btnL.type = 'button'; btnL.className = 'rotate-btn'; btnL.textContent = '↺';
  var btnR = document.createElement('button'); btnR.type = 'button'; btnR.className = 'rotate-btn'; btnR.textContent = '↻';

  (function(fileData, c, idx, g, cs) {
    cb.addEventListener('change', function() { updateMergeSelCount(g, cs); });
    btnL.addEventListener('click', function(e) {
      e.stopPropagation();
      var prev = fileData.rotations[idx] || 0;
      fileData.rotations[idx] = (prev - 90 + 360) % 360;
      delete fileData.canvasCache[idx + '_' + prev];
      renderMergeCanvas(c, fileData, idx);
    });
    btnR.addEventListener('click', function(e) {
      e.stopPropagation();
      var prev = fileData.rotations[idx] || 0;
      fileData.rotations[idx] = (prev + 90) % 360;
      delete fileData.canvasCache[idx + '_' + prev];
      renderMergeCanvas(c, fileData, idx);
    });
    handle.addEventListener('mousedown', function() { c.draggable = true; });
    handle.addEventListener('mouseleave', function() { if(!mergePageDragSrc) c.draggable = false; });
  })(fd, card, originalIdx, grid, countSpan);

  btnArea.appendChild(btnL); btnArea.appendChild(btnR);
  card.appendChild(handle); card.appendChild(cbWrap); card.appendChild(wrap); card.appendChild(btnArea);
  setupMergeCardDrag(card, fd);
  return card;
}

function renderMergeCanvas(card, fd, originalIdx) {
  var wrap = card.querySelector('.page-canvas-wrap');
  var rotation = fd.rotations[originalIdx] || 0;
  var cacheKey = originalIdx + '_' + rotation;
  var canvas = wrap.querySelector('canvas');
  if(!canvas) { canvas = document.createElement('canvas'); wrap.appendChild(canvas); }
  if(fd.canvasCache[cacheKey]) {
    var cached = fd.canvasCache[cacheKey];
    canvas.width = cached.width; canvas.height = cached.height;
    canvas.getContext('2d').drawImage(cached, 0, 0);
    return Promise.resolve();
  }
  return fd.pdfjsDoc.getPage(originalIdx + 1).then(function(page) {
    var viewport = page.getViewport({ scale: 0.4, rotation: rotation });
    canvas.width = viewport.width; canvas.height = viewport.height;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return page.render({ canvasContext: ctx, viewport: viewport }).promise.then(function() {
      var cc = document.createElement('canvas'); cc.width = canvas.width; cc.height = canvas.height;
      cc.getContext('2d').drawImage(canvas, 0, 0); fd.canvasCache[cacheKey] = cc;
    });
  });
}

function setupMergeCardDrag(card, fd) {
  card.addEventListener('dragstart', function() {
    mergePageDragSrc = card;
    setTimeout(function() { card.classList.add('dragging'); }, 0);
  });
  card.addEventListener('dragend', function() {
    card.classList.remove('dragging'); card.draggable = false;
    mergePageDragSrc = null;
    rebuildMergePageOrder(fd);
    updateMergePageLabels(card.closest('.pages-grid'));
  });
  card.addEventListener('dragover', function(e) {
    e.preventDefault();
    if(mergePageDragSrc && mergePageDragSrc !== card && mergePageDragSrc.dataset.fileId === card.dataset.fileId)
      card.classList.add('drag-over');
  });
  card.addEventListener('dragleave', function() { card.classList.remove('drag-over'); });
  card.addEventListener('drop', function(e) {
    e.preventDefault(); card.classList.remove('drag-over');
    if(!mergePageDragSrc || mergePageDragSrc === card) return;
    if(mergePageDragSrc.dataset.fileId !== card.dataset.fileId) return;
    var g = card.closest('.pages-grid');
    var cards = Array.from(g.querySelectorAll('.page-card'));
    var si = cards.indexOf(mergePageDragSrc), ti = cards.indexOf(card);
    if(si < ti) g.insertBefore(mergePageDragSrc, card.nextSibling);
    else g.insertBefore(mergePageDragSrc, card);
  });
}

function rebuildMergePageOrder(fd) {
  var section = document.querySelector('.merge-file-section[data-file-id="' + fd.id + '"]');
  if(!section) return;
  fd.pageOrder = Array.from(section.querySelectorAll('.page-card')).map(function(c) { return parseInt(c.dataset.originalIdx, 10); });
}
function updateMergePageLabels(grid) {
  if(!grid) return;
  Array.from(grid.querySelectorAll('.page-card')).forEach(function(c, i) {
    var lbl = c.querySelector('.page-checkbox-label'); if(lbl) lbl.textContent = 'p.' + (i + 1);
  });
}

function setupMergeFileDrag(header, section) {
  header.addEventListener('dragstart', function(e) {
    mergeFileDragSrc = section;
    setTimeout(function() { header.classList.add('dragging'); }, 0);
    e.stopPropagation();
  });
  header.addEventListener('dragend', function() {
    header.classList.remove('dragging'); mergeFileDragSrc = null; rebuildMergeFilesOrder();});
  header.addEventListener('dragover', function(e) {
    e.preventDefault(); e.stopPropagation();if(mergeFileDragSrc && mergeFileDragSrc !== section) header.classList.add('drag-over');
  });
  header.addEventListener('dragleave', function() { header.classList.remove('drag-over'); });
  header.addEventListener('drop', function(e) {
    e.preventDefault(); e.stopPropagation(); header.classList.remove('drag-over');
    if(!mergeFileDragSrc || mergeFileDragSrc === section) return;
    var list = document.getElementById('merge-files-list');
    var sections = Array.from(list.querySelectorAll('.merge-file-section'));
    var si = sections.indexOf(mergeFileDragSrc), ti = sections.indexOf(section);
    if(si < ti) list.insertBefore(mergeFileDragSrc, section.nextSibling);
    else list.insertBefore(mergeFileDragSrc, section);
  });
}

function rebuildMergeFilesOrder() {
  var newOrder = [];
  Array.from(document.querySelectorAll('#merge-files-list .merge-file-section')).forEach(function(s) {
    var id = parseInt(s.dataset.fileId, 10);
    var fd = mergeFiles.find(function(f) { return f.id === id; });
    if(fd) newOrder.push(fd);
  });
  mergeFiles = newOrder;
}

function generateMergePDF() {
  if(mergeFiles.length === 0) return;
  rebuildMergeFilesOrder();
  var btn = document.getElementById('merge-download-btn');
  btn.textContent = '⏳ 結合中...'; btn.disabled = true;
  hideMsg('merge-success-msg'); hideMsg('merge-error-msg');
  PDFLib.PDFDocument.create().then(function(newDoc) {
    var chain = Promise.resolve();
    mergeFiles.forEach(function(fd) {
      chain = chain.then(function() {
        rebuildMergePageOrder(fd);
        var copy = new Uint8Array(fd.rawBuffer.slice(0));
        return PDFLib.PDFDocument.load(copy, { ignoreEncryption: true }).then(function(srcDoc) {
          var inner = Promise.resolve();
          fd.pageOrder.forEach(function(idx) {
            inner = inner.then(function() {
              return newDoc.copyPages(srcDoc, [idx]).then(function(copied) {
                var p = copied[0]; var rot = fd.rotations[idx] || 0;
                if(rot !== 0) p.setRotation(PDFLib.degrees(rot));
                newDoc.addPage(p);
              });
            });
          });
          return inner;
        });
      });
    });
    return chain.then(function() { return newDoc.save({ useObjectStreams: false }); });
  }).then(function(bytes) {
    downloadBlob(bytes, mergeFiles[0].name.replace(/\.pdf$/i, '') + '_merged.pdf');
    showMsg('merge-success-msg');
  }).catch(function(err) {
    showError('merge-error-msg', err);
  }).finally(function() {
    btn.textContent = '📎 結合してダウンロード'; btn.disabled = false;
  });
}

// =====================
// 共通
// =====================
function downloadBlob(bytes, filename) {
  var blob = new Blob([bytes], { type: 'application/pdf' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a'); a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function() { URL.revokeObjectURL(url); }, 1000);
}
function showMsg(id) { var el = document.getElementById(id); if(!el) return; el.style.display = 'block'; setTimeout(function() { el.style.display = 'none'; }, 4000); }
function hideMsg(id) { var el = document.getElementById(id); if(el) el.style.display = 'none'; }
function showError(id, err) { var el = document.getElementById(id); if(!el) return; el.textContent = '❌ エラー: ' + (err && err.message ? err.message : String(err)); el.style.display = 'block'; }
</script>
</body>
</html>
