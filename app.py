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
  body {
    background: #fff8fb;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #7a2e5e;
    min-height: 100vh;}
  h1 {
    text-align: center;
    color: #d96ea0;
    padding: 28px 0 6px;
    font-size: 1.8rem;
  }
  .subtitle {
    text-align: center;
    color: #b07aad;
    font-size: 0.9rem;
    margin-bottom: 24px;
  }
  .container {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 16px;
  }
  .tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 28px;
    justify-content: center;
  }
  .tab-btn {
    background: #fde8f3;
    border: 2px solid #f9b8d8;
    border-radius: 24px;
    padding: 10px 32px;
    font-size: 1rem;
    font-weight: bold;
    color: #b07aad;
    cursor: pointer;
    transition: all 0.2s;
  }
  .tab-btn.active {
    background: #f9b8d8;
    color: #7a2e5e;
    border-color: #f490c0;
  }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .drop-zone {
    border: 3px dashed #f9b8d8;
    border-radius: 20px;
    background: #fde8f3;
    padding: 40px 24px;
    text-align: center;
    max-width: 600px;
    margin: 0 auto 32px;
    transition: all 0.2s;
  }
  .drop-zone.dragover {
    background: #fcd0e8;
    border-color: #f490c0;
  }
  .drop-zone-title {
    color: #c762a0;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 8px;
  }
  .drop-zone-sub {
    color: #b07aad;
    font-size: 0.85rem;
    display: block;
    margin-bottom: 16px;
  }
  .select-btn {
    display: inline-block;
    background: #f9b8d8;
    color: #7a2e5e;
    border: none;
    border-radius: 20px;
    padding: 8px 28px;
    font-size: 0.95rem;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
  }
  .select-btn:hover { background: #f490c0; color: white; }

  .section-title {
    color: #c762a0;
    font-size: 1.1rem;
    font-weight: bold;
    border-left: 5px solid #f9b8d8;
    padding-left: 10px;
    margin-bottom: 12px;
  }

  /* 一括操作バー */
  .bulk-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    background: #fde8f3;
    border: 2px solid #f9b8d8;
    border-radius: 16px;
    padding: 10px 16px;
    margin-bottom: 18px;
  }
  .bulk-bar-label {
    color: #c762a0;
    font-size: 0.9rem;
    font-weight: bold;margin-right: 4px;
  }
  .bulk-btn {
    background: white;
    border: 2px solid #f9b8d8;
    border-radius: 20px;
    padding: 6px 18px;
    font-size: 0.9rem;
    font-weight: bold;
    color: #b07aad;
    cursor: pointer;
    transition: all 0.2s;
  }
  .bulk-btn:hover { background: #f9b8d8; color: #7a2e5e; }
  .bulk-btn.danger:hover { background: #f490c0; color: white; }
  .bulk-rotate-btn {
    background: white;
    border: 2px solid #f9b8d8;
    border-radius: 20px;
    padding: 6px 20px;
    font-size: 1rem;
    font-weight: bold;
    color: #c762a0;
    cursor: pointer;
    transition: all 0.2s;
  }
  .bulk-rotate-btn:hover { background: #f9b8d8; color: #7a2e5e; }
  .selected-count {
    color: #d96ea0;
    font-size: 0.85rem;
    margin-left: auto;
  }

  .pages-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 32px;
  }
  .page-card {
    background: white;
    border: 2px solid #f9b8d8;
    border-radius: 16px;
    width: 160px;
    padding: 10px;
    text-align: center;
    cursor: grab;
    user-select: none;
    transition: box-shadow 0.2s, transform 0.2s, border-color 0.15s;
    position: relative;
  }
  .page-card:hover {
    box-shadow: 0 4px 16px #f9b8d840;
    transform: translateY(-2px);
  }
  .page-card.selected {
    border-color: #f490c0;
    background: #fff0f8;
    box-shadow: 0 0 0 3px #f9b8d8;
  }
  .page-card.dragging { opacity: 0.4; }
  .page-card.drag-over { border-color: #f490c0; background: #fde8f3; }

  /* 選択チェックマーク */
  .page-check {
    position: absolute;
    top: 6px;
    right: 8px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid #f9b8d8;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    color: white;
    transition: all 0.15s;
  }
  .page-card.selected .page-check {
    background: #f490c0;
    border-color: #f490c0;
  }

  .page-canvas-wrap {
    width: 100%;
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
    margin-top: 4px;
  }
  .page-canvas-wrap canvas {
    width: 100%;
    border-radius: 8px;
    display: block;
  }
  .page-label {
    color: #b07aad;
    font-size: 0.8rem;
    margin-bottom: 8px;
  }
  .rotate-buttons {
    display: flex;
    justify-content: center;
    gap: 8px;
  }
  .rotate-btn {
    background: #fde8f3;
    border: 1px solid #f9b8d8;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    font-size: 1rem;
    cursor: pointer;
    color: #c762a0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
  }
  .rotate-btn:hover { background: #f9b8d8; color: #7a2e5e; }

  .merge-file-section {
    background: white;
    border: 2px solid #f9b8d8;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 20px;
  }
  .merge-file-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;cursor: grab;
    padding: 6px 8px;
    border-radius: 10px;
    background: #fde8f3;}
  .merge-file-header:hover { background: #fcd0e8; }
  .merge-file-header.dragging { opacity: 0.4; }
  .merge-file-header.drag-over { outline: 2px dashed #f490c0; }
  .merge-file-name {
    font-weight: bold;
    color: #c762a0;
    font-size: 0.95rem;
    flex: 1;
  }
  .merge-file-pages {
    color: #b07aad;
    font-size: 0.8rem;
  }
  .remove-file-btn {
    background: #fde8f3;
    border: 1px solid #f9b8d8;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    font-size: 0.9rem;
    cursor: pointer;
    color: #c762a0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;flex-shrink: 0;
  }
  .remove-file-btn:hover { background: #f9b8d8; color: #7a2e5e; }

  /* 結合タブ用一括バー */
  .merge-bulk-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    background: #fef6fb;
    border: 1px solid #f9b8d8;
    border-radius: 12px;
    padding: 7px 12px;
    margin-bottom: 10px;
  }
  .merge-bulk-bar .bulk-bar-label {
    font-size: 0.82rem;
  }
  .merge-bulk-bar .bulk-btn,
  .merge-bulk-bar .bulk-rotate-btn {
    font-size: 0.82rem;
    padding: 4px 14px;
  }
  .merge-bulk-bar .selected-count {
    font-size: 0.8rem;
  }

  .btn-area {
    text-align: center;
    margin-bottom: 24px;
  }
  .download-btn {
    background: #f9b8d8;
    color: #7a2e5e;
    border: none;
    border-radius: 24px;
    padding: 14px 48px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
  }
  .download-btn:hover:not(:disabled) { background: #f490c0; color: white; }
  .download-btn:disabled { opacity: 0.6; cursor: not-allowed; }

  #loading {
    display: none;text-align: center;
    color: #c762a0;
    font-size: 1rem;
    margin: 24px 0;
  }
  .spinner {
    display: inline-block;
    width: 32px;
    height: 32px;
    border: 4px solid #f9b8d8;
    border-top-color: #d96ea0;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    vertical-align: middle;
    margin-right: 8px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .success-msg {
    display: none;
    text-align: center;
    color: #2e7a52;
    background: #e8f8ee;
    border: 1px solid #a0e0bc;
    border-radius: 12px;
    padding: 12px 24px;
    margin: 16px auto;
    max-width: 500px;
    font-weight: bold;
  }
  .error-msg {
    display: none;
    text-align: center;
    color: #7a2e2e;
    background: #f8e8e8;
    border: 1px solid #e0a0a0;
    border-radius: 12px;
    padding: 12px 24px;
    margin: 16px auto;
    max-width: 500px;
    font-weight: bold;
    word-break: break-all;
  }
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
      <span class="drop-zone-sub">またはボタンからファイルを選択</span><button class="select-btn" type="button" onclick="document.getElementById('sort-file-input').click()">📂ファイルを選択</button>
      <input type="file" id="sort-file-input" accept=".pdf" style="display:none;">
    </div>
    <div id="sort-pages-section" style="display:none;">
      <p class="section-title">📋 ページ一覧</p>

      <!-- 並び替えタブ一括バー -->
      <div class="bulk-bar">
        <span class="bulk-bar-label">選択操作：</span>
        <button class="bulk-btn" type="button" onclick="sortSelectAll()">全選択</button>
        <button class="bulk-btn" type="button" onclick="sortDeselectAll()">選択解除</button>
        <span style="color:#e0a0c0;margin:0 4px;">|</span>
        <span class="bulk-bar-label">選択ページを回転：</span>
        <button class="bulk-rotate-btn" type="button" onclick="sortBulkRotate(-90)">↺ 左90°</button>
        <button class="bulk-rotate-btn" type="button" onclick="sortBulkRotate(90)">↻ 右90°</button>
        <button class="bulk-rotate-btn" type="button" onclick="sortBulkRotate(180)">↕ 180°</button>
        <span class="selected-count" id="sort-selected-count">0ページ選択中</span>
      </div><p style="color:#b07aad;font-size:0.82rem;margin-bottom:14px;">💡 カードをクリックで選択／ドラッグで並び替え</p><div class="pages-grid" id="sort-pages-grid"></div>
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

// ==========================
// タブ切り替え
// ==========================
function switchTab(name) {
  var btns = document.querySelectorAll('.tab-btn');
  btns[0].classList.toggle('active', name === 'sort');
  btns[1].classList.toggle('active', name === 'merge');
  document.getElementById('tab-sort').classList.toggle('active', name === 'sort');
  document.getElementById('tab-merge').classList.toggle('active', name === 'merge');
}

// ==========================
// 並び替えタブ
// ==========================
var sortPdfjsDoc = null;
var sortPageOrder = [];
var sortRotations = {};
var sortRawBuffer = null;
var sortOriginalFileName = '';
var sortDragSrc = null;

document.getElementById('sort-drop-zone').addEventListener('dragover', function(e) {
  e.preventDefault(); this.classList.add('dragover');
});
document.getElementById('sort-drop-zone').addEventListener('dragleave', function() {
  this.classList.remove('dragover');
});
document.getElementById('sort-drop-zone').addEventListener('drop', function(e) {
  e.preventDefault(); this.classList.remove('dragover');
  var file = e.dataTransfer.files[0];
  if (file) loadSortPDF(file);
});
document.getElementById('sort-file-input').addEventListener('change', function() {
  if (this.files && this.files[0]) loadSortPDF(this.files[0]);
  this.value = '';
});

function loadSortPDF(file) {
  document.getElementById('loading').style.display = 'block';
  document.getElementById('sort-pages-section').style.display = 'none';
  hideMsg('sort-success-msg');
  hideMsg('sort-error-msg');

  var reader = new FileReader();
  reader.onload = function(e) {
    sortRawBuffer = e.target.result;
    sortOriginalFileName = file.name.replace(/\.pdf$/i, '');
    var copyForPdfjs = new Uint8Array(sortRawBuffer.slice(0));

    pdfjsLib.getDocument({ data: copyForPdfjs }).promise
      .then(function(doc) {
        sortPdfjsDoc = doc;
        var total = doc.numPages;
        sortPageOrder = [];
        sortRotations = {};
        for (var i = 0; i < total; i++) {
          sortPageOrder.push(i);sortRotations[i] = 0;
        }
        return renderSortAllPages();
      })
      .then(function() {
        document.getElementById('sort-pages-section').style.display = 'block';
        document.getElementById('loading').style.display = 'none';
        updateSortSelectedCount();
      })
      .catch(function(err) {
        showError('sort-error-msg', err);document.getElementById('loading').style.display = 'none';
      });
  };
  reader.onerror = function(e) {
    showError('sort-error-msg', e);
    document.getElementById('loading').style.display = 'none';
  };
  reader.readAsArrayBuffer(file);
}

function renderSortAllPages() {
  var grid = document.getElementById('sort-pages-grid');
  grid.innerHTML = '';
  var promises = [];
  for (var i = 0; i < sortPageOrder.length; i++) {
    var card = createSortCard(i, sortPageOrder[i]);
    grid.appendChild(card);
    promises.push(renderSortCanvas(card, sortPageOrder[i]));
  }
  return Promise.all(promises);
}

function createSortCard(orderIdx, originalIdx) {
  var card = document.createElement('div');
  card.className = 'page-card';
  card.draggable = true;
  card.dataset.originalIdx = String(originalIdx);

  // 選択チェックマーク
  var check = document.createElement('div');
  check.className = 'page-check';
  check.textContent = '✓';

  var wrap = document.createElement('div');
  wrap.className = 'page-canvas-wrap';

  var label = document.createElement('div');
  label.className = 'page-label';
  label.textContent = 'p.' + (orderIdx + 1) + '（元: ' + (originalIdx + 1) + '）';

  var btnArea = document.createElement('div');
  btnArea.className = 'rotate-buttons';

  var btnL = document.createElement('button');
  btnL.type = 'button'; btnL.className = 'rotate-btn';
  btnL.textContent = '↺'; btnL.title = '左に90°回転';

  var btnR = document.createElement('button');
  btnR.type = 'button'; btnR.className = 'rotate-btn';
  btnR.textContent = '↻'; btnR.title = '右に90°回転';

  (function(c, idx) {
    // カードクリックで選択トグル（ボタン以外の部分）
    c.addEventListener('click', function(e) {
      if (e.target.closest('.rotate-btn')) return;
      c.classList.toggle('selected');
      updateSortSelectedCount();
    });
    btnL.addEventListener('click', function(e) {
      e.stopPropagation();
      sortRotations[idx] = ((sortRotations[idx] || 0) - 90+ 360) % 360;
      renderSortCanvas(c, idx);
    });
    btnR.addEventListener('click', function(e) {
      e.stopPropagation();
      sortRotations[idx] = ((sortRotations[idx] || 0) + 90) % 360;
      renderSortCanvas(c, idx);
    });
  })(card, originalIdx);

  btnArea.appendChild(btnL);
  btnArea.appendChild(btnR);
  card.appendChild(check);
  card.appendChild(wrap);
  card.appendChild(label);
  card.appendChild(btnArea);
  setupSortCardDrag(card);
  return card;
}

function renderSortCanvas(card, originalIdx) {
  var wrap = card.querySelector('.page-canvas-wrap');
  var rotation = sortRotations[originalIdx] || 0;
  return sortPdfjsDoc.getPage(originalIdx + 1).then(function(page) {
    var viewport = page.getViewport({ scale: 0.4, rotation: rotation });
    var canvas = wrap.querySelector('canvas');
    if (!canvas) { canvas = document.createElement('canvas'); wrap.appendChild(canvas); }
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return page.render({ canvasContext: ctx, viewport: viewport }).promise;
  });
}

//全選択・全解除
function sortSelectAll() {
  Array.from(document.querySelectorAll('#sort-pages-grid .page-card'))
    .forEach(function(c) { c.classList.add('selected'); });
  updateSortSelectedCount();
}
function sortDeselectAll() {
  Array.from(document.querySelectorAll('#sort-pages-grid .page-card'))
    .forEach(function(c) { c.classList.remove('selected'); });
  updateSortSelectedCount();
}

// 選択数表示更新
function updateSortSelectedCount() {
  var count = document.querySelectorAll('#sort-pages-grid .page-card.selected').length;
  document.getElementById('sort-selected-count').textContent = count +'ページ選択中';
}

// 一括回転（並び替えタブ）
function sortBulkRotate(deg) {
  var selected = Array.from(document.querySelectorAll('#sort-pages-grid .page-card.selected'));
  if (selected.length === 0) return;
  var promises = [];
  selected.forEach(function(card) {
    var idx = parseInt(card.dataset.originalIdx, 10);
    sortRotations[idx] = ((sortRotations[idx] || 0) + deg + 360) % 360;
    promises.push(renderSortCanvas(card, idx));
  });
  return Promise.all(promises);
}

function setupSortCardDrag(card) {
  card.addEventListener('dragstart', function() {
    sortDragSrc = card;
    setTimeout(function() { card.classList.add('dragging'); }, 0);
  });
  card.addEventListener('dragend', function() {
    card.classList.remove('dragging');
    sortDragSrc = null;
    rebuildSortPageOrder();
    updateSortLabels();
  });
  card.addEventListener('dragover', function(e) {
    e.preventDefault();
    if (sortDragSrc && sortDragSrc !== card) card.classList.add('drag-over');
  });
  card.addEventListener('dragleave', function() { card.classList.remove('drag-over'); });
  card.addEventListener('drop', function(e) {
    e.preventDefault();
    card.classList.remove('drag-over');
    if (!sortDragSrc || sortDragSrc === card) return;
    var grid = document.getElementById('sort-pages-grid');
    var cards = Array.from(grid.querySelectorAll('.page-card'));
    var si = cards.indexOf(sortDragSrc);
    var ti = cards.indexOf(card);
    if (si < ti) grid.insertBefore(sortDragSrc, card.nextSibling);
    elsegrid.insertBefore(sortDragSrc, card);
  });
}

function rebuildSortPageOrder() {
  sortPageOrder = Array.from(
    document.querySelectorAll('#sort-pages-grid .page-card')
  ).map(function(c) { return parseInt(c.dataset.originalIdx, 10); });
}

function updateSortLabels() {
  Array.from(document.querySelectorAll('#sort-pages-grid .page-card'))
    .forEach(function(card, i) {
      card.querySelector('.page-label').textContent =
        'p.' + (i + 1) + '（元: ' + (parseInt(card.dataset.originalIdx, 10) + 1) + '）';
    });
}

function generateSortPDF() {
  var btn = document.getElementById('sort-download-btn');
  btn.textContent = '⏳ 生成中...';
  btn.disabled = true;
  hideMsg('sort-success-msg');
  hideMsg('sort-error-msg');
  rebuildSortPageOrder();

  var copyForPdfLib = new Uint8Array(sortRawBuffer.slice(0));
  PDFLib.PDFDocument.load(copyForPdfLib, { ignoreEncryption: true })
    .then(function(srcDoc) {
      return PDFLib.PDFDocument.create().then(function(newDoc) {
        var chain = Promise.resolve();
        sortPageOrder.forEach(function(idx) {
          chain = chain.then(function() {
            return newDoc.copyPages(srcDoc, [idx]).then(function(copied) {
              var p = copied[0];
              var rot = sortRotations[idx] || 0;
              if (rot !== 0) p.setRotation(PDFLib.degrees(rot));
              newDoc.addPage(p);
            });
          });
        });
        return chain.then(function() { return newDoc.save({ useObjectStreams: false }); });
      });
    })
    .then(function(bytes) {
      downloadBlob(bytes, sortOriginalFileName + '_sorted.pdf');
      showMsg('sort-success-msg');})
    .catch(function(err) { showError('sort-error-msg', err); })
    .finally(function() {
      btn.textContent = '📥 PDFを出力する';
      btn.disabled = false;
    });
}

// ==========================
// 結合タブ
// ==========================
var mergeFiles = [];
var mergeFileIdSeq = 0;
var mergeFileDragSrc = null;
var mergePageDragSrc = null;

document.getElementById('merge-drop-zone').addEventListener('dragover', function(e) {
  e.preventDefault(); this.classList.add('dragover');
});
document.getElementById('merge-drop-zone').addEventListener('dragleave', function() {
  this.classList.remove('dragover');
});
document.getElementById('merge-drop-zone').addEventListener('drop', function(e) {
  e.preventDefault(); this.classList.remove('dragover');
  var files = Array.from(e.dataTransfer.files).filter(function(f) {
    return f.name.toLowerCase().endsWith('.pdf');
  });
  if (files.length) loadMergeFiles(files);
});
document.getElementById('merge-file-input').addEventListener('change', function() {
  var files = Array.from(this.files).filter(function(f) {
    return f.name.toLowerCase().endsWith('.pdf');
  });
  if (files.length) loadMergeFiles(files);
  this.value = '';
});

function loadMergeFiles(files) {
  document.getElementById('loading').style.display = 'block';
  hideMsg('merge-success-msg');
  hideMsg('merge-error-msg');

  var chain = Promise.resolve();
  files.forEach(function(file) {
    chain = chain.then(function() {
      return new Promise(function(resolve, reject) {
        var reader = new FileReader();
        reader.onload = function(e) {
          var rawBuffer = e.target.result;
          var copyForPdfjs = new Uint8Array(rawBuffer.slice(0));
          pdfjsLib.getDocument({ data: copyForPdfjs }).promise
            .then(function(doc) {
              var count = doc.numPages;
              var order = []; var rots = {};
              for (var i = 0; i < count; i++) { order.push(i); rots[i] = 0; }
              var fd = {
                id: mergeFileIdSeq++,
                name: file.name,
                rawBuffer: rawBuffer,
                pdfjsDoc: doc,
                pageCount: count,
                pageOrder: order,
                rotations: rots,
                canvasCache: {}
              };
              mergeFiles.push(fd);
              return appendMergeSection(fd);
            })
            .then(resolve).catch(reject);
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
      });
    });
  });

  chain
    .then(function() { document.getElementById('merge-pages-section').style.display = 'block'; })
    .catch(function(err) { showError('merge-error-msg', err); })
    .finally(function() { document.getElementById('loading').style.display = 'none'; });
}

function appendMergeSection(fd) {
  var list = document.getElementById('merge-files-list');
  var section = buildMergeSection(fd);
  list.appendChild(section);
  var grid = section.querySelector('.pages-grid');
  var promises = [];
  fd.pageOrder.forEach(function(originalIdx, i) {
    var card = createMergeCard(fd, i, originalIdx);
    grid.appendChild(card);
    promises.push(renderMergeCanvas(card, fd, originalIdx));
  });
  return Promise.all(promises);
}

function buildMergeSection(fd) {
  var section = document.createElement('div');
  section.className = 'merge-file-section';
  section.dataset.fileId = String(fd.id);

  //ヘッダー
  var header = document.createElement('div');
  header.className = 'merge-file-header';
  header.draggable = true;
  header.dataset.fileId = String(fd.id);

  var icon = document.createElement('span');
  icon.textContent = '☰'; icon.style.color = '#d96ea0';

  var nameSpan = document.createElement('span');
  nameSpan.className = 'merge-file-name';
  nameSpan.textContent = '📄 ' + fd.name;

  var pagesSpan = document.createElement('span');
  pagesSpan.className = 'merge-file-pages';
  pagesSpan.textContent = fd.pageCount + 'ページ';

  var removeBtn = document.createElement('button');
  removeBtn.type = 'button'; removeBtn.className = 'remove-file-btn';
  removeBtn.textContent = '✕';
  (function(fileData, sec) {
    removeBtn.addEventListener('click', function() {
      mergeFiles = mergeFiles.filter(function(f) { return f.id !== fileData.id; });
      sec.remove();
      if (mergeFiles.length === 0)
        document.getElementById('merge-pages-section').style.display = 'none';
    });
  })(fd, section);

  header.appendChild(icon);
  header.appendChild(nameSpan);
  header.appendChild(pagesSpan);
  header.appendChild(removeBtn);

  // 一括操作バー（結合タブ用）
  var bulkBar = document.createElement('div');
  bulkBar.className = 'merge-bulk-bar';

  var bulkLabel = document.createElement('span');
  bulkLabel.className = 'bulk-bar-label';
  bulkLabel.textContent = '選択：';

  var btnAll = document.createElement('button');
  btnAll.type = 'button'; btnAll.className = 'bulk-btn';
  btnAll.textContent = '全選択';

  var btnNone = document.createElement('button');
  btnNone.type = 'button'; btnNone.className = 'bulk-btn';
  btnNone.textContent = '解除';

  var sep = document.createElement('span');
  sep.style.cssText = 'color:#e0a0c0;margin:0 2px;';
  sep.textContent = '|';

  var rotLabel = document.createElement('span');
  rotLabel.className = 'bulk-bar-label';
  rotLabel.textContent = '回転：';

  var btnBL = document.createElement('button');
  btnBL.type = 'button'; btnBL.className = 'bulk-rotate-btn';
  btnBL.textContent = '↺ 左90°';

  var btnBR = document.createElement('button');
  btnBR.type = 'button'; btnBR.className = 'bulk-rotate-btn';
  btnBR.textContent = '↻ 右90°';

  var btnB180 = document.createElement('button');
  btnB180.type = 'button'; btnB180.className = 'bulk-rotate-btn';
  btnB180.textContent = '↕ 180°';

  var countSpan = document.createElement('span');
  countSpan.className = 'selected-count';
  countSpan.textContent = '0ページ選択中';

  var sectionEl = section; // クロージャ用
  (function(fileData, grid, cs) {
    btnAll.addEventListener('click', function() {
      Array.from(grid.querySelectorAll('.page-card')).forEach(function(c) { c.classList.add('selected'); });
      updateMergeBulkCount(grid, cs);
    });
    btnNone.addEventListener('click', function() {
      Array.from(grid.querySelectorAll('.page-card')).forEach(function(c) { c.classList.remove('selected'); });
      updateMergeBulkCount(grid, cs);
    });
    btnBL.addEventListener('click', function() { mergeBulkRotate(fileData, grid, cs, -90); });
    btnBR.addEventListener('click', function() { mergeBulkRotate(fileData, grid, cs, 90); });
    btnB180.addEventListener('click', function() { mergeBulkRotate(fileData, grid, cs, 180); });
  })(fd, null, countSpan); // gridはあとでセット

  bulkBar.appendChild(bulkLabel);
  bulkBar.appendChild(btnAll);
  bulkBar.appendChild(btnNone);
  bulkBar.appendChild(sep);
  bulkBar.appendChild(rotLabel);
  bulkBar.appendChild(btnBL);
  bulkBar.appendChild(btnBR);
  bulkBar.appendChild(btnB180);
  bulkBar.appendChild(countSpan);

  var hint = document.createElement('p');
  hint.style.cssText = 'color:#b07aad;font-size:0.78rem;margin-bottom:8px;';
  hint.textContent = '💡 カードをクリックで選択／ドラッグで並び替え';

  var grid = document.createElement('div');
  grid.className = 'pages-grid';
  grid.style.marginTop = '4px';

  // gridが確定してからイベントを正しく繋ぎ直す
  (function(fileData, g, cs) {
    btnAll.onclick = function() {
      Array.from(g.querySelectorAll('.page-card')).forEach(function(c) { c.classList.add('selected'); });
      updateMergeBulkCount(g, cs);
    };
    btnNone.onclick = function() {
      Array.from(g.querySelectorAll('.page-card')).forEach(function(c) { c.classList.remove('selected'); });
      updateMergeBulkCount(g, cs);
    };
    btnBL.onclick = function() { mergeBulkRotate(fileData, g, cs, -90); };
    btnBR.onclick = function() { mergeBulkRotate(fileData, g, cs, 90); };
    btnB180.onclick = function() { mergeBulkRotate(fileData, g, cs, 180); };
  })(fd, grid, countSpan);

  section.appendChild(header);
  section.appendChild(bulkBar);
  section.appendChild(hint);
  section.appendChild(grid);
  setupMergeFileDrag(header, section);
  return section;
}

function updateMergeBulkCount(grid, countSpan) {
  var count = grid.querySelectorAll('.page-card.selected').length;
  countSpan.textContent = count + 'ページ選択中';
}

function mergeBulkRotate(fd, grid, countSpan, deg) {
  var selected = Array.from(grid.querySelectorAll('.page-card.selected'));
  if (selected.length === 0) return;
  selected.forEach(function(card) {
    var idx = parseInt(card.dataset.originalIdx, 10);
    var prev = fd.rotations[idx] || 0;
    fd.rotations[idx] = (prev + deg + 360) % 360;
    delete fd.canvasCache[idx + '_' + prev];
    renderMergeCanvas(card, fd, idx);
  });
}

function createMergeCard(fd, orderIdx, originalIdx) {
  var card = document.createElement('div');
  card.className = 'page-card';
  card.draggable = true;
  card.dataset.fileId = String(fd.id);
  card.dataset.originalIdx = String(originalIdx);

  var check = document.createElement('div');
  check.className = 'page-check';
  check.textContent = '✓';

  var wrap = document.createElement('div');
  wrap.className = 'page-canvas-wrap';

  var label = document.createElement('div');
  label.className = 'page-label';
  label.textContent = 'p.' + (orderIdx + 1);

  var btnArea = document.createElement('div');
  btnArea.className = 'rotate-buttons';

  var btnL = document.createElement('button');
  btnL.type = 'button'; btnL.className = 'rotate-btn';
  btnL.textContent = '↺'; btnL.title = '左に90°回転';

  var btnR = document.createElement('button');
  btnR.type = 'button'; btnR.className = 'rotate-btn';
  btnR.textContent = '↻'; btnR.title = '右に90°回転';

  (function(fileData, c, idx) {
    c.addEventListener('click', function(e) {
      if (e.target.closest('.rotate-btn')) return;
      c.classList.toggle('selected');
      // 親gridとcountSpanを探して更新
      var grid = c.closest('.pages-grid');
      var countSpan = c.closest('.merge-file-section').querySelector('.selected-count');
      if (grid && countSpan) updateMergeBulkCount(grid, countSpan);
    });btnL.addEventListener('click', function(e) {
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
  })(fd, card, originalIdx);

  btnArea.appendChild(btnL);
  btnArea.appendChild(btnR);
  card.appendChild(check);
  card.appendChild(wrap);
  card.appendChild(label);
  card.appendChild(btnArea);
  setupMergeCardDrag(card, fd);
  return card;
}

function renderMergeCanvas(card, fd, originalIdx) {
  var wrap = card.querySelector('.page-canvas-wrap');
  var rotation = fd.rotations[originalIdx] || 0;
  var cacheKey = originalIdx + '_' + rotation;
  var canvas = wrap.querySelector('canvas');
  if (!canvas) { canvas = document.createElement('canvas'); wrap.appendChild(canvas); }
  if (fd.canvasCache[cacheKey]) {
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
      var cc = document.createElement('canvas');
      cc.width = canvas.width; cc.height = canvas.height;
      cc.getContext('2d').drawImage(canvas, 0, 0);
      fd.canvasCache[cacheKey] = cc;
    });
  });
}

function setupMergeCardDrag(card, fd) {
  card.addEventListener('dragstart', function() {
    mergePageDragSrc = card;
    setTimeout(function() { card.classList.add('dragging'); }, 0);
  });
  card.addEventListener('dragend', function() {
    card.classList.remove('dragging');
    mergePageDragSrc = null;
    rebuildMergePageOrder(fd);
    updateMergePageLabels(card.closest('.pages-grid'));
  });
  card.addEventListener('dragover', function(e) {
    e.preventDefault();
    if (mergePageDragSrc && mergePageDragSrc !== card &&
        mergePageDragSrc.dataset.fileId === card.dataset.fileId)
      card.classList.add('drag-over');
  });
  card.addEventListener('dragleave', function() { card.classList.remove('drag-over'); });
  card.addEventListener('drop', function(e) {
    e.preventDefault();
    card.classList.remove('drag-over');
    if (!mergePageDragSrc || mergePageDragSrc === card) return;
    if (mergePageDragSrc.dataset.fileId !== card.dataset.fileId) return;
    var grid = card.closest('.pages-grid');
    var cards = Array.from(grid.querySelectorAll('.page-card'));
    var si = cards.indexOf(mergePageDragSrc);
    var ti = cards.indexOf(card);
    if (si < ti) grid.insertBefore(mergePageDragSrc, card.nextSibling);
    else         grid.insertBefore(mergePageDragSrc, card);
  });
}

function rebuildMergePageOrder(fd) {
  var section = document.querySelector('.merge-file-section[data-file-id="' + fd.id + '"]');
  if (!section) return;
  fd.pageOrder = Array.from(section.querySelectorAll('.page-card'))
    .map(function(c) { return parseInt(c.dataset.originalIdx, 10); });
}

function updateMergePageLabels(grid) {
  Array.from(grid.querySelectorAll('.page-card')).forEach(function(c, i) {
    c.querySelector('.page-label').textContent = 'p.' + (i + 1);
  });
}

function setupMergeFileDrag(header, section) {
  header.addEventListener('dragstart', function(e) {
    mergeFileDragSrc = section;
    setTimeout(function() { header.classList.add('dragging'); }, 0);
    e.stopPropagation();
  });
  header.addEventListener('dragend', function() {
    header.classList.remove('dragging');
    mergeFileDragSrc = null;
    rebuildMergeFilesOrder();});
  header.addEventListener('dragover', function(e) {
    e.preventDefault(); e.stopPropagation();
    if (mergeFileDragSrc && mergeFileDragSrc !== section) header.classList.add('drag-over');
  });
  header.addEventListener('dragleave', function() { header.classList.remove('drag-over'); });
  header.addEventListener('drop', function(e) {
    e.preventDefault(); e.stopPropagation();
    header.classList.remove('drag-over');
    if (!mergeFileDragSrc || mergeFileDragSrc === section) return;
    var list = document.getElementById('merge-files-list');
    var sections = Array.from(list.querySelectorAll('.merge-file-section'));
    var si = sections.indexOf(mergeFileDragSrc);
    var ti = sections.indexOf(section);
    if (si < ti) list.insertBefore(mergeFileDragSrc, section.nextSibling);
    else         list.insertBefore(mergeFileDragSrc, section);
  });
}

function rebuildMergeFilesOrder() {
  var newOrder = [];
  Array.from(document.querySelectorAll('#merge-files-list .merge-file-section'))
    .forEach(function(s) {
      var id = parseInt(s.dataset.fileId, 10);
      var fd = mergeFiles.find(function(f) { return f.id === id; });
      if (fd) newOrder.push(fd);
    });
  mergeFiles = newOrder;
}

function generateMergePDF() {
  if (mergeFiles.length === 0) return;
  rebuildMergeFilesOrder();
  var btn = document.getElementById('merge-download-btn');
  btn.textContent = '⏳ 結合中...'; btn.disabled = true;
  hideMsg('merge-success-msg'); hideMsg('merge-error-msg');

  PDFLib.PDFDocument.create().then(function(newDoc) {
    var chain = Promise.resolve();
    mergeFiles.forEach(function(fd) {
      chain = chain.then(function() {
        rebuildMergePageOrder(fd);
        var copyForPdfLib = new Uint8Array(fd.rawBuffer.slice(0));
        return PDFLib.PDFDocument.load(copyForPdfLib, { ignoreEncryption: true })
          .then(function(srcDoc) {
            var inner = Promise.resolve();
            fd.pageOrder.forEach(function(idx) {
              inner = inner.then(function() {
                return newDoc.copyPages(srcDoc, [idx]).then(function(copied) {
                  var p = copied[0];
                  var rot = fd.rotations[idx] || 0;
                  if (rot !== 0) p.setRotation(PDFLib.degrees(rot));
                  newDoc.addPage(p);
                });
              });
            });
            return inner;
          });
      });
    });
    return chain.then(function() { return newDoc.save({ useObjectStreams: false }); });
  })
  .then(function(bytes) {
    var mergedName = mergeFiles[0].name.replace(/\.pdf$/i, '') + '_merged.pdf';
    downloadBlob(bytes, mergedName);
    showMsg('merge-success-msg');
  })
  .catch(function(err) { showError('merge-error-msg', err); })
  .finally(function() {
    btn.textContent = '📎 結合してダウンロード'; btn.disabled = false;
  });
}

// ==========================
// 共通ユーティリティ
// ==========================
function downloadBlob(bytes, filename) {
  var blob = new Blob([bytes], { type: 'application/pdf' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a);
  setTimeout(function() { URL.revokeObjectURL(url); }, 1000);
}
function showMsg(id) {
  var el = document.getElementById(id); if (!el) return;
  el.style.display = 'block';
  setTimeout(function() { el.style.display = 'none'; }, 4000);
}
function hideMsg(id) {
  var el = document.getElementById(id); if (el) el.style.display = 'none';
}
function showError(id, err) {
  var el = document.getElementById(id); if (!el) return;
  el.textContent = '❌ エラー: ' + (err && err.message ? err.message : String(err));
  el.style.display = 'block';
}
</script>
</body>
</html>
