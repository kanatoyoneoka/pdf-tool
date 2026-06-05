<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌸 PDF結合ツール</title>
<script src="https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>
<script src="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.min.js"></script>
<script src="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #fff8fb; font-family: 'Helvetica Neue', Arial, sans-serif; color: #7a2e5e; min-height: 100vh; }
  h1 { text-align: center; color: #d96ea0; padding: 28px 0 6px; font-size: 1.8rem; }
  .subtitle { text-align: center; color: #b07aad; font-size: 0.9rem; margin-bottom: 24px; }
  .container { max-width: 960px; margin: 0 auto; padding: 0 16px; }

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

  /* 全ページグリッド（ファイルをまたいで並び替え） */
  .all-pages-grid { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 32px; }

  .page-card { background: white; border: 2px solid #f9b8d8; border-radius: 16px; width: 150px; padding: 10px; text-align: center; user-select: none; position: relative; transition: box-shadow 0.2s, border-color 0.15s; }
  .page-card:hover { box-shadow: 0 4px 16px #f9b8d840; }
  .page-card.drag-over-left { border-left: 4px solid #f490c0; }
  .page-card.drag-over-right { border-right: 4px solid #f490c0; }
  .page-card.dragging { opacity: 0.3; }

  .page-checkbox-wrap { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; }
  .page-checkbox { width: 18px; height: 18px; accent-color: #f490c0; cursor: pointer; flex-shrink: 0; }
  .page-checkbox-label { color: #c762a0; font-size: 0.72rem; cursor: pointer; line-height: 1.3; text-align: left; }

  .drag-handle { position: absolute; top: 7px; right: 7px; color: #d9b8d0; font-size: 0.85rem; cursor: grab; padding: 2px 3px; line-height: 1; }
  .drag-handle:active { cursor: grabbing; }

  /*ファイルラベル（カード上部の色帯） */
  .file-badge { font-size: 0.68rem; font-weight: bold; border-radius: 8px; padding: 2px 7px; margin-bottom: 6px; display: inline-block; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

  .page-canvas-wrap { width: 100%; min-height: 80px; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; pointer-events: none; }
  .page-canvas-wrap canvas { width: 100%; border-radius: 8px; display: block; }

  .rotate-buttons { display: flex; justify-content: center; gap: 8px; }
  .rotate-btn { background: #fde8f3; border: 1px solid #f9b8d8; border-radius: 50%; width: 32px; height: 32px; font-size: 1rem; cursor: pointer; color: #c762a0; display: flex; align-items: center; justify-content: center; }
  .rotate-btn:hover { background: #f9b8d8; color: #7a2e5e; }

  /*ファイル管理リスト */
  .file-list-section { background: white; border: 2px solid #f9b8d8; border-radius: 16px; padding: 14px 16px; margin-bottom: 20px; }
  .file-list-row { display: flex; align-items: center; gap: 10px; padding: 6px 0; border-bottom: 1px solid #fde8f3; }
  .file-list-row:last-child { border-bottom: none; }
  .file-list-badge { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; }
  .file-list-name { flex: 1; font-size: 0.9rem; color: #7a2e5e; font-weight: bold; }
  .file-list-pages { color: #b07aad; font-size: 0.8rem; margin-right: 4px; }
  .remove-file-btn { background: #fde8f3; border: 1px solid #f9b8d8; border-radius: 50%; width: 26px; height: 26px; font-size: 0.85rem; cursor: pointer; color: #c762a0; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
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
  <h1>🌸 PDF結合ツール 🌸</h1>
  <p class="subtitle">複数PDFのページを自由に並び替え・回転して結合できます</p>

  <div class="drop-zone" id="drop-zone">
    <div class="drop-zone-title">📄 PDFをここにドロップ</div>
    <span class="drop-zone-sub">何度でも追加できます</span>
    <button class="select-btn" type="button" onclick="document.getElementById('file-input').click()">📂 ファイルを選択</button>
    <input type="file" id="file-input" accept=".pdf" multiple style="display:none;">
  </div>

  <div id="loading"><span class="spinner"></span>読み込み中...🌸</div>

  <div id="main-section" style="display:none;">

    <!--ファイル管理 -->
    <p class="section-title">📁 読み込みファイル</p>
    <div class="file-list-section">
      <div id="file-list"></div>
    </div>

    <!-- 操作バー -->
    <div class="sel-bar">
      <span class="sel-bar-label">選択：</span>
      <button class="sel-bar-btn" type="button" onclick="selectAll()">全選択</button>
      <button class="sel-bar-btn" type="button" onclick="deselectAll()">全解除</button>
      <span style="width:1px;height:20px;background:#f9b8d8;display:inline-block;margin:0 4px;"></span>
      <button class="sel-rotate-btn" type="button" onclick="rotateSelected(-90)">↺ 選択を左回転</button>
      <button class="sel-rotate-btn" type="button" onclick="rotateSelected(90)">↻ 選択を右回転</button>
      <span class="sel-count" id="sel-count">0ページ選択中</span>
    </div>
    <p class="hint-text">💡 チェックで複数選択して回転。☰ をドラッグでファイルをまたいで並び替えできます。</p>

    <!-- 全ページグリッド -->
    <p class="section-title">📋ページ一覧（ドラッグで自由に並び替え）</p>
    <div class="all-pages-grid" id="all-pages-grid"></div>

    <div class="btn-area">
      <button class="download-btn" id="download-btn" type="button" onclick="generatePDF()">📎 結合してダウンロード</button>
    </div><div class="success-msg" id="success-msg">🌸 結合完了！ダウンロードを開始しました！</div>
    <div class="error-msg" id="error-msg"></div>
  </div>
</div>

<script>
pdfjsLib.GlobalWorkerOptions.workerSrc = '';

//ファイルごとの色（バッジ用）
var FILE_COLORS = [
  { bg: '#fde8f3', text: '#c762a0', dot: '#f490c0' },
  { bg: '#e8f0fd', text: '#3a62c0', dot: '#6a9af4' },
  { bg: '#e8fdf0', text: '#2e7a52', dot: '#5ec88a' },
  { bg: '#fdf5e8', text: '#a06020', dot: '#f4b86a' },
  { bg: '#f0e8fd', text: '#6a3ac0', dot: '#a07af4' },
  { bg: '#fde8e8', text: '#c03a3a', dot: '#f47a7a' },
];

var files = [];       // { id, name, rawBuffer, pdfjsDoc, rotations, color }
var fileIdSeq = 0;
var pageDragSrc = null;  // ドラッグ中のカード

// ==========================
// ファイル読み込み
// ==========================
document.getElementById('drop-zone').addEventListener('dragover', function(e){ e.preventDefault(); this.classList.add('dragover'); });
document.getElementById('drop-zone').addEventListener('dragleave', function(){ this.classList.remove('dragover'); });
document.getElementById('drop-zone').addEventListener('drop', function(e){
  e.preventDefault(); this.classList.remove('dragover');
  var fs = Array.from(e.dataTransfer.files).filter(function(f){ return f.name.toLowerCase().endsWith('.pdf'); });
  if(fs.length) loadFiles(fs);
});
document.getElementById('file-input').addEventListener('change', function(){
  var fs = Array.from(this.files).filter(function(f){ return f.name.toLowerCase().endsWith('.pdf'); });
  if(fs.length) loadFiles(fs); this.value = '';
});

function loadFiles(fileList) {
  document.getElementById('loading').style.display = 'block';
  hideMsg('success-msg'); hideMsg('error-msg');
  var chain = Promise.resolve();
  fileList.forEach(function(file) {
    chain = chain.then(function() {
      return new Promise(function(resolve, reject) {
        var reader = new FileReader();
        reader.onload = function(e) {
          var raw = e.target.result;
          var copy = new Uint8Array(raw.slice(0));
          pdfjsLib.getDocument({ data: copy }).promise.then(function(doc) {
            var colorIdx = files.length % FILE_COLORS.length;
            var fd = {
              id: fileIdSeq++,
              name: file.name,
              rawBuffer: raw,
              pdfjsDoc: doc,
              pageCount: doc.numPages,
              rotations: {},
              color: FILE_COLORS[colorIdx]
            };
            for(var i = 0; i < doc.numPages; i++) fd.rotations[i] = 0;
            files.push(fd);
          }).then(resolve).catch(reject);
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
      });
    });
  });
  chain.then(function() {
    rebuildUI();
    document.getElementById('main-section').style.display = 'block';
  }).catch(function(err) {
    showError('error-msg', err);
  }).finally(function() {
    document.getElementById('loading').style.display = 'none';
  });
}

// ==========================
// UI全体を再構築
// ==========================
function rebuildUI() {
  buildFileList();
  buildAllPagesGrid();
  updateSelCount();
}

//ファイル一覧
function buildFileList() {
  var list = document.getElementById('file-list');
  list.innerHTML = '';
  if(files.length === 0) { document.getElementById('main-section').style.display = 'none'; return; }
  files.forEach(function(fd) {
    var row = document.createElement('div'); row.className = 'file-list-row';
    var dot = document.createElement('div');
    dot.className = 'file-list-badge';
    dot.style.background = fd.color.dot;
    var name = document.createElement('span'); name.className = 'file-list-name'; name.textContent = fd.name;
    var pages = document.createElement('span'); pages.className = 'file-list-pages'; pages.textContent = fd.pageCount +'ページ';
    var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'remove-file-btn'; btn.textContent = '✕';
    (function(fileData) {
      btn.onclick = function() {
        files = files.filter(function(f) { return f.id !== fileData.id; });
        // カラー再割り当て
        files.forEach(function(f, idx) { f.color = FILE_COLORS[idx % FILE_COLORS.length]; });
        rebuildUI();
      };
    })(fd);
    row.appendChild(dot); row.appendChild(name); row.appendChild(pages); row.appendChild(btn);
    list.appendChild(row);
  });
}

// ページグリッド（全ファイル横断）
function buildAllPagesGrid() {
  var grid = document.getElementById('all-pages-grid');
  grid.innerHTML = '';
  var promises = [];
  // グリッド上の順序を管理する配列：{ fileId, originalIdx }
  // 既存カードの順序を保持するため、gridOrderを使う
  getAllPageOrder().forEach(function(item) {
    var fd = getFile(item.fileId);
    if(!fd) return;
    var card = createPageCard(fd, item.originalIdx);
    grid.appendChild(card);
    promises.push(renderCanvas(card, fd, item.originalIdx));
  });
  return Promise.all(promises);
}

// グリッドの現在の順序を取得
function getAllPageOrder() {
  var cards = document.querySelectorAll('#all-pages-grid .page-card');
  if(cards.length > 0) {
    // 既にカードがあればその順序を使う
    return Array.from(cards).map(function(c) {
      return { fileId: parseInt(c.dataset.fileId, 10), originalIdx: parseInt(c.dataset.originalIdx, 10) };
    });
  }
  // 初回：ファイル順× ページ順
  var order = [];
  files.forEach(function(fd) {
    for(var i = 0; i < fd.pageCount; i++) order.push({ fileId: fd.id, originalIdx: i });
  });
  return order;
}

function getFile(id) {
  return files.find(function(f) { return f.id === id; }) || null;
}

// ==========================
// ページカード生成
// ==========================
function createPageCard(fd, originalIdx) {
  var card = document.createElement('div');
  card.className = 'page-card';
  card.draggable = false;
  card.dataset.fileId = String(fd.id);
  card.dataset.originalIdx = String(originalIdx);

  // ドラッグハンドル
  var handle = document.createElement('div');
  handle.className = 'drag-handle'; handle.textContent = '☰'; handle.title = 'ドラッグで並び替え';

  // ファイルバッジ
  var badge = document.createElement('span');
  badge.className = 'file-badge';
  badge.style.background = fd.color.bg;
  badge.style.color = fd.color.text;
  badge.textContent = fd.name.replace(/\.pdf$/i, '');

  // チェックボックス
  var cbWrap = document.createElement('div'); cbWrap.className = 'page-checkbox-wrap';
  var cb = document.createElement('input'); cb.type = 'checkbox'; cb.className = 'page-checkbox';
  cb.id = 'cb-' + fd.id + '-' + originalIdx;
  var cbLabel = document.createElement('label'); cbLabel.className = 'page-checkbox-label';
  cbLabel.htmlFor = 'cb-' + fd.id + '-' + originalIdx;
  cbLabel.textContent = 'p.' + (originalIdx + 1);
  cbWrap.appendChild(cb); cbWrap.appendChild(cbLabel);

  // プレビュー
  var wrap = document.createElement('div'); wrap.className = 'page-canvas-wrap';

  // 回転ボタン
  var btnArea = document.createElement('div'); btnArea.className = 'rotate-buttons';
  var btnL = document.createElement('button'); btnL.type = 'button'; btnL.className = 'rotate-btn'; btnL.textContent = '↺';
  var btnR = document.createElement('button'); btnR.type = 'button'; btnR.className = 'rotate-btn'; btnR.textContent = '↻';

  (function(fileData, c, idx) {
    cb.addEventListener('change', updateSelCount);
    btnL.addEventListener('click', function(e) {
      e.stopPropagation();
      fileData.rotations[idx] = ((fileData.rotations[idx] || 0) - 90+ 360) % 360;
      renderCanvas(c, fileData, idx);
    });
    btnR.addEventListener('click', function(e) {
      e.stopPropagation();
      fileData.rotations[idx] = ((fileData.rotations[idx] || 0) + 90) % 360;
      renderCanvas(c, fileData, idx);
    });
    handle.addEventListener('mousedown', function() { c.draggable = true; });
    handle.addEventListener('mouseleave', function() { if(!pageDragSrc) c.draggable = false; });
  })(fd, card, originalIdx);

  btnArea.appendChild(btnL); btnArea.appendChild(btnR);
  card.appendChild(handle);
  card.appendChild(badge);
  card.appendChild(cbWrap);
  card.appendChild(wrap);
  card.appendChild(btnArea);
  setupCardDrag(card);
  return card;
}

// ==========================
// キャンバス描画
// ==========================
function renderCanvas(card, fd, originalIdx) {
  var wrap = card.querySelector('.page-canvas-wrap');
  var rotation = fd.rotations[originalIdx] || 0;
  return fd.pdfjsDoc.getPage(originalIdx + 1).then(function(page) {
    var viewport = page.getViewport({ scale: 0.35, rotation: rotation });
    var canvas = wrap.querySelector('canvas');
    if(!canvas) { canvas = document.createElement('canvas'); wrap.appendChild(canvas); }
    canvas.width = viewport.width; canvas.height = viewport.height;
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return page.render({ canvasContext: ctx, viewport: viewport }).promise;
  });
}

// ==========================
// ドラッグ（ファイルをまたいでOK）
// ==========================
function setupCardDrag(card) {
  card.addEventListener('dragstart', function(e) {
    pageDragSrc = card;
    e.dataTransfer.effectAllowed = 'move';
    setTimeout(function() { card.classList.add('dragging'); }, 0);
  });
  card.addEventListener('dragend', function() {
    card.classList.remove('dragging');
    card.draggable = false;
    pageDragSrc = null;
    document.querySelectorAll('.page-card').forEach(function(c) {
      c.classList.remove('drag-over-left', 'drag-over-right');
    });
  });
  card.addEventListener('dragover', function(e) {
    e.preventDefault();
    if(!pageDragSrc || pageDragSrc === card) return;
    document.querySelectorAll('.page-card').forEach(function(c) {
      c.classList.remove('drag-over-left', 'drag-over-right');
    });
    var rect = card.getBoundingClientRect();
    var mid = rect.left + rect.width / 2;
    if(e.clientX < mid) card.classList.add('drag-over-left');
    else card.classList.add('drag-over-right');
  });
  card.addEventListener('dragleave', function() {
    card.classList.remove('drag-over-left', 'drag-over-right');
  });
  card.addEventListener('drop', function(e) {
    e.preventDefault();
    card.classList.remove('drag-over-left', 'drag-over-right');
    if(!pageDragSrc || pageDragSrc === card) return;
    var grid = document.getElementById('all-pages-grid');
    var rect = card.getBoundingClientRect();
    var mid = rect.left + rect.width / 2;
    if(e.clientX < mid) grid.insertBefore(pageDragSrc, card);
    else grid.insertBefore(pageDragSrc, card.nextSibling);
  });
}

// ==========================
// 選択・回転
// ==========================
function updateSelCount() {
  var count = document.querySelectorAll('#all-pages-grid .page-checkbox:checked').length;
  document.getElementById('sel-count').textContent = count +'ページ選択中';
}
function selectAll() {
  document.querySelectorAll('#all-pages-grid .page-checkbox').forEach(function(cb) { cb.checked = true; });
  updateSelCount();
}
function deselectAll() {
  document.querySelectorAll('#all-pages-grid .page-checkbox').forEach(function(cb) { cb.checked = false; });
  updateSelCount();
}
function rotateSelected(deg) {
  var any = false;
  document.querySelectorAll('#all-pages-grid .page-card').forEach(function(card) {
    var cb = card.querySelector('.page-checkbox');
    if(cb && cb.checked) {
      any = true;
      var fd = getFile(parseInt(card.dataset.fileId, 10));
      var idx = parseInt(card.dataset.originalIdx, 10);
      if(fd) {
        fd.rotations[idx] = ((fd.rotations[idx] || 0) + deg + 360) % 360;
        renderCanvas(card, fd, idx);
      }
    }
  });
  if(!any) alert('ページを選択してから回転してください🌸');
}

// ==========================
// PDF生成
// ==========================
function generatePDF() {
  var btn = document.getElementById('download-btn');
  btn.textContent = '⏳生成中...'; btn.disabled = true;
  hideMsg('success-msg'); hideMsg('error-msg');

  // グリッドの現在順序を取得
  var pageOrder = Array.from(document.querySelectorAll('#all-pages-grid .page-card')).map(function(c) {
    return { fileId: parseInt(c.dataset.fileId, 10), originalIdx: parseInt(c.dataset.originalIdx, 10) };
  });

  // ファイルごとにPDFDocumentをロード
  var loadedDocs = {};
  var chain = Promise.resolve();
  files.forEach(function(fd) {
    chain = chain.then(function() {
      var copy = new Uint8Array(fd.rawBuffer.slice(0));
      return PDFLib.PDFDocument.load(copy, { ignoreEncryption: true }).then(function(doc) {
        loadedDocs[fd.id] = doc;
      });
    });
  });

  chain.then(function() {
    return PDFLib.PDFDocument.create().then(function(newDoc) {
      var inner = Promise.resolve();
      pageOrder.forEach(function(item) {
        inner = inner.then(function() {
          var srcDoc = loadedDocs[item.fileId];
          var fd = getFile(item.fileId);
          if(!srcDoc || !fd) return;
          return newDoc.copyPages(srcDoc, [item.originalIdx]).then(function(copied) {
            var p = copied[0];
            var rot = fd.rotations[item.originalIdx] || 0;
            if(rot !== 0) p.setRotation(PDFLib.degrees(rot));
            newDoc.addPage(p);
          });
        });
      });
      return inner.then(function() { return newDoc.save({ useObjectStreams: false }); });
    });
  }).then(function(bytes) {
    var name = files.length > 0 ? files[0].name.replace(/\.pdf$/i, '') + '_merged.pdf' : 'merged.pdf';
    downloadBlob(bytes, name);
    showMsg('success-msg');
  }).catch(function(err) {
    showError('error-msg', err);
  }).finally(function() {
    btn.textContent = '📎 結合してダウンロード'; btn.disabled = false;
  });
}

// ==========================
// 共通
// ==========================
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
