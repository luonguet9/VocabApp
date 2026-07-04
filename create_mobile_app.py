#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
SRC_HTML = BASE_DIR / "app" / "templates" / "index.html"
VOCAB_CSV = BASE_DIR / "vocab.csv"
MOBILE_DIR = BASE_DIR / "mobile"
MOBILE_DIR.mkdir(exist_ok=True)
OUT_HTML = MOBILE_DIR / "index.html"
VOCAB_JS = MOBILE_DIR / "vocab.js"

def parse_csv(path: Path) -> list:
    cards = []
    if not path.exists():
        return cards
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if "\t" not in line:
                continue
            parts = line.split("\t")
            front = parts[0].strip()
            back  = parts[1].strip() if len(parts) > 1 else ""
            topic = parts[2].strip() if len(parts) > 2 else ""
            level = parts[3].strip() if len(parts) > 3 else ""

            pipe_idx = back.find("|")
            vi   = (back[:pipe_idx] if pipe_idx > -1 else back).strip()
            pron = back[pipe_idx + 1:].strip() if pipe_idx > -1 else ""

            m       = re.match(r"^(.*?)\s+(\(.*\))\s*$", front)
            term    = m.group(1).strip() if m else front
            example = m.group(2).strip() if m else ""

            cards.append({
                "key":     front,
                "term":    term,
                "example": example,
                "vi":      vi,
                "pron":    pron,
                "topic":   topic,
                "deck":    level,
                "fav":     False,
                "known":   False,
            })
    return cards

def main():
    with open(SRC_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add PWA tags to head
    pwa_tags = """
  <link rel="manifest" href="manifest.json">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Vocab App">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <script src="vocab.js"></script>
"""
    html = html.replace("</head>", pwa_tags + "</head>")

    # 2. Show Sync Button in Settings overlay on mobile (unified UI with main Start button)
    html = html.replace('id="btnSyncPC" style="margin-bottom:12px;display:none"', 'id="btnSyncPC" style="margin-bottom:12px;display:block"')

    # 3. Add offline progress helpers & sync handler right after <script>
    helpers_js = """<script>
// ── OFFLINE STORAGE & SYNC ───────────────────────────────────────────────────
function getProgress() {
  try { return JSON.parse(localStorage.getItem('vocab_progress') || '{}'); }
  catch(e) { return {}; }
}
function saveProgress(key, data) {
  const prog = getProgress();
  prog[key] = { ...prog[key], ...data };
  try { localStorage.setItem('vocab_progress', JSON.stringify(prog)); }
  catch(e) {}
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  });
}
"""
    html = html.replace("<script>", helpers_js, 1)

    # 4. Replace setKnown
    old_known = """async function setKnown(c, value) {
  c.known = value;
  fetch('/api/known', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ deck: c.deck, key: c.key, known: value }),
  });
}"""
    new_known = """async function setKnown(c, value) {
  c.known = value;
  saveProgress(c.key, { known: value });
}"""
    html = html.replace(old_known, new_known)

    # 5. Replace toggleFav
    old_fav = """async function toggleFav(c) {
  c.fav = !c.fav;
  await fetch('/api/fav', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ deck: c.deck, key: c.key, fav: c.fav }),
  });
}"""
    new_fav = """async function toggleFav(c) {
  c.fav = !c.fav;
  saveProgress(c.key, { fav: c.fav });
}"""
    html = html.replace(old_fav, new_fav)

    # 6. Replace introduceCard
    old_intro = """function introduceCard(c) {
  if (!c || !c.is_new) return;
  c.is_new = false;
  newIntroduced++;
  fetch('/api/introduce', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key: c.key }),
  });
}"""
    new_intro = """function introduceCard(c) {
  if (!c || !c.is_new) return;
  c.is_new = false;
  newIntroduced++;
  const today = new Date().toLocaleDateString('en-CA');
  const prog = getProgress();
  if (!prog[c.key]) prog[c.key] = { fav: false, known: false, date: today };
  else if (!prog[c.key].date) prog[c.key].date = today;
  try { localStorage.setItem('vocab_progress', JSON.stringify(prog)); } catch(e){}
}"""
    html = html.replace(old_intro, new_intro)

    # 7. Replace history modal click
    old_hist = """document.getElementById('btnOpenHistory').addEventListener('click', async () => {
  document.getElementById('historyOverlay').classList.remove('hidden');
  const res  = await fetch('/api/history');
  const data = await res.json();
  const el   = document.getElementById('historyContent');
  if (!data.length) {
    el.innerHTML = '<p style="color:#9ca3af;font-size:0.85rem">Chưa có lịch sử học.</p>';
    return;
  }
  const today = new Date().toLocaleDateString('en-CA'); // YYYY-MM-DD local time
  el.innerHTML = data.map(day => {
    const label = day.date === today ? 'Hôm nay' :
      new Date(day.date + 'T00:00:00').toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
    return `<div class="history-day">
      <div class="history-date">📆 ${label}<em>${day.words.length} từ</em></div>
      <div class="history-words">${day.words.map(w => `<span class="history-word">${w}</span>`).join('')}</div>
    </div>`;
  }).join('');
});"""
    new_hist = """document.getElementById('btnOpenHistory').addEventListener('click', async () => {
  document.getElementById('historyOverlay').classList.remove('hidden');
  const prog = getProgress();
  const dateMap = {};
  for (const [key, val] of Object.entries(prog)) {
    if (val && val.date) {
      if (!dateMap[val.date]) dateMap[val.date] = [];
      dateMap[val.date].push(key);
    }
  }
  const data = Object.keys(dateMap).sort().reverse().map(d => ({ date: d, words: dateMap[d] }));
  const el   = document.getElementById('historyContent');
  if (!data.length) {
    el.innerHTML = '<p style="color:#9ca3af;font-size:0.85rem">Chưa có lịch sử học.</p>';
    return;
  }
  const today = new Date().toLocaleDateString('en-CA');
  el.innerHTML = data.map(day => {
    const label = day.date === today ? 'Hôm nay' :
      new Date(day.date + 'T00:00:00').toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
    return `<div class="history-day">
      <div class="history-date">📆 ${label}<em>${day.words.length} từ</em></div>
      <div class="history-words">${day.words.map(w => `<span class="history-word">${w}</span>`).join('')}</div>
    </div>`;
  }).join('');
});"""
    html = html.replace(old_hist, new_hist)

    # 8. Replace reset button
    old_reset = """document.getElementById('btnReset').addEventListener('click', async () => {
  if (!confirm('Xóa toàn bộ tiến độ (fav + known + lịch sử học)?\\nHành động này không thể hoàn tác.')) return;
  await fetch('/api/reset', { method: 'POST' });
  localStorage.removeItem('vocabDailyNew');
  dailyNew = 10;
  document.getElementById('settingsOverlay').classList.add('hidden');
  await loadCards();
});"""
    new_reset = """document.getElementById('btnReset').addEventListener('click', async () => {
  if (!confirm('Xóa toàn bộ tiến độ offline (fav + known + lịch sử học)?\\nHành động này không thể hoàn tác.')) return;
  localStorage.removeItem('vocab_progress');
  localStorage.removeItem('vocabDailyNew');
  dailyNew = 10;
  document.getElementById('settingsOverlay').classList.add('hidden');
  await loadCards();
});"""
    html = html.replace(old_reset, new_reset)

    # 9. Replace _fetchAndRender
    old_fetch = """async function _fetchAndRender(n) {
  document.getElementById('flashSection').innerHTML = '<div class="loading">Đang tải dữ liệu...</div>';

  const res = await fetch('/api/start-day', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ new: n }),
  });
  const data  = await res.json();
  allCards      = data.cards;
  reviewCount   = data.review;
  newServed     = data.today_introduced + data.new;
  newIntroduced = data.today_introduced;"""
    new_fetch = """async function _fetchAndRender(n) {
  document.getElementById('flashSection').innerHTML = '<div class="loading">Đang tải dữ liệu...</div>';

  const today = new Date().toLocaleDateString('en-CA');
  const prog = getProgress();
  let today_n = 0;
  for (const val of Object.values(prog)) {
    if (val && val.date === today) today_n++;
  }
  const remaining_new = Math.max(0, n - today_n);
  const session = [];
  let review_n = 0;
  let new_n = 0;
  for (const item of (typeof VOCAB_DATA !== 'undefined' ? VOCAB_DATA : [])) {
    const c = { ...item };
    const p = prog[c.key];
    const d = p ? p.date : null;
    if (d) {
      c.fav = Boolean(p.fav);
      c.known = Boolean(p.known);
      c.is_new = false;
      session.push(c);
      if (d !== today) review_n++;
    } else if (new_n < remaining_new) {
      c.fav = p ? Boolean(p.fav) : false;
      c.known = p ? Boolean(p.known) : false;
      c.is_new = true;
      session.push(c);
      new_n++;
    }
  }
  allCards = session;
  reviewCount = review_n;
  newServed = today_n + new_n;
  newIntroduced = today_n;"""
    html = html.replace(old_fetch, new_fetch)

    # 10. Add sync button event listener at the end before </script>
    sync_listener = """
document.getElementById('btnSyncPC').addEventListener('click', async () => {
  const ip = prompt("Nhập IP máy tính (PC) đang chạy run.bat (ví dụ 100.65.37.111):", localStorage.getItem('last_pc_ip') || "100.65.37.111");
  if (!ip) return;
  localStorage.setItem('last_pc_ip', ip.trim());
  const url = `http://${ip.trim()}:5100/api/sync`;
  try {
    const prog = getProgress();
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ progress: prog })
    });
    const data = await res.json();
    if (data.ok && data.progress) {
      localStorage.setItem('vocab_progress', JSON.stringify(data.progress));
      alert("🎉 Đồng bộ thành công với PC!");
      loadCards();
    } else {
      alert("❌ Lỗi đồng bộ: " + (data.error || "Không xác định"));
    }
  } catch (e) {
    alert("❌ Không thể kết nối với PC tại " + url + ". Hãy kiểm tra PC đã chạy run.bat và dùng chung Wi-Fi!");
  }
});

loadCards();
</script>"""
    html = html.replace("loadCards();\n</script>", sync_listener)
    html = html.replace("loadCards();\r\n</script>", sync_listener)

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] (1/3) Generated offline mobile app at {OUT_HTML}")

    # Generate vocab.js from vocab.csv
    cards = parse_csv(VOCAB_CSV)
    js_content = f"// Auto-generated from vocab.csv\nconst VOCAB_DATA = {json.dumps(cards, ensure_ascii=False, indent=2)};\n"
    with open(VOCAB_JS, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"[OK] (2/3) Generated {VOCAB_JS} with {len(cards)} cards.")

    # Generate sw.js with Network-First offline fallback strategy
    sw_path = MOBILE_DIR / "sw.js"
    sw_content = """const CACHE_NAME = 'vocab-offline-v2';
const ASSETS = [
  './',
  './index.html',
  './vocab.js',
  './manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      );
    })
  );
  self.clients.claim();
});

// Network First, fallback to Cache (Luôn lấy code mới nhất khi có mạng, dùng offline khi mất mạng)
self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const resClone = res.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(e.request, resClone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
"""
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(sw_content)
    print(f"[OK] (3/3) Generated offline service worker at {sw_path}")

    # Ensure .nojekyll exists for GitHub Pages compatibility
    with open(MOBILE_DIR / ".nojekyll", "w", encoding="utf-8") as f:
        f.write("# Disable Jekyll\n")

if __name__ == "__main__":
    main()
