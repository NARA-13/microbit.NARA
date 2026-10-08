#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 3 patch (verified anchors): right sidebar nav, mobile drawer, account+avatar, UI polish."""
import io

P = "/home/user/iconnect.html"
h = io.open(P, encoding="utf-8").read()
orig_len = len(h)

def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, f"count {c} != {n} :: {a[:80]!r}"
    h = h.replace(a, b, 1)

def ins(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, f"count {c} != {n} :: {a[:80]!r}"
    h = h.replace(a, b + a, 1)

def splice_range(i, j, new):
    """Replace lines[i:j] (line numbers, human 1-based, inclusive) with new text."""
    global h
    lines = h.split("\n")
    assert 1 <= i <= j <= len(lines), (i, j, len(lines))
    lines[i-1:j] = new.split("\n")
    h = "\n".join(lines)

# ================================================================
# 1. TOKENS
# ================================================================
rep("""  --header-h:66px;
}""", """  --header-h:68px;
  --sb-w:236px;
  --sb-w-c:206px;
}""")

# ================================================================
# 2. HEADER — hamburger button CSS (after .icon-btn)
# ================================================================
rep(""".icon-btn:active{transform:translateY(0) scale(.95)}""", """.icon-btn:active{transform:translateY(0) scale(.95)}
.head-more{
  display:none;width:36px;height:36px;border-radius:10px;
  align-items:center;justify-content:center;flex-shrink:0;
  background:var(--surface-2);border:1px solid var(--line);
  color:var(--txt-2);cursor:pointer;transition:.2s var(--ease);
}
.head-more:hover{color:var(--txt);border-color:var(--line-strong)}
.head-more:active{transform:scale(.94)}
.head-more svg{width:17px;height:17px}
""")

# ================================================================
# 3. TABS CSS  ->  SHELL + RIGHT SIDEBAR CSS (line-based splice)
# ================================================================
lines = h.split("\n")
i = next(k for k, l in enumerate(lines) if l.startswith(".tabbar{")) + 1
j = next(k for k, l in enumerate(lines) if l.startswith(".tab .badge{")) + 1
k2 = next(k for k in range(j, len(lines)) if lines[k] == "}")
SHELL_CSS = """/* ============================================================
   APP SHELL — main + right sidebar
   ============================================================ */
.shell{
  display:grid;grid-template-columns:minmax(0,1fr) var(--sb-w);gap:22px;
  align-items:start;width:100%;max-width:1400px;margin:0 auto;
  padding:26px 22px 96px;
}
main{grid-column:1;grid-row:1;min-width:0;padding:0;width:100%}
.side{
  grid-column:2;grid-row:1;position:sticky;top:calc(var(--header-h) + 22px);
  display:flex;flex-direction:column;gap:12px;min-width:0;
}
.nav{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);
  box-shadow:var(--shadow);padding:10px;
}
.nav-ttl{
  font-size:10px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
  color:var(--txt-3);padding:6px 12px 10px;
}
.tab{
  position:relative;display:flex;align-items:center;gap:10px;width:100%;
  height:40px;padding:0 12px;border-radius:11px;border:none;background:transparent;
  font-size:13px;font-weight:650;color:var(--txt-2);cursor:pointer;white-space:nowrap;
  transition:.18s var(--ease);text-align:left;
}
.tab svg{width:16px;height:16px;flex-shrink:0;opacity:.8;transition:.18s var(--ease)}
.tab:hover{color:var(--txt);background:var(--surface-2)}
.tab.active{
  color:#fff;background:linear-gradient(135deg,var(--brand),var(--brand-600));
  box-shadow:0 6px 18px rgba(13,128,242,.30);font-weight:750;
}
html[data-theme="light"] .tab.active{box-shadow:0 5px 16px rgba(13,128,242,.24)}
.tab.active svg{opacity:1}
.tab .badge{
  margin-left:auto;min-width:17px;height:17px;padding:0 5px;border-radius:99px;
  background:var(--surface);color:var(--brand);font-size:10px;font-weight:800;
  display:grid;place-items:center;
}
.tab.active .badge{background:rgba(255,255,255,.22);color:#fff}
.side-me{
  display:flex;align-items:center;gap:11px;padding:10px;border-radius:var(--radius-lg);
  background:var(--surface);border:1px solid var(--line);box-shadow:var(--shadow);
  text-align:left;cursor:pointer;transition:.18s var(--ease);color:inherit;width:100%;
}
.side-me:hover{border-color:var(--line-strong);transform:translateY(-1px)}
.side-me .av{
  width:38px;height:38px;border-radius:12px;background:var(--surface-2);
  border:1px solid var(--line);display:grid;place-items:center;overflow:hidden;flex-shrink:0;
  font-size:13px;font-weight:800;color:var(--brand);
}
.side-me .av img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.side-me .av{position:relative}
.side-me .me-txt{min-width:0;display:flex;flex-direction:column;gap:2px}
.side-me .nm{font-size:12.5px;font-weight:750;color:var(--txt);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.side-me .rl{display:flex;align-items:center;gap:5px;font-size:10.5px;font-weight:600;color:var(--txt-3)}
.side-me .rl i{width:5px;height:5px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 2px var(--ok-soft);flex-shrink:0}
.side-me .arr{margin-left:auto;color:var(--txt-3);flex-shrink:0;display:grid;place-items:center}
.side-me .arr svg{width:14px;height:14px}
.side-x{
  display:none;width:32px;height:32px;border-radius:10px;
  align-items:center;justify-content:center;
  background:var(--surface-2);border:1px solid var(--line);
  color:var(--txt-2);cursor:pointer;
}
.scrim{
  position:fixed;inset:0;z-index:85;background:rgba(5,8,14,.55);
  backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px);
  opacity:0;pointer-events:none;transition:opacity .3s var(--ease);
}
html.menu-open .scrim{opacity:1;pointer-events:auto}
html.menu-open{overflow:hidden}"""
splice_range(i, k2, SHELL_CSS)

# ================================================================
# 4. MAIN OLD RULE removal
# ================================================================
rep("main{flex:1;padding:26px 22px 90px;max-width:1180px;width:100%;margin:0 auto}",
    "/* main layout handled by .shell above */")

# ================================================================
# 5. MARKUP — open shell + aside around tabbar
# ================================================================
rep("""<!-- ==================== TABS ==================== -->
<nav class="tabbar" id="tabbar">
""", """<!-- ==================== NAVIGATION · right sidebar ==================== -->
<div class="shell">
  <div class="scrim" id="scrim" onclick="closeSide()"></div>
  <aside class="side" id="sideA">
    <button class="side-x" id="sideX" type="button" aria-label="Close">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" width="15" height="15"><path d="M18 6 6 18M6 6l12 12"/></svg>
    </button>
    <nav class="nav" id="tabbar" aria-label="Navigasi">
      <div class="nav-ttl" data-i18n="navTitle">MENU</div>
""")

rep("""</nav>

<main>""", """    </nav>
    <button class="side-me" id="btnMe" type="button">
      <span class="av" id="meAv"><span id="mePh">NK</span></span>
      <span class="me-txt">
        <span class="nm" id="meName">Sobat ICONNECT</span>
        <span class="rl"><i></i><span id="meRole" data-i18n="icnUser">Pengguna ICONNECT</span></span>
      </span>
      <span class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="m9 18 6-6-6-6"/></svg></span>
    </button>
  </aside>

<main>""")

# close .shell then .app
rep("""</main>
</div>

<div class="toasts" id="toasts"></div>""", """</main>
  </div>
</div>

<div class="toasts" id="toasts"></div>""")

# ================================================================
# 6. MARKUP — hamburger in header
# ================================================================
rep("""      <span class="btn-connect-label" data-i18n="btn_connect">Hubungkan</span>
    </button>
  </div>
</header>""", """      <span class="btn-connect-label" data-i18n="btn_connect">Hubungkan</span>
    </button>
    <button class="head-more" id="btnMore" type="button" aria-label="Menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
  </div>
</header>""")

# ================================================================
# 7. DEV AVATAR — id + CSS
# ================================================================
rep("""    <div class="dev-av">NK</div>""", """    <div class="dev-av" id="devAv"><span>NK</span></div>""")
rep(""".dev-av{
  position:relative;width:78px;height:78px;margin:0 auto 18px;border-radius:24px;
  background:linear-gradient(140deg,var(--brand),var(--violet));
  display:grid;place-items:center;color:#fff;font-size:27px;font-weight:800;letter-spacing:.02em;
  box-shadow:0 12px 34px rgba(13,128,242,.35);
}""", """.dev-av{
  position:relative;width:78px;height:78px;margin:0 auto 18px;border-radius:24px;overflow:hidden;
  background:linear-gradient(140deg,var(--brand),var(--violet));
  display:grid;place-items:center;color:#fff;font-size:27px;font-weight:800;letter-spacing:.02em;
  box-shadow:0 12px 34px rgba(13,128,242,.35);
}
.dev-av span{position:relative;color:#fff;font-weight:800}
.dev-av img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}""")

# ================================================================
# 8. ACCOUNT SECTION — CSS (before Developer CSS)
# ================================================================
rep("""/* ---------- Developer ---------- */""", """/* ---------- Account / Profile ---------- */
.sec-h{display:flex;align-items:center;gap:11px;margin:4px 0 12px}
.sec-h svg{width:19px;height:19px;color:var(--brand);flex-shrink:0}
.sec-h b{font-size:16px;font-weight:820;letter-spacing:-.02em;display:block}
.sec-h span{display:block;font-size:11.5px;font-weight:550;color:var(--txt-3);margin-top:2px}
.acct{display:flex;gap:22px;align-items:flex-start}
.acct-side{display:flex;flex-direction:column;align-items:center;gap:13px;flex-shrink:0;width:150px}
.acct-av{
  position:relative;width:112px;height:112px;border-radius:32px;overflow:hidden;
  background:linear-gradient(140deg,var(--brand),var(--violet));
  display:grid;place-items:center;
  box-shadow:0 14px 38px rgba(13,128,242,.32);
  border:3px solid var(--surface);outline:1px solid var(--line);
}
.acct-av span{position:relative;color:#fff;font-size:38px;font-weight:800;letter-spacing:.02em;user-select:none}
.acct-av img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.acct-btns{display:flex;flex-direction:column;gap:8px;width:100%}
.acct-btns .btn{width:100%}
.acct-hint{font-size:11px;color:var(--txt-3);line-height:1.55;text-align:center}
.acct-fields{flex:1;min-width:0;display:flex;flex-direction:column;gap:13px;max-width:400px}
.fld{display:flex;flex-direction:column;gap:6px}
.fld-lb{font-size:12px;font-weight:750;color:var(--txt-2);letter-spacing:.03em}
.fld input{
  height:42px;border-radius:11px;border:1px solid var(--line);background:var(--surface-2);
  padding:0 13px;font-size:13.5px;font-weight:600;color:var(--txt);outline:0;width:100%;
  transition:.2s var(--ease);
}
.fld input:focus{border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-soft)}
.fld input::placeholder{color:var(--txt-3);font-weight:500}
.ok-line{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:700;color:var(--ok)}
.ok-line[hidden]{display:none}
.ok-line svg{flex-shrink:0}
@media (max-width:560px){
  .acct{flex-direction:column;align-items:center}
  .acct-fields{width:100%;max-width:none}
}

/* ---------- Developer ---------- */""")

# ================================================================
# 9. ACCOUNT SECTION — HTML in Settings (before preferences card)
# ================================================================
rep("""  </div>
  <div class="card" style="max-width:620px">""", """  </div>

  <div class="sec-h">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4.5 21a7.5 7.5 0 0 1 15 0"/></svg>
    <div><b data-i18n="secAccount"></b><span data-i18n="secAccountSub"></span></div>
  </div>
  <div class="card" style="max-width:620px">
    <div class="acct">
      <div class="acct-side">
        <div class="acct-av" id="acctAv"><span id="acctPh">NK</span></div>
        <div class="acct-btns">
          <button class="btn btn-primary btn-sm" id="btnPickAv" type="button">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>
            <span data-i18n="acctUp"></span>
          </button>
          <button class="btn btn-ghost btn-sm" id="btnResetAv" type="button">
            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h18"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M19 7 18 19a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 7"/></svg>
            <span data-i18n="acctReset"></span>
          </button>
        </div>
        <p class="acct-hint" data-i18n="acctHint"></p>
      </div>
      <div class="acct-fields">
        <label class="fld">
          <span class="fld-lb" data-i18n="acctName"></span>
          <input id="acctName" type="text" maxlength="24" data-i18n-ph="acctNamePh" autocomplete="off" spellcheck="false">
        </label>
        <label class="fld">
          <span class="fld-lb" data-i18n="acctTag"></span>
          <input id="acctTag" type="text" maxlength="30" data-i18n-ph="acctTagPh" autocomplete="off" spellcheck="false">
        </label>
        <p class="ok-line" id="acctSaved" hidden>
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
          <span data-i18n="acctSaved"></span>
        </p>
      </div>
    </div>
    <input type="file" id="avFile" accept="image/*" hidden>
  </div>

  <div class="card" style="max-width:620px">""")

# ================================================================
# 10. I18N KEYS ×5
# ================================================================
ID_KEYS = """    navTitle:"MENU",
    secAccount:"Akun Saya",
    secAccountSub:"Kustomisasi profil yang tampil di aplikasi",
    icnUser:"Pengguna ICONNECT",
    acctName:"Nama Tampilan",
    acctTag:"Status / Tagline",
    acctHint:"Foto disimpan lokal di perangkat ini. Format JPG/PNG, tanpa diunggah ke jaringan.",
    acctUp:"Unggah Foto",
    acctReset:"Hapus Foto",
    acctSaved:"Profil tersimpan",
    acctNamePh:"Contoh: Nararya",
    acctTagPh:"Contoh: Pembuat ICONNECT",
    acctBig:"Foto terlalu besar (maks 1.5 MB)",
"""
EN_KEYS = """    navTitle:"MENU",
    secAccount:"My Account",
    secAccountSub:"Customize the profile shown in the app",
    icnUser:"ICONNECT User",
    acctName:"Display Name",
    acctTag:"Status / Tagline",
    acctHint:"Photo is stored locally on this device. JPG/PNG, never uploaded.",
    acctUp:"Upload Photo",
    acctReset:"Remove Photo",
    acctSaved:"Profile saved",
    acctNamePh:"e.g. Nararya",
    acctTagPh:"e.g. ICONNECT Maker",
    acctBig:"Photo too large (max 1.5 MB)",
"""
JA_KEYS = """  navTitle:"メニュー",
  secAccount:"マイアカウント",
  secAccountSub:"アプリに表示されるプロフィールをカスタマイズ",
  icnUser:"ICONNECT ユーザー",
  acctName:"表示名",
  acctTag:"ステータス / タグライン",
  acctHint:"写真はこの端末にローカル保存されます（JPG/PNG、アップロードなし）。",
  acctUp:"写真をアップロード",
  acctReset:"写真を削除",
  acctSaved:"プロフィールを保存しました",
  acctNamePh:"例：ナラリヤ",
  acctTagPh:"例：ICONNECT 製作者",
  acctBig:"写真が大きすぎます（最大 1.5MB）",
"""
ZH_KEYS = """  navTitle:"菜单",
  secAccount:"我的账户",
  secAccountSub:"自定义应用中显示的个人资料",
  icnUser:"ICONNECT 用户",
  acctName:"显示名称",
  acctTag:"状态 / 简介",
  acctHint:"照片仅保存在此设备本地（JPG/PNG，不会上传）。",
  acctUp:"上传照片",
  acctReset:"删除照片",
  acctSaved:"个人资料已保存",
  acctNamePh:"例如：Nararya",
  acctTagPh:"例如：ICONNECT 制作者",
  acctBig:"照片过大（最大 1.5MB）",
"""
ES_KEYS = """  navTitle:"MENÚ",
  secAccount:"Mi Cuenta",
  secAccountSub:"Personaliza el perfil que se muestra en la app",
  icnUser:"Usuario ICONNECT",
  acctName:"Nombre visible",
  acctTag:"Estado / Lema",
  acctHint:"La foto se guarda localmente en este dispositivo (JPG/PNG, sin subir a la red).",
  acctUp:"Subir Foto",
  acctReset:"Quitar Foto",
  acctSaved:"Perfil guardado",
  acctNamePh:"p. ej. Nararya",
  acctTagPh:"p. ej. Creador de ICONNECT",
  acctBig:"Foto demasiado grande (máx. 1,5 MB)",
"""
rep("""  id:{
    disconnected:""", """  id:{
""" + ID_KEYS + """    disconnected:""")
rep("""  en:{
    disconnected:""", """  en:{
""" + EN_KEYS + """    disconnected:""")
rep("""I18N.ja = {
  disconnected:""", """I18N.ja = {
""" + JA_KEYS + """  disconnected:""")
rep("""I18N.zh = {
  disconnected:""", """I18N.zh = {
""" + ZH_KEYS + """  disconnected:""")
rep("""I18N.es = {
  disconnected:""", """I18N.es = {
""" + ES_KEYS + """  disconnected:""")

# ================================================================
# 11. JS — prefs defaults
# ================================================================
rep("""const prefs = Object.assign({theme:"dark",lang:"id",demo:false,auto:true,sfx:"soft"},""",
    """const prefs = Object.assign({theme:"dark",lang:"id",demo:false,auto:true,sfx:"soft",name:"",tag:"",avatar:""},""")

# ================================================================
# 12. JS — setLang calls syncProfile
# ================================================================
rep("""  if (window.renderCode) renderCode();
}""", """  if (window.renderCode) renderCode();
  syncProfile();
}""")

# ================================================================
# 13. JS — tabs block + sidebar/profile logic
# ================================================================
rep("""/* ---------- tabs ---------- */
let unread = 0;
$$(".tab").forEach(t => t.onclick = () => {
  $$(".tab").forEach(x => x.classList.remove("active"));
  $$(".panel").forEach(x => x.classList.remove("active"));
  t.classList.add("active");
  $("#p-" + t.dataset.tab).classList.add("active");
  window.scrollTo({top:0, behavior:"smooth"});
  if (t.dataset.tab === "log"){ unread = 0; $("#logBadge").classList.add("hide"); }
  sfx("tab");
});""", """/* ---------- tabs ---------- */
let unread = 0;
$$(".tab").forEach(t => t.onclick = () => {
  $$(".tab").forEach(x => x.classList.remove("active"));
  $$(".panel").forEach(x => x.classList.remove("active"));
  t.classList.add("active");
  $("#p-" + t.dataset.tab).classList.add("active");
  window.scrollTo({top:0, behavior:"smooth"});
  if (t.dataset.tab === "log"){ unread = 0; $("#logBadge").classList.add("hide"); }
  closeSide();
  sfx("tab");
});

/* ---------- right sidebar / drawer ---------- */
function openSide(){ document.documentElement.classList.add("menu-open"); }
function closeSide(){ document.documentElement.classList.remove("menu-open"); }
function setTab(name){
  const t = $('.tab[data-tab="' + name + '"]');
  if (t) t.click();
}
$("#btnMore").onclick = () => {
  document.documentElement.classList.contains("menu-open") ? closeSide() : openSide();
  sfx("tick");
};
document.getElementById("sideX").onclick = closeSide;
$("#btnMe").onclick = () => setTab("set");

/* ---------- profile / account ---------- */
function initialsOf(name){
  const n = (name || "").trim();
  if (!n) return "NK";
  const p = n.split(/\\s+/);
  if (p.length > 1) return (p[0][0] + p[p.length - 1][0]).toUpperCase();
  return n.slice(0, 2).toUpperCase();
}
function applyAv(){
  const url = prefs.avatar || "";
  document.querySelectorAll("#acctAv,#meAv,#devAv").forEach(box => {
    const old = box.querySelector("img");
    if (old) old.remove();
    if (url){
      const im = document.createElement("img");
      im.src = url;
      box.appendChild(im);
    }
  });
}
function updateProfileUI(){
  const name = prefs.name || "";
  const ph = initialsOf(name);
  $("#meName").textContent = name || T("homeName");
  $("#meRole").textContent = prefs.tag || T("icnUser");
  $("#mePh").textContent = ph;
  $("#acctPh").textContent = ph;
  const dv = $("#devAv");
  dv.textContent = "";
  const sp = document.createElement("span");
  sp.textContent = ph;
  dv.appendChild(sp);
  applyAv();
}
function syncProfile(){
  const ne = $("#acctName"), tg = $("#acctTag");
  if (ne) ne.value = prefs.name || "";
  if (tg) tg.value = prefs.tag || "";
  updateProfileUI();
}
(function(){
  const f = $("#avFile"), pick = $("#btnPickAv"), reset = $("#btnResetAv");
  const nameEl = $("#acctName"), tagEl = $("#acctTag"), saved = $("#acctSaved");
  if (!f || !nameEl) return;
  let t;
  const flashSaved = () => {
    if (!saved) return;
    saved.hidden = false;
    clearTimeout(t);
    t = setTimeout(() => { saved.hidden = true; }, 2600);
  };
  pick.onclick = () => { f.click(); sfx("tick"); };
  reset.onclick = () => {
    prefs.avatar = ""; savePrefs(); updateProfileUI(); flashSaved(); sfx("warn");
  };
  f.onchange = () => {
    const file = f.files && f.files[0];
    if (!file) return;
    if (file.size > 1.5 * 1024 * 1024){
      toast(T("acctBig"), "err"); f.value = ""; return;
    }
    const rd = new FileReader();
    rd.onload = e => {
      prefs.avatar = String(e.target.result);
      savePrefs(); updateProfileUI(); flashSaved(); sfx("success");
      toast(T("acctSaved"), "ok");
    };
    rd.onerror = () => toast(T("acctBig"), "err");
    rd.readAsDataURL(file);
    f.value = "";
  };
  nameEl.oninput = () => { prefs.name = nameEl.value.trim().slice(0, 24); savePrefs(); updateProfileUI(); flashSaved(); };
  tagEl.oninput = () => { prefs.tag = tagEl.value.trim().slice(0, 30); savePrefs(); updateProfileUI(); flashSaved(); };
})();""")

# ================================================================
# 14. RESPONSIVE — drawer block before 980px media
# ================================================================
rep("""@media (max-width:980px){""", """@media (max-width:1080px){
  .shell{grid-template-columns:minmax(0,1fr) var(--sb-w-c);gap:16px}
}
@media (max-width:1024px){
  .shell{grid-template-columns:minmax(0,1fr);padding:22px 16px 96px}
  .side{
    grid-column:1;grid-row:2;position:fixed;top:0;right:0;bottom:0;z-index:90;
    width:min(304px,86vw);padding:18px;overflow-y:auto;
    background:var(--surface);border-left:1px solid var(--line);
    box-shadow:-18px 0 54px rgba(0,0,0,.35);
    transform:translateX(calc(100% + 30px));transition:transform .34s var(--ease);
  }
  html[data-theme="light"] .side{box-shadow:-18px 0 54px rgba(16,24,40,.18)}
  html.menu-open .side{transform:translateX(0)}
  .side-x{display:inline-flex;position:absolute;top:12px;right:12px}
  .head-more{display:inline-flex}
}
@media (max-width:980px){""")

# ================================================================
# 15. INIT — call syncProfile once
# ================================================================
rep("""setTheme(prefs.theme);
setLang(prefs.lang);""", """setTheme(prefs.theme);
setLang(prefs.lang);
syncProfile();""")

io.open(P, "w", encoding="utf-8").write(h)
print("patched OK")
print("bytes:", orig_len, "->", len(h), f"({(len(h)-orig_len)/1024:.1f} kB added)")
print("lines:", h.count("\n") + 1)
