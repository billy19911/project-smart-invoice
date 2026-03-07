import os
import sys
import socket
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, send_file
from fpdf import FPDF
import tempfile

# ── Base dir ─────────────────────────────────────────────────────────────────
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

def get_db_path():
    return os.path.join(BASE_DIR, 'smartnota.db')

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

# ════════════════════════════════════════════════════════════════════════════
#  SHARED LAYOUT
# ════════════════════════════════════════════════════════════════════════════
_LAYOUT = """<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Smart Nota – {{ page_title }}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --sidebar-w:240px;
  --accent:#4f46e5;
  --accent-light:#eef2ff;
  --accent-dark:#3730a3;
  --bg:#f8fafc;
  --card-bg:#ffffff;
  --text:#1e293b;
  --text-muted:#64748b;
  --border:#e2e8f0;
  --success:#10b981;
  --danger:#ef4444;
  --warning:#f59e0b;
}
*{box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);margin:0;min-height:100vh}

/* ── Sidebar ── */
.sidebar{
  position:fixed;top:0;left:0;width:var(--sidebar-w);height:100vh;
  background:linear-gradient(160deg,#1e1b4b 0%,#312e81 100%);
  display:flex;flex-direction:column;z-index:100;
  box-shadow:4px 0 20px rgba(0,0,0,.15)
}
.sidebar-logo{
  padding:24px 20px 16px;
  border-bottom:1px solid rgba(255,255,255,.1)
}
.sidebar-logo .logo-icon{
  width:40px;height:40px;border-radius:10px;
  background:var(--accent);display:flex;align-items:center;justify-content:center;
  font-size:18px;color:#fff;margin-bottom:10px
}
.sidebar-logo h6{color:#fff;font-weight:700;margin:0;font-size:.9rem;letter-spacing:.3px}
.sidebar-logo small{color:rgba(255,255,255,.5);font-size:.7rem}
.sidebar-nav{padding:16px 12px;flex:1}
.sidebar-nav .nav-label{
  color:rgba(255,255,255,.35);font-size:.65rem;font-weight:600;
  text-transform:uppercase;letter-spacing:.8px;padding:8px 8px 4px
}
.sidebar-nav a{
  display:flex;align-items:center;gap:10px;
  padding:10px 12px;border-radius:8px;
  color:rgba(255,255,255,.7);text-decoration:none;
  font-size:.85rem;font-weight:500;margin-bottom:2px;
  transition:all .2s
}
.sidebar-nav a:hover{background:rgba(255,255,255,.1);color:#fff}
.sidebar-nav a.active{background:rgba(255,255,255,.15);color:#fff}
.sidebar-nav a i{font-size:1rem;width:20px;text-align:center}
.sidebar-footer{
  padding:16px 20px;border-top:1px solid rgba(255,255,255,.1)
}
.ip-box{
  background:rgba(255,255,255,.07);border-radius:8px;
  padding:10px 12px;border:1px solid rgba(255,255,255,.1)
}
.ip-box .label{color:rgba(255,255,255,.4);font-size:.65rem;text-transform:uppercase;letter-spacing:.5px}
.ip-box .ip-val{color:#a5b4fc;font-size:.78rem;font-weight:600;word-break:break-all}

/* ── Main ── */
.main{margin-left:var(--sidebar-w);min-height:100vh}
.topbar{
  background:var(--card-bg);border-bottom:1px solid var(--border);
  padding:14px 28px;display:flex;align-items:center;justify-content:space-between;
  position:sticky;top:0;z-index:50
}
.topbar h5{margin:0;font-weight:700;font-size:1rem;color:var(--text)}
.topbar .breadcrumb{margin:0;font-size:.78rem}
.content{padding:28px}

/* ── Cards ── */
.card{
  background:var(--card-bg);border:1px solid var(--border);
  border-radius:12px;box-shadow:0 1px 4px rgba(0,0,0,.04)
}
.card-header-custom{
  padding:16px 20px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between
}
.card-header-custom h6{margin:0;font-weight:700;font-size:.9rem;color:var(--text)}
.card-body-custom{padding:20px}

/* ── Stat cards ── */
.stat-card{border-radius:12px;padding:20px;position:relative;overflow:hidden}
.stat-card .icon{
  width:44px;height:44px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;font-size:1.2rem
}
.stat-card .value{font-size:1.5rem;font-weight:700;margin-top:12px;margin-bottom:2px}
.stat-card .label{font-size:.78rem;font-weight:500;opacity:.7}
.stat-purple{background:linear-gradient(135deg,#ede9fe,#ddd6fe);color:#4c1d95}
.stat-purple .icon{background:#7c3aed;color:#fff}
.stat-green{background:linear-gradient(135deg,#d1fae5,#a7f3d0);color:#064e3b}
.stat-green .icon{background:#059669;color:#fff}
.stat-blue{background:linear-gradient(135deg,#dbeafe,#bfdbfe);color:#1e3a8a}
.stat-blue .icon{background:#2563eb;color:#fff}
.stat-orange{background:linear-gradient(135deg,#ffedd5,#fed7aa);color:#7c2d12}
.stat-orange .icon{background:#ea580c;color:#fff}

/* ── Form ── */
.form-label{font-size:.8rem;font-weight:600;color:var(--text-muted);margin-bottom:4px;text-transform:uppercase;letter-spacing:.3px}
.form-control,.form-select{
  border:1.5px solid var(--border);border-radius:8px;
  font-size:.88rem;padding:9px 12px;color:var(--text);
  background:var(--card-bg);transition:border-color .2s,box-shadow .2s
}
.form-control:focus,.form-select:focus{
  border-color:var(--accent);box-shadow:0 0 0 3px rgba(79,70,229,.12);outline:none
}
.form-control.readonly-field{background:#f8fafc;color:var(--text-muted)}

/* ── Buttons ── */
.btn{border-radius:8px;font-size:.85rem;font-weight:600;padding:9px 16px;transition:all .2s}
.btn-primary{background:var(--accent);border-color:var(--accent)}
.btn-primary:hover{background:var(--accent-dark);border-color:var(--accent-dark)}
.btn-success{background:var(--success);border-color:var(--success)}
.btn-outline-primary{color:var(--accent);border-color:var(--accent)}
.btn-outline-primary:hover{background:var(--accent);border-color:var(--accent)}
.btn-icon{width:32px;height:32px;padding:0;display:inline-flex;align-items:center;justify-content:center;border-radius:6px}

/* ── Table ── */
.table-custom{width:100%;border-collapse:collapse;font-size:.85rem}
.table-custom thead th{
  background:#f1f5f9;color:var(--text-muted);font-size:.72rem;
  font-weight:700;text-transform:uppercase;letter-spacing:.5px;
  padding:10px 14px;border-bottom:2px solid var(--border);white-space:nowrap
}
.table-custom tbody td{
  padding:11px 14px;border-bottom:1px solid var(--border);
  vertical-align:middle;color:var(--text)
}
.table-custom tbody tr:hover{background:#f8fafc}
.table-custom tbody tr:last-child td{border-bottom:none}
.table-custom tfoot td{
  padding:12px 14px;border-top:2px solid var(--border);
  font-weight:700;background:#f1f5f9
}

/* ── Badge ── */
.badge-pill{border-radius:20px;font-size:.7rem;font-weight:600;padding:3px 10px}
.badge-grosir{background:#ede9fe;color:#5b21b6}
.badge-retail{background:#e0f2fe;color:#0369a1}
.badge-nota{background:#f1f5f9;color:#475569;font-family:monospace;font-size:.78rem;padding:3px 8px;border-radius:4px}

/* ── Alert new product ── */
.panel-baru{
  background:linear-gradient(135deg,#fffbeb,#fef3c7);
  border:1.5px solid #fcd34d;border-radius:10px;padding:16px
}
.panel-baru .panel-title{
  color:#92400e;font-weight:700;font-size:.85rem;
  display:flex;align-items:center;gap:6px;margin-bottom:12px
}

/* ── Total row ── */
.total-row{
  background:linear-gradient(135deg,var(--accent),var(--accent-dark));
  color:#fff;border-radius:8px;padding:14px 20px;
  display:flex;justify-content:space-between;align-items:center;margin-top:12px
}
.total-row .label{font-size:.85rem;opacity:.85}
.total-row .amount{font-size:1.4rem;font-weight:700}

/* ── Empty state ── */
.empty-state{text-align:center;padding:48px 20px;color:var(--text-muted)}
.empty-state i{font-size:3rem;opacity:.3;display:block;margin-bottom:12px}
.empty-state p{font-size:.9rem}

/* ── Nota detail print ── */
@media print{
  .sidebar,.topbar,.no-print{display:none!important}
  .main{margin-left:0}
  .content{padding:10px}
}

/* ── Responsive ── */
@media(max-width:768px){
  .sidebar{width:100%;height:auto;position:relative;flex-direction:row;flex-wrap:wrap}
  .sidebar-nav{display:flex;flex-direction:row;flex-wrap:wrap;padding:8px}
  .sidebar-nav .nav-label{display:none}
  .sidebar-nav a{padding:8px 10px;font-size:.8rem}
  .sidebar-footer{display:none}
  .main{margin-left:0}
  .content{padding:16px}
  .topbar{padding:10px 16px}
}

/* ── Animations ── */
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.fade-in{animation:fadeIn .3s ease}

/* ── Toast ── */
.toast-container{position:fixed;bottom:24px;right:24px;z-index:9999}
</style>
</head>
<body>

<!-- ═══ SIDEBAR ═══ -->
<div class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-icon"><i class="bi bi-receipt-cutoff"></i></div>
    <h6>Smart Nota</h6>
    <small>Portable v1.0</small>
  </div>
  <nav class="sidebar-nav">
    <div class="nav-label">Menu</div>
    <a href="/" class="{{ 'active' if active=='home' else '' }}">
      <i class="bi bi-grid-fill"></i> Dashboard
    </a>
    <a href="/nota/baru" class="{{ 'active' if active=='nota' else '' }}">
      <i class="bi bi-plus-circle-fill"></i> Buat Nota
    </a>
    <a href="/riwayat" class="{{ 'active' if active=='riwayat' else '' }}">
      <i class="bi bi-clock-history"></i> Riwayat Nota
    </a>
    <a href="/produk" class="{{ 'active' if active=='produk' else '' }}">
      <i class="bi bi-box-seam"></i> Daftar Produk
    </a>
  </nav>
  <div class="sidebar-footer">
    <div class="ip-box">
      <div class="label">Akses dari HP</div>
      <div class="ip-val"><i class="bi bi-wifi me-1"></i>http://{{ ip }}:5000</div>
    </div>
    <div style="text-align:center;margin-top:10px;color:rgba(255,255,255,.25);font-size:.68rem;letter-spacing:.3px">
      design by <span style="color:#a5b4fc;font-weight:600">bil</span>
    </div>
  </div>
</div>

<!-- ═══ MAIN ═══ -->
<div class="main">
  <div class="topbar">
    <div>
      <h5>{{ page_title }}</h5>
      <nav aria-label="breadcrumb" class="d-none d-md-block">
        <ol class="breadcrumb mb-0">
          <li class="breadcrumb-item"><a href="/" class="text-decoration-none">Home</a></li>
          {% if breadcrumb %}<li class="breadcrumb-item active">{{ breadcrumb }}</li>{% endif %}
        </ol>
      </nav>
    </div>
    <div class="d-flex align-items-center gap-2">
      <span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25 rounded-pill px-3 py-2" style="font-size:.75rem">
        <i class="bi bi-circle-fill me-1" style="font-size:.4rem;vertical-align:middle"></i>Server Aktif
      </span>
    </div>
  </div>
  <div class="content fade-in">
    {% block content %}{% endblock %}
  </div>
</div>

<!-- Toast container -->
<div class="toast-container" id="toastContainer"></div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
function showToast(msg, type='success'){
  const colors = {success:'#10b981',danger:'#ef4444',warning:'#f59e0b',info:'#3b82f6'};
  const icons  = {success:'bi-check-circle-fill',danger:'bi-x-circle-fill',warning:'bi-exclamation-triangle-fill',info:'bi-info-circle-fill'};
  const el = document.createElement('div');
  el.className='toast show align-items-center border-0 mb-2';
  el.style.cssText=`background:${colors[type]||colors.success};color:#fff;border-radius:10px;min-width:260px;box-shadow:0 4px 20px rgba(0,0,0,.15)`;
  el.innerHTML=`<div class="d-flex align-items-center gap-2 p-3">
    <i class="bi ${icons[type]||icons.success} fs-5"></i>
    <span style="font-size:.88rem;font-weight:500">${msg}</span>
    <button type="button" class="btn-close btn-close-white ms-auto" onclick="this.closest('.toast').remove()"></button>
  </div>`;
  document.getElementById('toastContainer').appendChild(el);
  setTimeout(()=>el.remove(), 3500);
}
function fmt(n){return Number(n).toLocaleString('id-ID')}
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML}
</script>
{% block scripts %}{% endblock %}
</body>
</html>"""

# ════════════════════════════════════════════════════════════════════════════
#  DASHBOARD (index)
# ════════════════════════════════════════════════════════════════════════════
INDEX_HTML = _LAYOUT.replace('{% block content %}{% endblock %}', """{% block content %}
<div class="row g-3 mb-4">
  <div class="col-6 col-lg-3">
    <div class="stat-card stat-purple">
      <div class="icon"><i class="bi bi-receipt-cutoff"></i></div>
      <div class="value">{{ stats.total_nota }}</div>
      <div class="label">Total Nota</div>
    </div>
  </div>
  <div class="col-6 col-lg-3">
    <div class="stat-card stat-green">
      <div class="icon"><i class="bi bi-cash-stack"></i></div>
      <div class="value">{{ stats.omzet_fmt }}</div>
      <div class="label">Total Omzet</div>
    </div>
  </div>
  <div class="col-6 col-lg-3">
    <div class="stat-card stat-blue">
      <div class="icon"><i class="bi bi-box-seam"></i></div>
      <div class="value">{{ stats.total_produk }}</div>
      <div class="label">Produk Tersimpan</div>
    </div>
  </div>
  <div class="col-6 col-lg-3">
    <div class="stat-card stat-orange">
      <div class="icon"><i class="bi bi-calendar-day"></i></div>
      <div class="value">{{ stats.nota_hari }}</div>
      <div class="label">Nota Hari Ini</div>
    </div>
  </div>
</div>

<div class="row g-3">
  <!-- Quick action -->
  <div class="col-lg-4">
    <div class="card h-100">
      <div class="card-header-custom">
        <h6><i class="bi bi-lightning-fill text-warning me-2"></i>Aksi Cepat</h6>
      </div>
      <div class="card-body-custom d-flex flex-column gap-2">
        <a href="/nota/baru" class="btn btn-primary d-flex align-items-center gap-2 justify-content-center py-3">
          <i class="bi bi-plus-circle-fill fs-5"></i>
          <div class="text-start">
            <div>Buat Nota Baru</div>
            <small class="opacity-75 fw-normal" style="font-size:.72rem">Input penjualan baru</small>
          </div>
        </a>
        <a href="/riwayat" class="btn btn-outline-primary d-flex align-items-center gap-2 justify-content-center py-3">
          <i class="bi bi-clock-history fs-5"></i>
          <div class="text-start">
            <div>Lihat Riwayat</div>
            <small class="opacity-75 fw-normal" style="font-size:.72rem">Semua nota tersimpan</small>
          </div>
        </a>
        <a href="/produk" class="btn btn-outline-secondary d-flex align-items-center gap-2 justify-content-center py-3">
          <i class="bi bi-box-seam fs-5"></i>
          <div class="text-start">
            <div>Kelola Produk</div>
            <small class="opacity-75 fw-normal" style="font-size:.72rem">Lihat daftar harga</small>
          </div>
        </a>
        <div class="mt-2 p-3 rounded-3" style="background:#f0fdf4;border:1px solid #bbf7d0">
          <div class="d-flex align-items-center gap-2 mb-1">
            <i class="bi bi-phone-fill text-success"></i>
            <span style="font-size:.78rem;font-weight:700;color:#166534">Akses dari HP</span>
          </div>
          <div style="font-size:.85rem;font-weight:700;color:#15803d">http://{{ ip }}:5000</div>
          <div style="font-size:.7rem;color:#4ade80;margin-top:2px">Pastikan 1 jaringan Wi-Fi</div>
        </div>
      </div>
    </div>
  </div>
  <!-- Nota terbaru -->
  <div class="col-lg-8">
    <div class="card">
      <div class="card-header-custom">
        <h6><i class="bi bi-clock-history me-2"></i>Nota Terbaru</h6>
        <a href="/riwayat" class="btn btn-sm btn-outline-primary">Lihat Semua</a>
      </div>
      <div class="card-body-custom p-0">
        {% if recent_notas %}
        <table class="table-custom w-100">
          <thead>
            <tr>
              <th>No. Nota</th><th>Pelanggan</th><th>Tanggal</th>
              <th class="text-end">Total</th><th class="text-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            {% for n in recent_notas %}
            <tr>
              <td><span class="badge-nota">{{ n.nomor }}</span></td>
              <td>{{ n.pelanggan or '–' }}</td>
              <td style="color:var(--text-muted);font-size:.82rem">{{ n.tanggal }}</td>
              <td class="text-end fw-semibold">Rp {{ '{:,.0f}'.format(n.total).replace(',','.') }}</td>
              <td class="text-center">
                <a href="/detail/{{ n.id }}" class="btn btn-sm btn-outline-primary btn-icon" title="Detail">
                  <i class="bi bi-eye"></i>
                </a>
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        {% else %}
        <div class="empty-state">
          <i class="bi bi-receipt"></i>
          <p>Belum ada nota. <a href="/nota/baru">Buat sekarang →</a></p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
{% endblock %}""").replace('{% block scripts %}{% endblock %}', '{% block scripts %}{% endblock %}')

# ════════════════════════════════════════════════════════════════════════════
#  INPUT NOTA
# ════════════════════════════════════════════════════════════════════════════
NOTA_HTML = _LAYOUT.replace('{% block content %}{% endblock %}', """{% block content %}
<div class="row g-3">
  <!-- Left: Form input -->
  <div class="col-lg-7">
    <!-- Info pelanggan -->
    <div class="card mb-3">
      <div class="card-header-custom">
        <h6><i class="bi bi-person-fill me-2"></i>Info Pelanggan</h6>
      </div>
      <div class="card-body-custom">
        <label class="form-label">Nama Pelanggan</label>
        <input type="text" id="pelanggan" class="form-control" placeholder="Opsional – kosongkan jika umum">
      </div>
    </div>

    <!-- Tambah barang -->
    <div class="card mb-3">
      <div class="card-header-custom">
        <h6><i class="bi bi-plus-circle-fill me-2 text-primary"></i>Tambah Barang</h6>
      </div>
      <div class="card-body-custom">
        <div class="row g-3 mb-3">
          <div class="col-12">
            <label class="form-label">Nama Barang</label>
            <div class="position-relative">
              <input type="text" id="inp-nama" class="form-control"
                     placeholder="Ketik nama barang…" autocomplete="off">
              <div id="saran-dropdown" style="
                display:none;position:absolute;top:100%;left:0;right:0;z-index:999;
                background:#fff;border:1.5px solid var(--accent);border-top:none;
                border-radius:0 0 8px 8px;max-height:200px;overflow-y:auto;
                box-shadow:0 4px 16px rgba(79,70,229,.12)">
              </div>
            </div>
          </div>
        </div>
        <div class="row g-3 mb-3">
          <div class="col-4">
            <label class="form-label">Qty</label>
            <input type="number" id="inp-qty" class="form-control" min="1" value="1">
          </div>
          <div class="col-4">
            <label class="form-label">Harga Satuan</label>
            <div class="input-group">
              <span class="input-group-text" style="font-size:.8rem;background:#f8fafc;border-color:var(--border)">Rp</span>
              <input type="number" id="inp-harga" class="form-control" min="0" placeholder="0">
            </div>
          </div>
          <div class="col-4">
            <label class="form-label">Subtotal</label>
            <input type="text" id="inp-subtotal" class="form-control readonly-field" readonly>
          </div>
        </div>

        <!-- Panel barang baru -->
        <div id="panel-baru" class="panel-baru d-none mb-3">
          <div class="panel-title">
            <i class="bi bi-stars"></i> Produk Baru! Simpan info harga ke database
          </div>
          <div class="row g-2">
            <div class="col-md-3 col-6">
              <label class="form-label">Harga Retail</label>
              <div class="input-group input-group-sm">
                <span class="input-group-text">Rp</span>
                <input type="number" id="inp-ret" class="form-control" min="0" placeholder="0">
              </div>
            </div>
            <div class="col-md-3 col-6">
              <label class="form-label">Harga Grosir</label>
              <div class="input-group input-group-sm">
                <span class="input-group-text">Rp</span>
                <input type="number" id="inp-gro" class="form-control" min="0" placeholder="0">
              </div>
            </div>
            <div class="col-md-3 col-6">
              <label class="form-label">Min Qty Grosir</label>
              <input type="number" id="inp-min-gro" class="form-control form-control-sm" min="1" value="10">
            </div>
            <div class="col-md-3 col-6">
              <label class="form-label">Satuan</label>
              <input type="text" id="inp-satuan" class="form-control form-control-sm" list="list-satuan-nota" maxlength="20" value="pcs">
              <datalist id="list-satuan-nota">
                <option value="pcs">
                <option value="pack">
                <option value="lusin">
                <option value="doz">
                <option value="box">
                <option value="roll">
                <option value="set">
              </datalist>
            </div>
          </div>
        </div>

        <button class="btn btn-primary w-100 py-2" onclick="tambahItem()">
          <i class="bi bi-plus-lg me-2"></i>Tambahkan ke Nota
        </button>
      </div>
    </div>
  </div>

  <!-- Right: Preview nota -->
  <div class="col-lg-5">
    <div class="card" style="position:sticky;top:80px">
      <div class="card-header-custom">
        <h6><i class="bi bi-file-earmark-text me-2"></i>Preview Nota</h6>
        <span class="badge bg-secondary rounded-pill" id="badge-count">0 item</span>
      </div>
      <div class="card-body-custom p-0">
        <table class="table-custom">
          <thead>
            <tr>
              <th>Barang</th><th class="text-center">Qty</th>
              <th class="text-end">Harga</th><th></th>
            </tr>
          </thead>
          <tbody id="tbl-items">
            <tr id="tr-empty">
              <td colspan="4" class="empty-state py-4">
                <i class="bi bi-cart-x d-block mb-2" style="font-size:1.5rem;opacity:.3"></i>
                <span style="font-size:.82rem">Belum ada item</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-body-custom pt-0">
        <div class="total-row">
          <span class="label"><i class="bi bi-calculator me-1"></i>TOTAL</span>
          <span class="amount" id="total-display">Rp 0</span>
        </div>
        <div class="d-flex gap-2 mt-3">
          <button class="btn btn-outline-danger flex-fill" onclick="resetForm()">
            <i class="bi bi-trash me-1"></i>Reset
          </button>
          <button class="btn btn-success flex-fill py-2" onclick="simpanNota()">
            <i class="bi bi-save-fill me-1"></i>Simpan Nota
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}""").replace('{% block scripts %}{% endblock %}', """{% block scripts %}
<script>
// ── State ────────────────────────────────────────────────────────────────────
let items = [];
let produkCache = {};
let allProduk = [];   // [nama]
const DRAFT_KEY = 'smartnota_draft';

// ── Load semua produk dari server ─────────────────────────────────────────────
fetch('/api/produk/list').then(r=>r.json()).then(list=>{ allProduk = list; });

// ── Restore draft dari localStorage ──────────────────────────────────────────
(function restoreDraft(){
  try {
    const raw = localStorage.getItem(DRAFT_KEY);
    if(!raw) return;
    const d = JSON.parse(raw);
    if(d.pelanggan) document.getElementById('pelanggan').value = d.pelanggan;
    if(d.items && d.items.length > 0){
      items = d.items;
      renderTable();
      showToast('Draft tersimpan dipulihkan ✓','info');
    }
  } catch(e){}
})();

function saveDraft(){
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify({
      pelanggan: document.getElementById('pelanggan').value,
      items
    }));
  } catch(e){}
}
function clearDraft(){ localStorage.removeItem(DRAFT_KEY); }

// ── Fuzzy/contains search ─────────────────────────────────────────────────────
const inpNama    = document.getElementById('inp-nama');
const dropdown   = document.getElementById('saran-dropdown');
const inpQty     = document.getElementById('inp-qty');
const inpHarga   = document.getElementById('inp-harga');
const inpSub     = document.getElementById('inp-subtotal');
const panelBaru  = document.getElementById('panel-baru');

function scoreMatch(query, target){
  const q = query.toLowerCase();
  const t = target.toLowerCase();
  if(t === q) return 100;
  if(t.startsWith(q)) return 80;
  if(t.includes(q)) return 60;
  // karakter berurutan (fuzzy)
  let i=0, bonus=0;
  for(let c of q){ const idx=t.indexOf(c,i); if(idx>=0){i=idx+1;bonus++;}else return 0; }
  return bonus;
}

function showDropdown(query){
  if(!query){ dropdown.style.display='none'; return; }
  const results = allProduk
    .map(n=>({ nama:n, score:scoreMatch(query,n) }))
    .filter(x=>x.score>0)
    .sort((a,b)=>b.score-a.score)
    .slice(0,8);
  if(!results.length){ dropdown.style.display='none'; return; }
  dropdown.innerHTML = results.map(r=>{
    const hi = r.nama.replace(new RegExp('('+escRe(query)+')','gi'),
                               '<strong style="color:var(--accent)">$1</strong>');
    return `<div class="saran-item" data-nama="${esc(r.nama)}"
                 style="padding:9px 14px;cursor:pointer;font-size:.86rem;
                        display:flex;align-items:center;gap:8px;
                        border-bottom:1px solid var(--border)">
              <i class="bi bi-box-seam" style="color:var(--text-muted);font-size:.8rem"></i>
              ${hi}
            </div>`;
  }).join('');
  dropdown.style.display='block';
  dropdown.querySelectorAll('.saran-item').forEach(el=>{
    el.addEventListener('mouseenter',()=>el.style.background='var(--accent-light)');
    el.addEventListener('mouseleave',()=>el.style.background='');
    el.addEventListener('mousedown', e=>{
      e.preventDefault();
      pilihProduk(el.dataset.nama);
    });
  });
}

function escRe(s){ return s.split('').map(c=>'.^$*+?()[]{}|\\\\'.indexOf(c)>=0?'\\\\'+c:c).join(''); }

inpNama.addEventListener('input', ()=>{ showDropdown(inpNama.value.trim()); });
inpNama.addEventListener('blur',  ()=>{ setTimeout(()=>dropdown.style.display='none',150); });
inpNama.addEventListener('focus', ()=>{ if(inpNama.value.trim()) showDropdown(inpNama.value.trim()); });

// Navigasi keyboard di dropdown
inpNama.addEventListener('keydown', e=>{
  const items2 = dropdown.querySelectorAll('.saran-item');
  const active = dropdown.querySelector('.saran-active');
  if(e.key==='ArrowDown'){
    e.preventDefault();
    if(!items2.length) return;
    if(!active){ items2[0].classList.add('saran-active'); items2[0].style.background='var(--accent-light)'; }
    else {
      const idx = [...items2].indexOf(active);
      active.classList.remove('saran-active'); active.style.background='';
      const next = items2[(idx+1)%items2.length];
      next.classList.add('saran-active'); next.style.background='var(--accent-light)';
    }
  } else if(e.key==='ArrowUp'){
    e.preventDefault();
    if(!items2.length) return;
    if(!active){ items2[items2.length-1].classList.add('saran-active'); items2[items2.length-1].style.background='var(--accent-light)'; }
    else {
      const idx = [...items2].indexOf(active);
      active.classList.remove('saran-active'); active.style.background='';
      const prev = items2[(idx-1+items2.length)%items2.length];
      prev.classList.add('saran-active'); prev.style.background='var(--accent-light)';
    }
  } else if(e.key==='Enter'){
    if(active){ e.preventDefault(); pilihProduk(active.dataset.nama); }
    else if(dropdown.style.display==='block' && items2.length===1){
      e.preventDefault(); pilihProduk(items2[0].dataset.nama);
    } else {
      e.preventDefault();
      dropdown.style.display='none';
      lookupNama(inpNama.value.trim());
    }
  } else if(e.key==='Tab'||e.key==='Escape'){
    dropdown.style.display='none';
  }
});

async function pilihProduk(nama){
  inpNama.value = nama;
  dropdown.style.display = 'none';
  await lookupNama(nama);
  inpQty.focus();
}

async function lookupNama(nama){
  if(!nama) return;
  const key = nama.toLowerCase();
  if(produkCache[key]){ applyProduk(produkCache[key]); return; }
  const res = await fetch('/api/produk/'+encodeURIComponent(nama));
  const d   = await res.json();
  if(d.found){
    produkCache[key] = {...d, is_new:false};
    applyProduk(produkCache[key]);
    panelBaru.classList.add('d-none');
  } else {
    produkCache[key] = {harga_ret:0,harga_gro:0,min_gro:10,satuan:'pcs',is_new:true};
    inpHarga.value = '';
    panelBaru.classList.remove('d-none');
    document.getElementById('inp-satuan').value = 'pcs';
  }
}

// Trigger lookup saat blur dari field nama (kalau tidak pilih dari dropdown)
inpNama.addEventListener('blur', ()=>{
  const nama = inpNama.value.trim();
  if(nama) lookupNama(nama);
});

function applyProduk(p){
  const qty = parseInt(inpQty.value)||1;
  const harga = (qty>=p.min_gro&&p.min_gro>0) ? p.harga_gro : p.harga_ret;
  inpHarga.value = harga;
  updateSubtotal();
}
inpQty.addEventListener('input', ()=>{
  const key = inpNama.value.trim().toLowerCase();
  if(produkCache[key]) applyProduk(produkCache[key]);
  updateSubtotal();
});
inpHarga.addEventListener('input', updateSubtotal);

// Saat isi inp-ret → otomatis isi inp-harga juga (biar subtotal langsung update)
document.getElementById('inp-ret').addEventListener('input', ()=>{
  const val = document.getElementById('inp-ret').value;
  if(!inpHarga.value) { inpHarga.value = val; updateSubtotal(); }
});

function updateSubtotal(){
  const qty   = parseInt(inpQty.value)||0;
  const harga = parseFloat(inpHarga.value)||
                parseFloat(document.getElementById('inp-ret').value)||0;
  inpSub.value = qty&&harga ? 'Rp '+fmt(qty*harga) : '';
}

// ── Tambah item ───────────────────────────────────────────────────────────────
function tambahItem(){
  const nama  = inpNama.value.trim();
  const qty   = parseInt(inpQty.value)||0;
  if(!nama)  return showToast('Nama barang wajib diisi!','danger');
  if(qty<=0) return showToast('Qty harus lebih dari 0!','danger');

  const key    = nama.toLowerCase();
  const isNew  = produkCache[key]?.is_new ?? true;

  // Untuk produk baru: ambil harga dari inp-ret jika inp-harga kosong
  let hargaRet = parseFloat(document.getElementById('inp-ret').value)||0;
  let hargaGro = parseFloat(document.getElementById('inp-gro').value)||0;
  let minGro   = parseInt(document.getElementById('inp-min-gro').value)||10;
  let satuan   = (document.getElementById('inp-satuan').value || 'pcs').trim().toLowerCase();
  let harga    = parseFloat(inpHarga.value)||0;
  if(!satuan) satuan = 'pcs';

  if(isNew && harga<=0 && hargaRet>0) harga = hargaRet;
  if(isNew && hargaGro<=0) hargaGro = hargaRet||harga;

  if(harga<=0) return showToast('Isi harga terlebih dahulu!','danger');

  let extra = {harga_ret:harga, harga_gro:harga, min_gro:10, satuan:'pcs', is_new:false};
  if(produkCache[key] && !isNew){
    extra = {...produkCache[key]};
  } else if(isNew) {
    extra = {harga_ret:hargaRet||harga, harga_gro:hargaGro||harga, min_gro:minGro, satuan:satuan, is_new:true};
    produkCache[key] = {...extra};
  }

  const isGrosir = (qty >= extra.min_gro && extra.min_gro > 0);
  const hargaFinal = isGrosir ? extra.harga_gro : extra.harga_ret;
  items.push({nama, qty, harga:hargaFinal, subtotal:qty*hargaFinal,
              harga_ret:extra.harga_ret, harga_gro:extra.harga_gro,
              min_gro:extra.min_gro, satuan:extra.satuan || 'pcs', is_new:extra.is_new, isGrosir});
  renderTable();
  saveDraft();
  showToast(nama+' ditambahkan ✓','success');
  inpNama.value=''; inpQty.value=1; inpHarga.value=''; inpSub.value='';
  panelBaru.classList.add('d-none');
  document.getElementById('inp-ret').value='';
  document.getElementById('inp-gro').value='';
  document.getElementById('inp-min-gro').value=10;
  document.getElementById('inp-satuan').value='pcs';
  inpNama.focus();
}

function hapusItem(idx){
  const nama = items[idx].nama;
  items.splice(idx,1);
  renderTable();
  saveDraft();  // ← autosave
  showToast(nama+' dihapus','warning');
}

function renderTable(){
  const tbody = document.getElementById('tbl-items');
  let total=0, html='';
  items.forEach((it,i)=>{
    total+=it.subtotal;
    html+=`<tr>
      <td>
        <div style="font-weight:500">${esc(it.nama)}</div>
        <small style="color:var(--text-muted)">
          ${it.isGrosir
            ? '<span class="badge-pill badge-grosir"><i class="bi bi-tag-fill me-1"></i>Grosir</span>'
            : '<span class="badge-pill badge-retail"><i class="bi bi-tag me-1"></i>Retail</span>'}
        </small>
      </td>
      <td class="text-center fw-semibold">${it.qty} ${esc(it.satuan || 'pcs')}</td>
      <td class="text-end" style="font-size:.82rem">Rp ${fmt(it.harga)}</td>
      <td class="text-end">
        <button class="btn btn-sm btn-icon btn-outline-danger" onclick="hapusItem(${i})">
          <i class="bi bi-trash3"></i>
        </button>
      </td>
    </tr>`;
  });
  if(!html) html=`<tr><td colspan="4" class="empty-state py-4">
    <i class="bi bi-cart-x d-block mb-2" style="font-size:1.5rem;opacity:.3"></i>
    <span style="font-size:.82rem">Belum ada item</span></td></tr>`;
  tbody.innerHTML = html;
  document.getElementById('total-display').textContent = 'Rp '+fmt(total);
  document.getElementById('badge-count').textContent   = items.length+' item';
}

// ── Simpan nota ───────────────────────────────────────────────────────────────
async function simpanNota(){
  if(!items.length) return showToast('Tambahkan minimal 1 barang!','warning');
  const pelanggan = document.getElementById('pelanggan').value.trim();
  const btn = document.querySelector('[onclick="simpanNota()"]');
  btn.disabled=true;
  btn.innerHTML='<span class="spinner-border spinner-border-sm me-2"></span>Menyimpan…';
  try{
    const res = await fetch('/api/simpan',{
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({pelanggan,items})
    });
    const d = await res.json();
    if(d.ok){
      clearDraft();   // ← hapus draft setelah berhasil simpan
      showToast('Nota '+d.nomor+' berhasil disimpan!','success');
      setTimeout(()=>window.location='/detail/'+d.nota_id, 800);
    } else {
      showToast('Gagal: '+d.msg,'danger');
      btn.disabled=false;
      btn.innerHTML='<i class="bi bi-save-fill me-1"></i>Simpan Nota';
    }
  } catch(e){
    showToast('Koneksi gagal','danger');
    btn.disabled=false;
    btn.innerHTML='<i class="bi bi-save-fill me-1"></i>Simpan Nota';
  }
}

// ── Reset ─────────────────────────────────────────────────────────────────────
async function resetForm(){
  if(items.length>0 && !confirm('Reset semua item? Produk baru akan tetap tersimpan.')) return;
  // Simpan produk baru ke DB sebelum reset (biar tidak hilang)
  const produkBaru = items.filter(i=>i.is_new);
  if(produkBaru.length > 0){
    await fetch('/api/produk/batch', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(produkBaru)
    });
    // Update allProduk supaya muncul di suggestion
    produkBaru.forEach(p=>{ if(!allProduk.includes(p.nama)) allProduk.push(p.nama); });
    showToast(produkBaru.length+' produk baru tersimpan ke database','info');
  }
  items=[];
  renderTable();
  clearDraft();
  document.getElementById('pelanggan').value='';
  showToast('Form direset','info');
}

// Autosave pelanggan saat diketik
document.getElementById('pelanggan').addEventListener('input', saveDraft);

// Enter navigation
inpQty.addEventListener('keydown', e=>{
  if(e.key==='Enter'){e.preventDefault(); tambahItem();}
});
</script>
{% endblock %}""")

# ════════════════════════════════════════════════════════════════════════════
#  RIWAYAT
# ════════════════════════════════════════════════════════════════════════════
RIWAYAT_HTML = _LAYOUT.replace('{% block content %}{% endblock %}', """{% block content %}
<!-- Search & filter bar -->
<div class="card mb-3">
  <div class="card-body-custom">
    <div class="row g-2 align-items-center">
      <div class="col-md-6">
        <div class="input-group">
          <span class="input-group-text" style="background:#f8fafc;border-color:var(--border)">
            <i class="bi bi-search text-muted"></i>
          </span>
          <input type="text" class="form-control" id="search-input"
                 placeholder="Cari no. nota atau pelanggan…" oninput="filterTable()">
        </div>
      </div>
      <div class="col-md-3">
        <input type="date" class="form-control" id="filter-date" onchange="filterTable()">
      </div>
      <div class="col-md-3 text-end">
        <a href="/nota/baru" class="btn btn-primary w-100">
          <i class="bi bi-plus-lg me-1"></i>Nota Baru
        </a>
      </div>
    </div>
  </div>
</div>

<div class="card">
  <div class="card-header-custom">
    <h6><i class="bi bi-table me-2"></i>Daftar Nota (<span id="count-label">{{ notas|length }}</span>)</h6>
    <span class="badge bg-primary rounded-pill">{{ notas|length }} total</span>
  </div>
  {% if notas %}
  <div class="card-body-custom p-0">
    <div class="table-responsive">
      <table class="table-custom" id="nota-table">
        <thead>
          <tr>
            <th>#</th>
            <th>No. Nota</th>
            <th>Pelanggan</th>
            <th>Tanggal</th>
            <th>Jml Item</th>
            <th class="text-end">Total</th>
            <th class="text-center">Aksi</th>
          </tr>
        </thead>
        <tbody>
          {% for n in notas %}
          <tr data-nomor="{{ n.nomor }}" data-pelanggan="{{ n.pelanggan or '' }}" data-tanggal="{{ n.tanggal }}">
            <td style="color:var(--text-muted);font-size:.8rem">{{ loop.index }}</td>
            <td><span class="badge-nota">{{ n.nomor }}</span></td>
            <td>
              {% if n.pelanggan %}
              <span class="d-flex align-items-center gap-1">
                <span style="width:26px;height:26px;background:var(--accent-light);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:700;color:var(--accent)">
                  {{ n.pelanggan[0]|upper }}
                </span>
                {{ n.pelanggan }}
              </span>
              {% else %}
              <span style="color:var(--text-muted)">–</span>
              {% endif %}
            </td>
            <td style="color:var(--text-muted);font-size:.82rem">{{ n.tanggal }}</td>
            <td>
              <span class="badge bg-light text-secondary border">{{ n.item_count }} item</span>
            </td>
            <td class="text-end fw-semibold" style="color:var(--accent)">
              Rp {{ '{:,.0f}'.format(n.total).replace(',','.') }}
            </td>
            <td class="text-center">
              <div class="d-flex gap-1 justify-content-center">
                <a href="/detail/{{ n.id }}" class="btn btn-sm btn-outline-primary btn-icon" title="Detail">
                  <i class="bi bi-eye"></i>
                </a>
                <a href="/pdf/{{ n.id }}" class="btn btn-sm btn-outline-danger btn-icon" title="PDF">
                  <i class="bi bi-file-pdf"></i>
                </a>
                <button class="btn btn-sm btn-outline-secondary btn-icon" title="Hapus"
                        onclick="hapus({{ n.id }}, '{{ n.nomor }}')">
                  <i class="bi bi-trash3"></i>
                </button>
              </div>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
  {% else %}
  <div class="card-body-custom">
    <div class="empty-state">
      <i class="bi bi-inbox"></i>
      <p>Belum ada nota tersimpan.</p>
      <a href="/nota/baru" class="btn btn-primary">Buat Nota Pertama</a>
    </div>
  </div>
  {% endif %}
</div>
{% endblock %}""").replace('{% block scripts %}{% endblock %}', """{% block scripts %}
<script>
function filterTable(){
  const q    = document.getElementById('search-input').value.toLowerCase();
  const date = document.getElementById('filter-date').value;
  const rows = document.querySelectorAll('#nota-table tbody tr');
  let visible=0;
  rows.forEach(r=>{
    const nomor   = (r.dataset.nomor||'').toLowerCase();
    const pel     = (r.dataset.pelanggan||'').toLowerCase();
    const tgl     = (r.dataset.tanggal||'');
    const matchQ  = !q || nomor.includes(q) || pel.includes(q);
    const matchD  = !date || tgl.startsWith(date);
    r.style.display = (matchQ && matchD) ? '' : 'none';
    if(matchQ && matchD) visible++;
  });
  document.getElementById('count-label').textContent=visible;
}

async function hapus(id, nomor){
  if(!confirm('Hapus nota '+nomor+'?')) return;
  const r = await fetch('/hapus/'+id,{method:'POST'});
  const d = await r.json();
  if(d.ok){ showToast('Nota '+nomor+' dihapus','warning'); setTimeout(()=>location.reload(),800); }
}
</script>
{% endblock %}""")

# ════════════════════════════════════════════════════════════════════════════
#  DETAIL NOTA
# ════════════════════════════════════════════════════════════════════════════
DETAIL_HTML = _LAYOUT.replace('{% block content %}{% endblock %}', """{% block content %}
<div class="row g-3">
  <div class="col-lg-8">
    <!-- Nota card -->
    <div class="card mb-3" id="nota-print">
      <div class="card-body-custom">
        <!-- Kop surat -->
        <div class="text-center pb-3 mb-3" style="border-bottom:2px solid var(--border)">
          <div style="width:50px;height:50px;background:var(--accent);border-radius:12px;margin:0 auto 10px;display:flex;align-items:center;justify-content:center">
            <i class="bi bi-receipt-cutoff text-white fs-4"></i>
          </div>
          <h5 class="fw-bold mb-0" style="color:var(--text)">SMART NOTA PORTABLE</h5>
          <small style="color:var(--text-muted)">Nota Penjualan Resmi</small>
        </div>
        <!-- Info -->
        <div class="row mb-4">
          <div class="col-6">
            <table style="font-size:.85rem;width:100%">
              <tr>
                <td style="color:var(--text-muted);width:100px;padding:3px 0">No. Nota</td>
                <td><strong class="badge-nota">{{ nota.nomor }}</strong></td>
              </tr>
              <tr>
                <td style="color:var(--text-muted);padding:3px 0">Tanggal</td>
                <td>{{ nota.tanggal }}</td>
              </tr>
              <tr>
                <td style="color:var(--text-muted);padding:3px 0">Pelanggan</td>
                <td><strong>{{ nota.pelanggan or '–' }}</strong></td>
              </tr>
            </table>
          </div>
        </div>
        <!-- Items -->
        <table class="table-custom mb-0">
          <thead>
            <tr>
              <th>#</th><th>Nama Barang</th><th class="text-center">Qty</th>
              <th class="text-end">Harga</th><th class="text-end">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {% for it in items %}
            <tr>
              <td style="color:var(--text-muted)">{{ loop.index }}</td>
              <td>
                <div style="font-weight:500">{{ it.nama }}</div>
              </td>
              <td class="text-center fw-semibold">{{ it.qty }}</td>
              <td class="text-end" style="font-size:.85rem">Rp {{ '{:,.0f}'.format(it.harga).replace(',','.') }}</td>
              <td class="text-end fw-semibold">Rp {{ '{:,.0f}'.format(it.subtotal).replace(',','.') }}</td>
            </tr>
            {% endfor %}
          </tbody>
          <tfoot>
            <tr>
              <td colspan="4" class="text-end fw-bold">TOTAL</td>
              <td class="text-end fw-bold" style="color:var(--accent);font-size:1rem">
                Rp {{ '{:,.0f}'.format(nota.total).replace(',','.') }}
              </td>
            </tr>
          </tfoot>
        </table>
        <!-- Tanda tangan -->
        <div class="row mt-5 pt-2">
          <div class="col-4 text-center">
            <div style="font-size:.82rem;margin-bottom:40px;color:var(--text-muted)">Hormat Kami,</div>
            <div style="border-top:1.5px solid var(--border);padding-top:4px;font-size:.82rem">( _________________ )</div>
          </div>
          <div class="col-4"></div>
          <div class="col-4 text-center">
            <div style="font-size:.82rem;margin-bottom:40px;color:var(--text-muted)">Penerima,</div>
            <div style="border-top:1.5px solid var(--border);padding-top:4px;font-size:.82rem">( _________________ )</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Right panel -->
  <div class="col-lg-4">
    <div class="card mb-3">
      <div class="card-header-custom">
        <h6><i class="bi bi-info-circle me-2"></i>Ringkasan</h6>
      </div>
      <div class="card-body-custom">
        <div class="d-flex justify-content-between mb-2">
          <span style="font-size:.85rem;color:var(--text-muted)">Jumlah Item</span>
          <strong>{{ items|length }} item</strong>
        </div>
        <div class="d-flex justify-content-between mb-3">
          <span style="font-size:.85rem;color:var(--text-muted)">Total Qty</span>
          <strong>{{ items|sum(attribute='qty') }} pcs</strong>
        </div>
        <div class="total-row">
          <span class="label">TOTAL</span>
          <span class="amount" style="font-size:1.1rem">Rp {{ '{:,.0f}'.format(nota.total).replace(',','.') }}</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-header-custom">
        <h6><i class="bi bi-download me-2"></i>Ekspor</h6>
      </div>
      <div class="card-body-custom d-flex flex-column gap-2">
        <button class="btn btn-outline-secondary d-flex align-items-center gap-2 no-print" onclick="window.print()">
          <i class="bi bi-printer fs-5"></i>
          <div class="text-start">
            <div style="font-size:.85rem">Print Nota</div>
            <small class="text-muted fw-normal" style="font-size:.72rem">Cetak langsung dari browser</small>
          </div>
        </button>
        <a href="/pdf/{{ nota.id }}" class="btn btn-danger d-flex align-items-center gap-2 no-print">
          <i class="bi bi-file-earmark-pdf fs-5"></i>
          <div class="text-start">
            <div style="font-size:.85rem">Download PDF</div>
            <small class="fw-normal" style="font-size:.72rem;opacity:.8">Simpan file PDF ke device</small>
          </div>
        </a>
        <hr class="my-1">
        <a href="/nota/baru" class="btn btn-primary no-print">
          <i class="bi bi-plus-circle me-1"></i>Buat Nota Baru
        </a>
        <a href="/riwayat" class="btn btn-outline-secondary no-print">
          <i class="bi bi-arrow-left me-1"></i>Kembali ke Riwayat
        </a>
      </div>
    </div>
  </div>
</div>
{% endblock %}""").replace('{% block scripts %}{% endblock %}', '{% block scripts %}{% endblock %}')

# ════════════════════════════════════════════════════════════════════════════
#  PRODUK
# ════════════════════════════════════════════════════════════════════════════
PRODUK_HTML = _LAYOUT.replace('{% block content %}{% endblock %}', """{% block content %}
<div class="card">
  <div class="card-header-custom">
    <h6><i class="bi bi-box-seam me-2"></i>Daftar Produk (<span id="produk-count">{{ produk|length }}</span>)</h6>
    <span class="badge bg-primary rounded-pill">Auto-saved dari nota</span>
  </div>
  {% if produk %}
  <div class="card-body-custom border-bottom">
    <div class="input-group">
      <span class="input-group-text" style="background:#f8fafc;border-color:var(--border)">
        <i class="bi bi-search text-muted"></i>
      </span>
      <input type="text" class="form-control" id="produk-search"
             placeholder="Cari nama produk atau satuan...">
    </div>
  </div>
  <div class="card-body-custom p-0">
    <table class="table-custom">
      <thead>
        <tr>
          <th>#</th>
          <th>Nama Produk</th>
          <th class="text-end">Harga Retail</th>
          <th class="text-end">Harga Grosir</th>
          <th class="text-center">Satuan</th>
          <th class="text-center">Min Grosir</th>
          <th class="text-center">Aksi</th>
        </tr>
      </thead>
      <tbody id="produk-table-body">
        {% for p in produk %}
        <tr id="row-{{ p.id }}" data-nama="{{ p.nama|lower }}" data-satuan="{{ (p.satuan or 'pcs')|lower }}">
          <td class="row-index" style="color:var(--text-muted);font-size:.8rem">{{ loop.index }}</td>
          <td><div style="font-weight:500">{{ p.nama }}</div></td>
          <td class="text-end">Rp {{ '{:,.0f}'.format(p.harga_ret).replace(',','.') }}</td>
          <td class="text-end" style="color:var(--accent);font-weight:600">
            Rp {{ '{:,.0f}'.format(p.harga_gro).replace(',','.') }}
          </td>
          <td class="text-center">
            <span class="badge bg-light text-secondary border">{{ p.satuan or 'pcs' }}</span>
          </td>
          <td class="text-center">
            <span class="badge-pill badge-grosir">≥ {{ p.min_gro }} {{ p.satuan or 'pcs' }}</span>
          </td>
          <td class="text-center">
            <div class="d-flex gap-1 justify-content-center">
              <button class="btn btn-sm btn-outline-primary btn-icon" title="Edit"
                onclick='bukaEdit({{ p.id }}, {{ p.nama|tojson }}, {{ p.harga_ret }}, {{ p.harga_gro }}, {{ p.min_gro }}, {{ (p.satuan or "pcs")|tojson }})'>
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger btn-icon" title="Hapus"
                onclick='hapusProduk({{ p.id }}, {{ p.nama|tojson }})'>
                <i class="bi bi-trash3"></i>
              </button>
            </div>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <div class="card-body-custom">
    <div class="empty-state">
      <i class="bi bi-box"></i>
      <p>Belum ada produk. Produk tersimpan otomatis saat input nota baru.</p>
      <a href="/nota/baru" class="btn btn-primary">Buat Nota Pertama</a>
    </div>
  </div>
  {% endif %}
</div>

<!-- Modal Edit Produk -->
<div class="modal fade" id="modalEdit" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="border-radius:12px;border:none">
      <div class="modal-header border-0 pb-0">
        <h6 class="modal-title fw-bold"><i class="bi bi-pencil-square me-2 text-primary"></i>Edit Produk</h6>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body pt-2">
        <input type="hidden" id="edit-id">
        <div class="mb-3">
          <label class="form-label">Nama Produk</label>
          <input type="text" id="edit-nama" class="form-control" readonly
                 style="background:#f8fafc;color:var(--text-muted)">
          <small class="text-muted">Nama tidak bisa diubah</small>
        </div>
        <div class="row g-3">
          <div class="col-md-3 col-6">
            <label class="form-label">Harga Retail</label>
            <div class="input-group">
              <span class="input-group-text" style="font-size:.8rem">Rp</span>
              <input type="number" id="edit-ret" class="form-control" min="0">
            </div>
          </div>
          <div class="col-md-3 col-6">
            <label class="form-label">Harga Grosir</label>
            <div class="input-group">
              <span class="input-group-text" style="font-size:.8rem">Rp</span>
              <input type="number" id="edit-gro" class="form-control" min="0">
            </div>
          </div>
          <div class="col-md-3 col-6">
            <label class="form-label">Min Grosir</label>
            <input type="number" id="edit-min" class="form-control" min="1">
          </div>
          <div class="col-md-3 col-6">
            <label class="form-label">Satuan</label>
            <input type="text" id="edit-satuan" class="form-control" list="list-satuan" maxlength="20" placeholder="pcs">
          </div>
        </div>
        <datalist id="list-satuan">
          <option value="pcs">
          <option value="pack">
          <option value="lusin">
          <option value="doz">
          <option value="box">
          <option value="roll">
          <option value="set">
        </datalist>
      </div>
      <div class="modal-footer border-0 pt-0">
        <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Batal</button>
        <button class="btn btn-primary" onclick="simpanEdit()">
          <i class="bi bi-save me-1"></i>Simpan
        </button>
      </div>
    </div>
  </div>
</div>
{% endblock %}""").replace('{% block scripts %}{% endblock %}', """{% block scripts %}
<script>
const modalEdit = new bootstrap.Modal(document.getElementById('modalEdit'));

function bukaEdit(id, nama, ret, gro, min, satuan){
  document.getElementById('edit-id').value   = id;
  document.getElementById('edit-nama').value = nama;
  document.getElementById('edit-ret').value  = ret;
  document.getElementById('edit-gro').value  = gro;
  document.getElementById('edit-min').value  = min;
  document.getElementById('edit-satuan').value = (satuan || 'pcs');
  modalEdit.show();
}

async function simpanEdit(){
  const id  = document.getElementById('edit-id').value;
  const ret = parseFloat(document.getElementById('edit-ret').value)||0;
  const gro = parseFloat(document.getElementById('edit-gro').value)||0;
  const min = parseInt(document.getElementById('edit-min').value)||1;
  const satuan = (document.getElementById('edit-satuan').value || 'pcs').trim().toLowerCase();
  const r = await fetch('/api/produk/edit/'+id, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({harga_ret:ret, harga_gro:gro, min_gro:min, satuan:satuan || 'pcs'})
  });
  const d = await r.json();
  if(d.ok){ showToast('Produk berhasil diupdate','success'); modalEdit.hide(); setTimeout(()=>location.reload(),600); }
  else showToast('Gagal: '+d.msg,'danger');
}

async function hapusProduk(id, nama){
  if(!confirm('Hapus produk "'+nama+'"?')) return;
  const r = await fetch('/api/produk/hapus/'+id, {method:'POST'});
  const d = await r.json();
  if(d.ok){
    showToast(nama+' dihapus','warning');
    const row = document.getElementById('row-'+id);
    if(row) row.remove();
    filterProdukRows();
  }
  else showToast('Gagal: '+d.msg,'danger');
}

function filterProdukRows(){
  const inp = document.getElementById('produk-search');
  const body = document.getElementById('produk-table-body');
  if(!inp || !body) return;
  const q = (inp.value || '').trim().toLowerCase();
  const rows = [...body.querySelectorAll('tr')];
  let visible = 0;
  rows.forEach((row)=>{
    const nama = row.dataset.nama || '';
    const satuan = row.dataset.satuan || '';
    const match = !q || nama.includes(q) || satuan.includes(q);
    row.style.display = match ? '' : 'none';
    if(match){
      visible++;
      const idxCell = row.querySelector('.row-index');
      if(idxCell) idxCell.textContent = visible;
    }
  });
  const count = document.getElementById('produk-count');
  if(count) count.textContent = visible;
}

const produkSearch = document.getElementById('produk-search');
if(produkSearch){
  produkSearch.addEventListener('input', filterProdukRows);
  filterProdukRows();
}
</script>
{% endblock %}""")

# ════════════════════════════════════════════════════════════════════════════
#  FLASK SETUP & DB
# ════════════════════════════════════════════════════════════════════════════
app = Flask(__name__)
DB_PATH = get_db_path()

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS produk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL UNIQUE,
        harga_ret REAL NOT NULL DEFAULT 0,
        harga_gro REAL NOT NULL DEFAULT 0,
        min_gro INTEGER NOT NULL DEFAULT 1,
        satuan TEXT NOT NULL DEFAULT 'pcs'
    )''')
    cols = [r[1] for r in cur.execute("PRAGMA table_info(produk)").fetchall()]
    if 'satuan' not in cols:
        cur.execute("ALTER TABLE produk ADD COLUMN satuan TEXT NOT NULL DEFAULT 'pcs'")
    cur.execute("UPDATE produk SET satuan='pcs' WHERE satuan IS NULL OR TRIM(satuan)='' ")
    cur.execute('''CREATE TABLE IF NOT EXISTS nota (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomor TEXT NOT NULL,
        pelanggan TEXT,
        tanggal TEXT NOT NULL,
        total REAL NOT NULL DEFAULT 0
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS item_nota (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nota_id INTEGER NOT NULL,
        nama TEXT NOT NULL,
        qty INTEGER NOT NULL,
        harga REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (nota_id) REFERENCES nota(id)
    )''')
    con.commit()
    con.close()

init_db()

def get_con():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def next_nomor():
    today = datetime.now().strftime('%Y%m%d')
    con = get_con()
    row = con.execute("SELECT COUNT(*) as c FROM nota WHERE nomor LIKE ?",
                      (f'NTA-{today}%',)).fetchone()
    con.close()
    return f"NTA-{today}-{row['c']+1:03d}"

def render(template, **kw):
    kw.setdefault('ip', get_ip())
    kw.setdefault('breadcrumb', None)
    kw.setdefault('active', '')
    kw.setdefault('page_title', 'Smart Nota')
    return render_template_string(template, **kw)

# ════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════════════════════
@app.route('/')
def index():
    con = get_con()
    total_nota   = con.execute("SELECT COUNT(*) as c FROM nota").fetchone()['c']
    total_produk = con.execute("SELECT COUNT(*) as c FROM produk").fetchone()['c']
    omzet        = con.execute("SELECT COALESCE(SUM(total),0) as s FROM nota").fetchone()['s']
    today        = datetime.now().strftime('%Y-%m-%d')
    nota_hari    = con.execute("SELECT COUNT(*) as c FROM nota WHERE tanggal LIKE ?",
                               (today+'%',)).fetchone()['c']
    recent       = con.execute("SELECT * FROM nota ORDER BY id DESC LIMIT 6").fetchall()
    con.close()
    omzet_fmt = f"Rp {omzet:,.0f}".replace(',','.')[:12]
    stats = dict(total_nota=total_nota, total_produk=total_produk,
                 omzet_fmt=omzet_fmt, nota_hari=nota_hari)
    return render(INDEX_HTML, page_title='Dashboard', active='home',
                  stats=stats, recent_notas=recent)

@app.route('/nota/baru')
def nota_baru():
    return render(NOTA_HTML, page_title='Buat Nota Baru',
                  breadcrumb='Buat Nota', active='nota')

@app.route('/riwayat')
def riwayat():
    con = get_con()
    notas = con.execute("""
        SELECT n.*, COUNT(i.id) as item_count
        FROM nota n LEFT JOIN item_nota i ON i.nota_id=n.id
        GROUP BY n.id ORDER BY n.id DESC
    """).fetchall()
    con.close()
    return render(RIWAYAT_HTML, page_title='Riwayat Nota',
                  breadcrumb='Riwayat', active='riwayat', notas=notas)

@app.route('/produk')
def produk_page():
    con = get_con()
    produk = con.execute("SELECT * FROM produk ORDER BY nama").fetchall()
    con.close()
    return render(PRODUK_HTML, page_title='Daftar Produk',
                  breadcrumb='Produk', active='produk', produk=produk)

@app.route('/detail/<int:nota_id>')
def detail(nota_id):
    con = get_con()
    nota  = con.execute("SELECT * FROM nota WHERE id=?", (nota_id,)).fetchone()
    items = con.execute("SELECT * FROM item_nota WHERE nota_id=?", (nota_id,)).fetchall()
    con.close()
    if not nota: return "Nota tidak ditemukan", 404
    return render(DETAIL_HTML, page_title=f'Detail {nota["nomor"]}',
                  breadcrumb='Detail Nota', active='riwayat',
                  nota=nota, items=items)

@app.route('/api/produk/<nama>')
def api_produk(nama):
    con = get_con()
    row = con.execute("SELECT * FROM produk WHERE LOWER(nama)=LOWER(?)", (nama,)).fetchone()
    con.close()
    if row:
        return jsonify({'found':True,'harga_ret':row['harga_ret'],
              'harga_gro':row['harga_gro'],'min_gro':row['min_gro'],
              'satuan': row['satuan'] or 'pcs'})
    return jsonify({'found':False})

@app.route('/api/produk/list')
def api_produk_list():
    con = get_con()
    rows = con.execute("SELECT nama FROM produk ORDER BY nama").fetchall()
    con.close()
    return jsonify([r['nama'] for r in rows])

@app.route('/api/produk/batch', methods=['POST'])
def api_produk_batch():
    data = request.get_json() or []
    con  = get_con(); cur = con.cursor()
    for p in data:
        satuan = (p.get('satuan') or 'pcs').strip().lower()[:20]
        cur.execute('''INSERT INTO produk (nama,harga_ret,harga_gro,min_gro,satuan) VALUES (?,?,?,?,?)
            ON CONFLICT(nama) DO UPDATE SET
            harga_ret=excluded.harga_ret,harga_gro=excluded.harga_gro,min_gro=excluded.min_gro,satuan=excluded.satuan''',
            (p['nama'], p['harga_ret'], p['harga_gro'], p['min_gro'], satuan or 'pcs'))
    con.commit(); con.close()
    return jsonify({'ok': True})

@app.route('/api/produk/edit/<int:produk_id>', methods=['POST'])
def api_produk_edit(produk_id):
    data = request.get_json()
    satuan = (data.get('satuan') or 'pcs').strip().lower()[:20]
    con  = get_con()
    con.execute("UPDATE produk SET harga_ret=?,harga_gro=?,min_gro=?,satuan=? WHERE id=?",
                (data['harga_ret'], data['harga_gro'], data['min_gro'], satuan or 'pcs', produk_id))
    con.commit(); con.close()
    return jsonify({'ok': True})

@app.route('/api/produk/hapus/<int:produk_id>', methods=['POST'])
def api_produk_hapus(produk_id):
    con = get_con()
    con.execute("DELETE FROM produk WHERE id=?", (produk_id,))
    con.commit(); con.close()
    return jsonify({'ok': True})

@app.route('/api/simpan', methods=['POST'])
def api_simpan():
    data  = request.get_json()
    items = data.get('items', [])
    if not items: return jsonify({'ok':False,'msg':'Item kosong'})
    pelanggan = data.get('pelanggan','').strip()
    tanggal   = datetime.now().strftime('%Y-%m-%d %H:%M')
    nomor     = next_nomor()
    total     = sum(i['subtotal'] for i in items)
    con = get_con(); cur = con.cursor()
    for i in items:
      if i.get('is_new'):
        satuan = (i.get('satuan') or 'pcs').strip().lower()[:20]
        cur.execute('''INSERT INTO produk (nama,harga_ret,harga_gro,min_gro,satuan) VALUES (?,?,?,?,?)
          ON CONFLICT(nama) DO UPDATE SET
          harga_ret=excluded.harga_ret,harga_gro=excluded.harga_gro,min_gro=excluded.min_gro,satuan=excluded.satuan''',
          (i['nama'], i['harga_ret'], i['harga_gro'], i['min_gro'], satuan or 'pcs'))
    cur.execute("INSERT INTO nota (nomor,pelanggan,tanggal,total) VALUES (?,?,?,?)",
                (nomor,pelanggan,tanggal,total))
    nota_id = cur.lastrowid
    for i in items:
        cur.execute("INSERT INTO item_nota (nota_id,nama,qty,harga,subtotal) VALUES (?,?,?,?,?)",
                    (nota_id,i['nama'],i['qty'],i['harga'],i['subtotal']))
    con.commit(); con.close()
    return jsonify({'ok':True,'nota_id':nota_id,'nomor':nomor})

@app.route('/pdf/<int:nota_id>')
def pdf_route(nota_id):
    con = get_con()
    nota  = con.execute("SELECT * FROM nota WHERE id=?", (nota_id,)).fetchone()
    items = con.execute("SELECT * FROM item_nota WHERE nota_id=?", (nota_id,)).fetchall()
    con.close()
    if not nota: return "Nota tidak ditemukan", 404
    p = FPDF()
    p.add_page()
    p.set_margins(15, 15, 15)
    # Kop
    p.set_font('Arial','B',18)
    p.cell(0,9,'SMART NOTA PORTABLE',ln=True,align='C')
    p.set_font('Arial','',10)
    p.cell(0,5,'Nota Penjualan Resmi',ln=True,align='C')
    p.ln(2)
    p.set_draw_color(79,70,229)
    p.set_line_width(0.8)
    p.line(15,p.get_y(),195,p.get_y())
    p.ln(5)
    # Info
    p.set_font('Arial','',10)
    p.cell(40,6,'No. Nota',border=0); p.cell(5,6,':',border=0); p.cell(0,6,nota['nomor'],ln=True)
    p.cell(40,6,'Tanggal',border=0); p.cell(5,6,':',border=0); p.cell(0,6,nota['tanggal'],ln=True)
    p.cell(40,6,'Pelanggan',border=0); p.cell(5,6,':',border=0); p.cell(0,6,nota['pelanggan'] or '-',ln=True)
    p.ln(5)
    # Header tabel
    p.set_font('Arial','B',10)
    p.set_fill_color(79,70,229); p.set_text_color(255,255,255)
    p.cell(8,8,'No',border=1,align='C',fill=True)
    p.cell(75,8,'Nama Barang',border=1,align='C',fill=True)
    p.cell(20,8,'Qty',border=1,align='C',fill=True)
    p.cell(35,8,'Harga',border=1,align='C',fill=True)
    p.cell(42,8,'Subtotal',border=1,align='C',fill=True,ln=True)
    # Rows
    p.set_font('Arial','',10); p.set_text_color(0,0,0); p.set_fill_color(238,242,255)
    for idx,it in enumerate(items,1):
        fill=(idx%2==0)
        p.cell(8,7,str(idx),border=1,align='C',fill=fill)
        p.cell(75,7,it['nama'],border=1,fill=fill)
        p.cell(20,7,str(it['qty']),border=1,align='C',fill=fill)
        p.cell(35,7,f"Rp {it['harga']:,.0f}",border=1,align='R',fill=fill)
        p.cell(42,7,f"Rp {it['subtotal']:,.0f}",border=1,align='R',fill=fill,ln=True)
    # Total
    p.set_font('Arial','B',11)
    p.set_fill_color(79,70,229); p.set_text_color(255,255,255)
    p.cell(138,9,'TOTAL',border=1,align='R',fill=True)
    p.cell(42,9,f"Rp {nota['total']:,.0f}",border=1,align='R',fill=True,ln=True)
    p.set_text_color(0,0,0)
    p.ln(15)
    # TTD
    p.set_font('Arial','',10)
    xl,xr,yn=15,120,p.get_y()
    p.set_xy(xl,yn); p.cell(60,6,'Hormat Kami,',align='C')
    p.set_xy(xr,yn); p.cell(60,6,'Penerima,',align='C')
    p.ln(22); yn=p.get_y()
    p.set_xy(xl,yn); p.cell(60,6,'( _________________ )',align='C')
    p.set_xy(xr,yn); p.cell(60,6,'( _________________ )',align='C')
    tmp = tempfile.NamedTemporaryFile(delete=False,suffix='.pdf')
    p.output(tmp.name); tmp.close()
    return send_file(tmp.name, as_attachment=True,
                     download_name=f"nota-{nota['nomor']}.pdf",
                     mimetype='application/pdf')

@app.route('/hapus/<int:nota_id>', methods=['POST'])
def hapus(nota_id):
    con = get_con()
    con.execute("DELETE FROM item_nota WHERE nota_id=?", (nota_id,))
    con.execute("DELETE FROM nota WHERE id=?", (nota_id,))
    con.commit(); con.close()
    return jsonify({'ok':True})

# ════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT – System Tray + Auto Browser
# ════════════════════════════════════════════════════════════════════════════
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def buat_ikon():
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # background bulat indigo
    d.ellipse([0, 0, 63, 63], fill=(79, 70, 229))
    # gambar nota sederhana (persegi putih + garis)
    d.rectangle([18, 14, 46, 50], fill='white')
    d.rectangle([22, 22, 42, 24], fill=(79, 70, 229))
    d.rectangle([22, 28, 42, 30], fill=(79, 70, 229))
    d.rectangle([22, 34, 36, 36], fill=(79, 70, 229))
    return img

if __name__ == '__main__':
    import threading, webbrowser, time
    ip  = get_ip()
    url = 'http://127.0.0.1:5000'

    threading.Thread(target=run_flask, daemon=True).start()

    def _browser():
        time.sleep(1.5); webbrowser.open(url)
    threading.Thread(target=_browser, daemon=True).start()

    try:
        import pystray

        def on_buka(icon, item): webbrowser.open(url)
        def on_stop(icon, item): icon.stop(); os._exit(0)

        menu = pystray.Menu(
            pystray.MenuItem(f'🌐  Buka Smart Nota  ({ip}:5000)', on_buka, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('⏹  Stop Server', on_stop),
        )
        ikon = pystray.Icon('SmartNota', buat_ikon(), f'Smart Nota – {ip}:5000', menu)
        ikon.run()

    except Exception as e:
        print(f"\n  Smart Nota aktif: {url}  |  Jaringan: http://{ip}:5000")
        print("  CTRL+C untuk stop\n")
        try: threading.Event().wait()
        except KeyboardInterrupt: pass
