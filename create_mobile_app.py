#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import time
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
SRC_HTML = BASE_DIR / "app" / "templates" / "index.html"
MOBILE_DIR = BASE_DIR / "mobile"
MOBILE_DIR.mkdir(exist_ok=True)
OUT_HTML = MOBILE_DIR / "index.html"
VOCAB_JS = MOBILE_DIR / "vocab.js"
CLUSTERS_JS = MOBILE_DIR / "clusters.js"

def load_vocab(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cards = data.get("cards", [])
    for c in cards:
        c.setdefault("fav", False)
        c.setdefault("known", False)
    return cards

def load_clusters(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("clusters", [])

def main():
    print("[BUILD] Generating multi-user offline PWA...")
    
    USERS_JSON = BASE_DIR / "data" / "users.json"
    with open(USERS_JSON, "r", encoding="utf-8") as f:
        users_data = json.load(f)
        
    vocab_data_map = {}
    clusters_data_map = {}
    
    for u in users_data.get("users", []):
        uid = u["id"]
        vocab_path = BASE_DIR / "data" / uid / "vocab.json"
        clusters_path = BASE_DIR / "clusters.json"
        
        vocab_data_map[uid] = load_vocab(vocab_path)
        clusters_data_map[uid] = load_clusters(clusters_path)

    # Generate vocab.js with ALL data
    js_content = f"""// Auto-generated offline data bundle
const USERS_DATA = {json.dumps(users_data.get("users", []), ensure_ascii=False, indent=2)};
const VOCAB_DATA_MAP = {json.dumps(vocab_data_map, ensure_ascii=False, indent=2)};
const CLUSTERS_DATA_MAP = {json.dumps(clusters_data_map, ensure_ascii=False, indent=2)};
"""
    with open(VOCAB_JS, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"[OK] Generated {VOCAB_JS} with data for {len(users_data.get('users', []))} users.")

    with open(SRC_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add PWA tags to head
    pwa_tags = """
  <link rel="manifest" href="manifest.json">
  <script src="vocab.js"></script>
"""
    html = html.replace("</head>", pwa_tags + "</head>")

    # 2. Inject the Offline Mock API Interceptor
    mock_interceptor = """
<script>
// ── OFFLINE MOCK API INTERCEPTOR ─────────────────────────────────────────────
(function() {
    function getUid() { return localStorage.getItem('vocabUserId'); }
    window.getProgress = function() {
        const uid = getUid();
        if (!uid) return {};
        try { return JSON.parse(localStorage.getItem('vocab_progress_' + uid) || '{}'); } catch(e) { return {}; }
    };
    window.saveProgressData = function(data) {
        const uid = getUid();
        if (!uid) return;
        try { localStorage.setItem('vocab_progress_' + uid, JSON.stringify(data)); } catch(e) {}
    };
    window.updateProgress = function(key, data) {
        const p = window.getProgress();
        p[key] = { ...p[key], ...data };
        window.saveProgressData(p);
    };

    const offlineFetch = window.fetch;
    window.fetch = async function(resource, config) {
        if (typeof resource === 'string' && resource.startsWith('/api/')) {
            const uid = getUid();
            let body = {};
            if (config && config.body) {
                try { body = JSON.parse(config.body); } catch(e){}
            }
            
            const jsonResponse = (data) => new Response(JSON.stringify(data), { status: 200, headers: {'Content-Type': 'application/json'} });
            const errorResponse = (msg, status=400) => new Response(JSON.stringify({error: msg}), { status: status, headers: {'Content-Type': 'application/json'} });

            if (resource === '/api/users') {
                return jsonResponse({ users: USERS_DATA });
            }
            
            if (resource === '/api/login') {
                const user = USERS_DATA.find(u => u.id === body.id && u.pin === body.pin);
                if (user) {
                    return jsonResponse({ ok: true, user_id: user.id });
                }
                return errorResponse("Sai mã PIN", 401);
            }

            if (!uid) {
                if (typeof showLoginOverlay === 'function') showLoginOverlay();
                return errorResponse("Unauthorized", 401);
            }
            
            if (resource === '/api/start-day') {
                const p = window.getProgress();
                const today = new Date().toLocaleDateString('en-CA');
                const vocab = VOCAB_DATA_MAP[uid] || [];
                
                let today_n = 0;
                let review_n = 0;
                const session = [];
                const remaining_new = Math.max(0, (body.new || 10) - today_n);
                let new_n = 0;
                
                for (const key of Object.keys(p)) {
                    if (p[key] && p[key].date === today) today_n++;
                }
                
                for (const item of vocab) {
                    const c = { ...item };
                    const st = p[c.key];
                    if (st && st.date) {
                        c.fav = Boolean(st.fav);
                        c.known = Boolean(st.known);
                        c.is_new = false;
                        session.push(c);
                        if (st.date !== today) review_n++;
                    } else if (new_n < remaining_new) {
                        c.fav = st ? Boolean(st.fav) : false;
                        c.known = st ? Boolean(st.known) : false;
                        c.is_new = true;
                        session.push(c);
                        new_n++;
                    }
                }
                return jsonResponse({
                    cards: session,
                    all_cards: vocab,
                    review: review_n,
                    today_introduced: today_n,
                    new: new_n
                });
            }
            
            if (resource === '/api/clusters') {
                const p = window.getProgress();
                const clusters = (CLUSTERS_DATA_MAP[uid] || []).map(c => {
                    const st = p[c.id] || {};
                    return { ...c, fav: Boolean(st.fav), known: Boolean(st.known), introduced_date: st.date || null };
                });
                return jsonResponse({ clusters });
            }
            
            if (resource === '/api/history') {
                const p = window.getProgress();
                const vocab = VOCAB_DATA_MAP[uid] || [];
                const termMap = {};
                for (const c of vocab) termMap[c.key] = c.term;
                
                const dateMap = {};
                for (const [key, val] of Object.entries(p)) {
                    if (val && val.date) {
                        if (!dateMap[val.date]) dateMap[val.date] = [];
                        if (termMap[key]) dateMap[val.date].push(termMap[key]);
                    }
                }
                const data = Object.keys(dateMap).sort().reverse().map(d => ({ date: d, words: dateMap[d] }));
                return jsonResponse(data);
            }
            
            if (resource === '/api/introduce') {
                const p = window.getProgress();
                const today = new Date().toLocaleDateString('en-CA');
                if (!p[body.key]) p[body.key] = { fav: false, known: false, date: today };
                else if (!p[body.key].date) p[body.key].date = today;
                window.saveProgressData(p);
                return jsonResponse({ ok: true });
            }
            
            if (resource === '/api/fav') {
                const p = window.getProgress();
                if (!p[body.key]) p[body.key] = { fav: body.fav, known: false, date: null };
                else p[body.key].fav = body.fav;
                window.saveProgressData(p);
                return jsonResponse({ ok: true });
            }
            
            if (resource === '/api/known') {
                const p = window.getProgress();
                if (!p[body.key]) p[body.key] = { fav: false, known: body.known, date: null };
                else p[body.key].known = body.known;
                window.saveProgressData(p);
                return jsonResponse({ ok: true });
            }
            
            if (resource === '/api/reset') {
                localStorage.removeItem('vocab_progress_' + uid);
                return jsonResponse({ ok: true });
            }
            
            // Allow other APIs to fall through
        }
        
        return offlineFetch(resource, config);
    };

    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js').catch(() => {});
      });
    }
})();
</script>
"""
    html = html.replace("</head>", mock_interceptor + "</head>")

    # 3. Patch the Sync button to use saveProgressData
    html = html.replace(
        "localStorage.setItem('vocab_progress', JSON.stringify(data.progress));",
        "if (typeof window.saveProgressData === 'function') { window.saveProgressData(data.progress); } else { localStorage.setItem('vocab_progress', JSON.stringify(data.progress)); }"
    )
    html = html.replace(
        "(JSON.parse(localStorage.getItem('vocab_progress') || '{}'))",
        "(typeof window.getProgress === 'function' ? window.getProgress() : JSON.parse(localStorage.getItem('vocab_progress') || '{}'))"
    )

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Generated offline mobile app at {OUT_HTML}")

    # Generate sw.js with Network-First offline fallback strategy
    sw_path = MOBILE_DIR / "sw.js"
    sw_content = "const CACHE_NAME = 'vocab-offline-" + str(int(time.time())) + "';\n" + """const ASSETS = [
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
    print(f"[OK] Generated offline service worker at {sw_path}")

    with open(MOBILE_DIR / ".nojekyll", "w", encoding="utf-8") as f:
        f.write("# Disable Jekyll\n")

if __name__ == "__main__":
    main()
