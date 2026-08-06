#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import hashlib
import urllib.request
from pathlib import Path

LUCIDE_CDN = "https://unpkg.com/lucide@0.525.0/dist/umd/lucide.min.js"
LUCIDE_LOCAL = "lucide.min.js"

BASE_DIR = Path(__file__).parent.resolve()
SRC_HTML = BASE_DIR / "app" / "templates" / "index.html"
MOBILE_DIR = BASE_DIR / "mobile"
MOBILE_DIR.mkdir(exist_ok=True)
OUT_HTML = MOBILE_DIR / "index.html"
VOCAB_JS = MOBILE_DIR / "vocab.js"

MANIFEST_CONTENT = {
    "name": "Vocab Practice",
    "short_name": "Vocab",
    "description": "Offline English Vocabulary Practice",
    "start_url": "./index.html",
    "display": "standalone",
    "background_color": "#0f172a",
    "theme_color": "#0f172a",
    "orientation": "portrait-primary",
}

def _hash_pin(pin) -> str:
    """SHA-256 hash of PIN, first 16 hex chars — stored in vocab.js instead of plain PIN."""
    return hashlib.sha256(str(pin).encode('utf-8')).hexdigest()[:16]

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

def load_patterns(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("patterns", [])

_DEFAULT_TRACK = [{"id": "default", "name": "Mặc định", "file": "vocab.json"}]

def load_tracks(user_dir: Path) -> list:
    path = user_dir / "tracks.json"
    if not path.exists():
        return _DEFAULT_TRACK
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("tracks") or _DEFAULT_TRACK

def main():
    print("[BUILD] Generating multi-user offline PWA...")

    USERS_JSON = BASE_DIR / "data" / "users.json"
    with open(USERS_JSON, "r", encoding="utf-8") as f:
        users_data = json.load(f)

    vocab_data_map = {}
    shared_vocab_data = {}
    tracks_data_map = {}

    shared_dir = BASE_DIR / "data" / "shared"
    clusters_path = shared_dir / "clusters.json"
    patterns_path = shared_dir / "patterns.json"
    # Cluster/Pattern dùng chung cho MỌI user -- load 1 lần duy nhất thay vì lặp lại per-user,
    # tránh nhân bản JSON 3 lần trong vocab.js (patterns đã sửa từ trước; cluster sửa cùng đợt
    # với vocab track shared dưới đây, vì cùng 1 nguyên nhân: dữ liệu giống hệt nhau không cần
    # lặp theo user).
    clusters_data = load_clusters(clusters_path)
    patterns_data = load_patterns(patterns_path)

    for u in users_data.get("users", []):
        uid = u["id"]
        user_dir = BASE_DIR / "data" / uid

        tracks = load_tracks(user_dir)
        vocab_data_map[uid] = {}
        for t in tracks:
            if t.get("shared"):
                # Track dùng chung (vd Common/TOEIC/IELTS) -- load 1 lần duy nhất vào
                # shared_vocab_data, KHÔNG lặp lại cho từng user (trước đây mỗi user có 1 bản
                # riêng y hệt nhau, nhân JSON lên 3 lần cho 3 user dùng chung track này).
                if t["id"] not in shared_vocab_data:
                    shared_vocab_data[t["id"]] = load_vocab(shared_dir / t["file"])
            else:
                vocab_data_map[uid][t["id"]] = load_vocab(user_dir / t["file"])
        tracks_data_map[uid] = [
            {"id": t["id"], "name": t["name"], "shared": bool(t.get("shared"))} for t in tracks
        ]

    # Build safe user list: strip PIN, embed SHA-256 hash for offline auth
    safe_users = []
    for u in users_data.get("users", []):
        safe_u = {k: v for k, v in u.items() if k != 'pin'}
        safe_u['pin_hash'] = _hash_pin(u.get('pin', ''))
        safe_u['no_pin'] = not u.get('pin')
        safe_users.append(safe_u)

    # Generate vocab.js with ALL data
    js_content = f"""// Auto-generated offline data bundle
const USERS_DATA = {json.dumps(safe_users, ensure_ascii=False, indent=2)};
const VOCAB_DATA_MAP = {json.dumps(vocab_data_map, ensure_ascii=False, indent=2)};
const SHARED_VOCAB_DATA = {json.dumps(shared_vocab_data, ensure_ascii=False, indent=2)};
const TRACKS_DATA_MAP = {json.dumps(tracks_data_map, ensure_ascii=False, indent=2)};
const CLUSTERS_DATA = {json.dumps(clusters_data, ensure_ascii=False, indent=2)};
const PATTERNS_DATA = {json.dumps(patterns_data, ensure_ascii=False, indent=2)};
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
    // Migrate legacy single-track progress (flat 'vocab_progress_<uid>' key) to the new
    // per-track key 'vocab_progress_<uid>_<trackId>', so an existing offline install doesn't lose data.
    (function migrateLegacyProgress() {
        try {
            USERS_DATA.forEach(u => {
                const legacyKey = 'vocab_progress_' + u.id;
                const legacy = localStorage.getItem(legacyKey);
                if (legacy === null) return;
                const tracks = TRACKS_DATA_MAP[u.id] || [{id: 'default'}];
                const newKey = 'vocab_progress_' + u.id + '_' + tracks[0].id;
                if (localStorage.getItem(newKey) === null) localStorage.setItem(newKey, legacy);
                localStorage.removeItem(legacyKey);
            });
        } catch(e) {}
    })();

    function getUid() { return localStorage.getItem('vocabUserId'); }
    function getTrackId() {
        const uid = getUid();
        const tracks = TRACKS_DATA_MAP[uid] || [{id: 'default'}];
        const saved = uid && localStorage.getItem('vocabTrackId_' + uid);
        if (saved && tracks.some(t => t.id === saved)) return saved;
        return tracks[0].id;
    }
    // Track "shared" (Common/TOEIC/IELTS) chỉ lưu 1 bản dùng chung trong SHARED_VOCAB_DATA
    // (không lặp lại theo từng user) -- tra field "shared" trên TRACKS_DATA_MAP để biết lấy
    // đúng nguồn.
    function getVocabForTrack(uid, trackId) {
        const track = (TRACKS_DATA_MAP[uid] || []).find(t => t.id === trackId);
        if (track && track.shared) return SHARED_VOCAB_DATA[trackId] || [];
        return (VOCAB_DATA_MAP[uid] || {})[trackId] || [];
    }
    window.getProgress = function() {
        const uid = getUid();
        if (!uid) return {};
        try { return JSON.parse(localStorage.getItem('vocab_progress_' + uid + '_' + getTrackId()) || '{}'); } catch(e) { return {}; }
    };
    window.saveProgressData = function(data) {
        const uid = getUid();
        if (!uid) return;
        try { localStorage.setItem('vocab_progress_' + uid + '_' + getTrackId(), JSON.stringify(data)); } catch(e) {}
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
                const safeUsers = USERS_DATA.map(({ pin_hash, ...u }) => u);
                return jsonResponse({ users: safeUsers });
            }

            if (resource === '/api/login') {
                const pinStr = String(body.pin || '');
                const pinEnc = new TextEncoder().encode(pinStr);
                const hashBuf = await crypto.subtle.digest('SHA-256', pinEnc);
                const pinHash = Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, '0')).join('').slice(0, 16);
                const user = USERS_DATA.find(u => u.id === body.id && u.pin_hash === pinHash);
                if (user) {
                    return jsonResponse({ ok: true, user_id: user.id });
                }
                return errorResponse("Sai mã PIN", 401);
            }

            if (!uid) {
                if (typeof showLoginOverlay === 'function') showLoginOverlay();
                return errorResponse("Unauthorized", 401);
            }

            if (resource === '/api/tracks') {
                const tracks = TRACKS_DATA_MAP[uid] || [{id: 'default', name: 'Mặc định'}];
                return jsonResponse({ tracks, default: tracks[0].id });
            }

            if (resource === '/api/start-day') {
                const p = window.getProgress();
                const today = new Date().toLocaleDateString('en-CA');
                const vocab = getVocabForTrack(uid, getTrackId());

                const vocabKeys = new Set(vocab.map(item => item.key));
                let today_n = 0;
                for (const key of Object.keys(p)) {
                    if (vocabKeys.has(key) && p[key] && p[key].date === today) today_n++;
                }
                let review_n = 0;
                const session = [];
                const remaining_new = Math.max(0, (body.new || 10) - today_n);
                let new_n = 0;

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
                const trackId = getTrackId();
                const clusters = CLUSTERS_DATA
                    .filter(c => (c.tracks || []).includes(trackId))
                    .map(c => {
                        const st = p[c.id] || {};
                        return { ...c, fav: Boolean(st.fav), known: Boolean(st.known), introduced_date: st.date || null };
                    });
                return jsonResponse({ clusters });
            }

            if (resource === '/api/patterns') {
                const p = window.getProgress();
                // Luyện Pattern dùng chung cho mọi user/track (không lọc theo track như vocab/cluster).
                const patterns = PATTERNS_DATA
                    .map(pt => {
                        const st = p[pt.id] || {};
                        return { ...pt, fav: Boolean(st.fav), known: Boolean(st.known), introduced_date: st.date || null };
                    });
                return jsonResponse({ patterns });
            }

            if (resource === '/api/history') {
                const p = window.getProgress();
                const vocab = getVocabForTrack(uid, getTrackId());
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
                const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
                if (!p[body.key]) p[body.key] = { fav: body.fav, known: false, date: null, updated_at: ts };
                else { p[body.key].fav = body.fav; p[body.key].updated_at = ts; }
                window.saveProgressData(p);
                return jsonResponse({ ok: true });
            }

            if (resource === '/api/known') {
                const p = window.getProgress();
                const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
                if (!p[body.key]) p[body.key] = { fav: false, known: body.known, date: null, updated_at: ts };
                else { p[body.key].known = body.known; p[body.key].updated_at = ts; }
                window.saveProgressData(p);
                return jsonResponse({ ok: true });
            }

            if (resource === '/api/reset') {
                localStorage.removeItem('vocab_progress_' + uid + '_' + getTrackId());
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

    # Download Lucide locally for offline use
    lucide_path = MOBILE_DIR / LUCIDE_LOCAL
    if not lucide_path.exists():
        print(f"[DL]  Downloading Lucide icons from CDN...")
        with urllib.request.urlopen(LUCIDE_CDN) as response, open(lucide_path, 'wb') as out_file:
            out_file.write(response.read())
    print(f"[OK] Lucide icons available at {lucide_path}")

    # Replace CDN src with local path in mobile HTML
    cdn_tag = f'<script src="{LUCIDE_CDN}"></script>'
    if cdn_tag not in html:
        raise RuntimeError(
            f"Lucide CDN tag not found in {SRC_HTML} -- LUCIDE_CDN is out of date "
            "(version/attributes changed?). Update LUCIDE_CDN in create_mobile_app.py "
            "or mobile/index.html will still point at the CDN and break offline."
        )
    html = html.replace(cdn_tag, f'<script src="./{LUCIDE_LOCAL}"></script>')

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Generated offline mobile app at {OUT_HTML}")

    # Generate manifest.json (previously only existed because it was committed by hand)
    with open(MOBILE_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(MANIFEST_CONTENT, f, ensure_ascii=False, indent=2)
    print(f"[OK] Generated {MOBILE_DIR / 'manifest.json'}")

    # Remove stale build artifacts from older versions of this script
    stale_clusters_js = MOBILE_DIR / "clusters.js"
    if stale_clusters_js.exists():
        stale_clusters_js.unlink()
        print(f"[OK] Removed stale {stale_clusters_js} (cluster data now lives in vocab.js)")

    # Generate sw.js with Network-First offline fallback strategy
    sw_path = MOBILE_DIR / "sw.js"
    vocab_hash = hashlib.md5(js_content.encode('utf-8')).hexdigest()[:8]
    sw_content = f"const CACHE_NAME = 'vocab-offline-{vocab_hash}';\n" + """const ASSETS = [
  './',
  './index.html',
  './vocab.js',
  './lucide.min.js',
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
  if (e.request.method !== 'GET') return;  // Cache API chỉ chấp nhận GET -- POST (vd /api/sync) đi thẳng qua network
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const resClone = res.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(e.request, resClone));
        return res;
      })
      .catch(() => caches.match(e.request).then(cached => cached || caches.match('./index.html')))
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
