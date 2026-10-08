#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 4 patch: main-menu dashboard, sidebar LEFT, richer background, theme identity, storage hardening."""
import io

P = "/home/user/iconnect.html"
h = io.open(P, encoding="utf-8").read()
orig_len = len(h)
lines = h.split("\n")

def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, f"count {c} != {n} :: {a[:90]!r}"
    h = h.replace(a, b, 1)

def ins(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, f"count {c} != {n} :: {a[:90]!r}"
    h = h.replace(a, b + a, 1)

# ================================================================
# 1. THEME ORB VARS (first dark / light blocks only, line-based)
# ================================================================
def insert_after_line(marker, text, nth=0):
    global lines
    idxs = [i for i, l in enumerate(lines) if l.strip() == marker]
    assert len(idxs) >= nth + 1, (marker, len(idxs))
    i = idxs[nth]
    assert lines[i+1].strip().startswith("--"), lines[i+1][:60]
    lines[i+1:i+1] = [text]
    return i

insert_after_line('html[data-theme="dark"]{',
  '  --orb-1:rgba(13,128,242,.16); --orb-2:rgba(124,92,255,.12); --orb-3:rgba(22,179,100,.08); --orb-4:rgba(79,209,255,.07);')
insert_after_line('html[data-theme="light"]{',
  '  --orb-1:rgba(13,128,242,.09); --orb-2:rgba(124,92,255,.07); --orb-3:rgba(22,179,100,.05); --orb-4:rgba(79,209,255,.06);')

# ================================================================
# 2. body::after -> rich orbs (replace old single glow)
# ================================================================
rep("""body::after{
  content:"";position:fixed;z-index:0;pointer-events:none;
  top:-320px;left:50%;transform:translateX(-50%);
  width:1100px;height:700px;
  background:radial-gradient(circle, var(--brand-soft) 0%, transparent 62%);
  filter:blur(18px);opacity:.9;
}""", """body::after{
  content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(620px 460px at 8% -8%, var(--orb-1), transparent 60%),
    radial-gradient(540px 420px at 92% 0%, var(--orb-2), transparent 62%),
    radial-gradient(700px 520px at 78% 104%, var(--orb-3), transparent 62%),
    radial-gradient(420px 340px at 30% 82%, var(--orb-4), transparent 64%);
  transition:opacity .45s ease;
}""")

# smooth theme cross-fade
rep("::selection{background:var(--brand);color:#fff}",
    "body{transition:background .35s ease,color .35s ease}\n::selection{background:var(--brand);color:#fff}")

# ================================================================
# 3. header accent line
# ================================================================
rep(""".head-more svg{width:17px;height:17px}""", """.head-more svg{width:17px;height:17px}
header::after{
  content:"";position:absolute;left:0;right:0;bottom:-1px;height:1px;pointer-events:none;
  background:linear-gradient(90deg,transparent 4%,var(--brand) 32%,var(--violet) 68%,transparent 96%);
  opacity:.55;
}""")

# ================================================================
# 4. SHELL FLIP: sidebar LEFT, main right
# ================================================================
rep("""  display:grid;grid-template-columns:minmax(0,1fr) var(--sb-w);gap:22px;""",
    """  display:grid;grid-template-columns:var(--sb-w) minmax(0,1fr);gap:22px;""")
rep("""main{grid-column:1;grid-row:1;min-width:0;padding:0;width:100%}""",
    """main{grid-column:2;grid-row:1;min-width:0;padding:0;width:100%}""")
rep(""".side{
  grid-column:2;grid-row:1;position:sticky;top:calc(var(--header-h) + 22px);""",
    """.side{
  grid-column:1;grid-row:1;position:sticky;top:calc(var(--header-h) + 22px);""")
rep("""  .shell{grid-template-columns:minmax(0,1fr) var(--sb-w-c);gap:16px}""",
    """  .shell{grid-template-columns:var(--sb-w-c) minmax(0,1fr);gap:16px}""")

# drawer slides from LEFT
rep("""  .side{
    grid-column:1;grid-row:2;position:fixed;top:0;right:0;bottom:0;z-index:90;
    width:min(304px,86vw);padding:18px;overflow-y:auto;
    background:var(--surface);border-left:1px solid var(--line);
    box-shadow:-18px 0 54px rgba(0,0,0,.35);
    transform:translateX(calc(100% + 30px));transition:transform .34s var(--ease);
  }
  html[data-theme="light"] .side{box-shadow:-18px 0 54px rgba(16,24,40,.18)}""",
    """  .side{
    grid-column:1;grid-row:2;position:fixed;top:0;left:0;bottom:0;z-index:90;
    width:min(304px,86vw);padding:18px;overflow-y:auto;
    background:var(--surface);border-right:1px solid var(--line);
    box-shadow:18px 0 54px rgba(0,0,0,.35);
    transform:translateX(calc(-100% - 30px));transition:transform .34s var(--ease);
  }
  html[data-theme="light"] .side{box-shadow:18px 0 54px rgba(16,24,40,.18)}""")

# ================================================================
# 5. HERO: relative + deco layer + children above
# ================================================================
rep(""".hero{
  display:grid;grid-template-columns:1.15fr .85fr;gap:22px;align-items:center;
  margin-bottom:26px;
}""", """.hero{
  position:relative;overflow:hidden;
  display:grid;grid-template-columns:1.15fr .85fr;gap:22px;align-items:center;
  margin-bottom:26px;
}
.hero-copy{position:relative;z-index:1}
.hero-deco{position:absolute;inset:0;pointer-events:none}
.hero-deco i{
  position:absolute;display:grid;place-items:center;color:var(--brand);
  opacity:.11;animation:floaty 8s ease-in-out infinite;
}
.hero-deco svg{width:100%;height:100%}
.hero-deco .d1{width:46px;height:46px;top:6%;left:42%;color:var(--violet);animation-delay:-1.2s}
.hero-deco .d2{width:60px;height:60px;top:58%;left:1%;color:var(--ok);animation-delay:-3s}
.hero-deco .d3{width:36px;height:36px;top:12%;right:36%;animation-delay:-5s}
.hero-deco .d4{width:54px;height:54px;bottom:2%;right:1%;color:var(--violet);animation-delay:-6.4s}
.hero-deco .d5{width:30px;height:30px;bottom:34%;left:28%;color:var(--ok);animation-delay:-2.2s}
@keyframes floaty{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-14px) rotate(5deg)}}
@media (max-width:720px){.hero-deco{opacity:.7}}""")
rep(""".board-wrap{
  position:relative;background:var(--surface);border:1px solid var(--line);""",
    """.board-wrap{
  position:relative;z-index:1;background:var(--surface);border:1px solid var(--line);""")

# deco markup inside hero
rep("""  <div id="picker">
    <div class="hero">
      <div class="hero-copy">""", """  <div id="picker">
    <div class="hero">
      <div class="hero-deco" aria-hidden="true">
        <i class="d1"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7l10 10-5 4V3l5 4L7 17"/></svg></i>
        <i class="d2"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 12h3m14 0h3M5.6 5.6l2 2m8.8 8.8 2 2M5.6 18.4l2-2m8.8-8.8 2-2"/><circle cx="12" cy="12" r="5"/></svg></i>
        <i class="d3"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 2v3m4-3v3M10 19v3m4-3v3M2 10h3m-3 4h3m14-4h3m-3 4h3"/></svg></i>
        <i class="d4"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 3 4 14h6l-1 7 9-11h-6l1-7Z"/></svg></i>
        <i class="d5"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 3v18M3 12h18"/></svg></i>
      </div>
      <div class="hero-copy">""")

# ================================================================
# 6. stat pills upgrade
# ================================================================
rep(""".stat{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-sm);
  padding:10px 14px;min-width:96px;
}""", """.stat{
  position:relative;overflow:hidden;
  background:linear-gradient(180deg,var(--surface-2),var(--surface));
  border:1px solid var(--line);border-radius:var(--radius-sm);
  padding:10px 14px;min-width:96px;
  transition:.25s var(--ease);
}
.stat::after{content:"";position:absolute;left:0;top:0;bottom:0;width:2.5px;border-radius:2px;background:linear-gradient(180deg,var(--brand),var(--violet));opacity:.6}
.stat:hover{transform:translateY(-2px);border-color:var(--line-strong)}""")

# ================================================================
# 7. MODES -> big main-menu tiles
# ================================================================
rep(""".modes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.mode{
  position:relative;text-align:left;cursor:pointer;overflow:hidden;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);
  padding:20px;box-shadow:var(--shadow);
  transition:.32s var(--ease-out);
}
.mode::after{
  content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:linear-gradient(140deg, var(--brand-soft), transparent 55%);
  opacity:0;transition:.32s var(--ease);
}
.mode:hover{transform:translateY(-5px);border-color:var(--brand-line);box-shadow:var(--shadow-lg)}
.mode:hover::after{opacity:1}
.mode-n{
  position:absolute;top:16px;right:18px;font-size:34px;font-weight:800;
  color:var(--txt);opacity:.07;letter-spacing:-.04em;
}
.mode .ic{width:40px;height:40px;border-radius:12px;margin-bottom:36px}
.mode .ic svg{width:20px;height:20px}
.mode h3{font-size:15.5px;font-weight:700;letter-spacing:-.01em}
.mode p{font-size:12.5px;color:var(--txt-2);margin-top:6px;line-height:1.55;min-height:38px}
.mode-go{
  display:flex;align-items:center;gap:6px;margin-top:14px;
  font-size:12px;font-weight:700;color:var(--brand);
  transition:gap .25s var(--ease);
}
.mode:hover .mode-go{gap:11px}""", """.modes{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mode{
  position:relative;text-align:left;cursor:pointer;overflow:hidden;
  background:linear-gradient(165deg,var(--surface-2),var(--surface) 58%);
  border:1px solid var(--line);border-radius:22px;
  padding:22px 20px 18px;box-shadow:var(--shadow);
  transition:.32s var(--ease-out);
  display:flex;flex-direction:column;
}
.mode::after{
  content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:linear-gradient(140deg, var(--brand-soft), transparent 55%);
  opacity:0;transition:.32s var(--ease);
}
.mode::before{
  content:"";position:absolute;top:-26px;right:-26px;width:130px;height:130px;
  border-radius:40px;pointer-events:none;
  background:linear-gradient(135deg,var(--brand),var(--violet));
  opacity:.05;transform:rotate(22deg);transition:.4s var(--ease-out);
}
.mode:hover{transform:translateY(-6px);border-color:var(--brand-line);box-shadow:var(--shadow-lg)}
.mode:hover::after{opacity:1}
.mode:hover::before{opacity:.10;transform:rotate(8deg) scale(1.12)}
.mode-n{
  position:absolute;top:14px;right:18px;font-size:44px;font-weight:800;
  color:var(--txt);opacity:.08;letter-spacing:-.04em;
}
.mode .ic{width:54px;height:54px;border-radius:16px;margin-bottom:20px;box-shadow:0 8px 20px var(--brand-soft)}
.mode .ic svg{width:26px;height:26px}
.mode h3{font-size:17px;font-weight:750;letter-spacing:-.02em}
.mode p{font-size:12.5px;color:var(--txt-2);margin-top:7px;line-height:1.6;min-height:40px}
.mode-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.mode-tags span{
  font-size:10px;font-weight:650;letter-spacing:.02em;color:var(--txt-2);
  background:var(--surface-3);border:1px solid var(--line);
  padding:4px 9px;border-radius:99px;
}
.mode-go{
  display:flex;align-items:center;gap:6px;margin-top:auto;padding-top:16px;
  font-size:12px;font-weight:750;color:var(--brand);
  transition:gap .25s var(--ease);
}
.mode:hover .mode-go{gap:11px}""")

# ================================================================
# 8. mode tags markup (after each mode <p>)
# ================================================================
rep('<p data-i18n="m1_p">Pantau suhu, kelembaban, cahaya, dan data sensor lain lewat grafik real-time.</p>',
    '<p data-i18n="m1_p">Pantau suhu, kelembaban, cahaya, dan data sensor lain lewat grafik real-time.</p>\n'
    '        <div class="mode-tags"><span data-i18n="mt_s1">Grafik live</span><span data-i18n="mt_s2">5+ sensor</span><span data-i18n="mt_s3">Kartu otomatis</span></div>')
rep('<p data-i18n="m2_p">D-pad presisi, dua slider servo, dan tombol A/B untuk mengemudikan robot.</p>',
    '<p data-i18n="m2_p">D-pad presisi, dua slider servo, dan tombol A/B untuk mengemudikan robot.</p>\n'
    '        <div class="mode-tags"><span data-i18n="mt_r1">D-pad presisi</span><span data-i18n="mt_r2">Servo ×2</span><span data-i18n="mt_r3">Klakson &amp; A/B</span></div>')
rep('<p data-i18n="m3_p">Semua panel sekaligus: sensor, kontrol robot, dan matriks LED dalam satu layar.</p>',
    '<p data-i18n="m3_p">Semua panel sekaligus: sensor, kontrol robot, dan matriks LED dalam satu layar.</p>\n'
    '        <div class="mode-tags"><span data-i18n="mt_a1">Semua panel</span><span data-i18n="mt_a2">Satu layar penuh</span><span data-i18n="mt_a3">Kontrol + matriks</span></div>')

# ================================================================
# 9. i18n keys mt_* x5 langs (line-based: after each m3_p line in region)
# ================================================================
TAG_KEYS = {
 'id': '    mt_s1:"Grafik live", mt_s2:"5+ sensor", mt_s3:"Kartu otomatis", mt_r1:"D-pad presisi", mt_r2:"Servo ×2", mt_r3:"Klakson & A/B", mt_a1:"Semua panel", mt_a2:"Satu layar penuh", mt_a3:"Kontrol + matriks",',
 'en': '    mt_s1:"Live graphs", mt_s2:"5+ sensors", mt_s3:"Auto cards", mt_r1:"Precision D-pad", mt_r2:"Servo ×2", mt_r3:"Horn & A/B", mt_a1:"Every panel", mt_a2:"One full screen", mt_a3:"Control + matrix",',
 'ja': '  mt_s1:"ライブグラフ", mt_s2:"5+ センサー", mt_s3:"自動カード", mt_r1:"精密 D-pad", mt_r2:"サーボ ×2", mt_r3:"ホーン & A/B", mt_a1:"全パネル", mt_a2:"1 画面にまとめて", mt_a3:"操作 + マトリックス",',
 'zh': '  mt_s1:"实时曲线", mt_s2:"5+ 传感器", mt_s3:"自动卡片", mt_r1:"精准方向键", mt_r2:"舵机 ×2", mt_r3:"喇叭 & A/B", mt_a1:"全部面板", mt_a2:"一屏全览", mt_a3:"控制 + 点阵",',
 'es': '  mt_s1:"Gráficas en vivo", mt_s2:"5+ sensores", mt_s3:"Tarjetas auto", mt_r1:"Cruceta precisa", mt_r2:"Servo ×2", mt_r3:"Bocina & A/B", mt_a1:"Todos los paneles", mt_a2:"Una pantalla", mt_a3:"Control + matriz",',
}
markers = ['  id:{', '  en:{', 'I18N.ja = {', 'I18N.zh = {', 'I18N.es = {']
for idx, mk in enumerate(markers):
    mpos = [i for i, l in enumerate(lines) if l.strip() == mk.strip()]
    assert len(mpos) == 1, (mk, len(mpos))
    m = mpos[0]
    nxt = [i for i in range(m, len(lines)) if 'm3_p:' in lines[i]]
    assert nxt, mk
    n = nxt[0]
    lines[n+1:n+1] = [TAG_KEYS['id' if idx == 0 else 'en' if idx == 1 else ['ja','zh','es'][idx-2]]]

# ================================================================
# 10. storage hardening
# ================================================================
rep("""const prefs = Object.assign({theme:"dark",lang:"id",demo:false,auto:true,sfx:"soft",name:"",tag:"",avatar:""},
  JSON.parse(localStorage.getItem(LS) || "{}"));
const savePrefs = () => localStorage.setItem(LS, JSON.stringify(prefs));""",
    """const prefs = Object.assign({theme:"dark",lang:"id",demo:false,auto:true,sfx:"soft",name:"",tag:"",avatar:""},
  (() => { try { return JSON.parse(localStorage.getItem(LS) || "{}"); } catch(e){ return {}; } })());
const savePrefs = () => { try { localStorage.setItem(LS, JSON.stringify(prefs)); } catch(e){} };""")

# ================================================================
# write
# ================================================================
h = "\n".join(lines)
io.open(P, "w", encoding="utf-8").write(h)
print("r4 patched OK")
print("bytes:", orig_len, "->", len(h), f"({(len(h)-orig_len)/1024:.1f} kB added)")
print("lines:", h.count("\n") + 1)
