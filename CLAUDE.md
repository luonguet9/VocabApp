# CLAUDE.md — English Learning App

## Project Overview
Web app học từ vựng và cụm từ tiếng Anh chuyên nghiệp cho IT professional (B1 → C1).
Hỗ trợ cả chế độ Web PC (Flask Backend đa người dùng) và ứng dụng Offline HTML/Mobile App (PWA).

## Stack & Storage
- **Backend**: Python + Flask dev server (port 5100) — `app.run(debug=False, use_reloader=False, threaded=True)`. Waitress đã bị bỏ vì hung khi chạy qua subprocess trên Windows.
- **Frontend**: Single-page app, vanilla JS, HTML5, modern design
- **Storage**:
  - `data/users.json`: Danh sách người dùng và PIN để xác thực.
  - `data/<user_id>/vocab.json`: Bộ từ vựng riêng biệt cho từng user (luong: 1500 thẻ / 150 ngày).
  - `clusters.json` (root): 21 cụm từ (Collocation, Grammar, Idiom) dùng chung cho mọi user.
  - `progress.db`: SQLite lưu trạng thái học tập. Khóa chính là `(user_id, key)`.
- **Run**: `run.bat` — kiểm tra dependencies, chạy server, mở browser.

## Project Structure
```
ENG/
├── run.bat                  # Chạy server (double-click)
├── clusters.json            # 21 cụm từ chuyên đề gốc dùng chung (Grammar, Collocations)
├── progress.db              # SQLite: user_id, key, fav, known, introduced_date, updated_at
├── create_mobile_app.py     # Script build offline PWA cho TẤT CẢ users trong users.json
├── build_mobile.bat         # Wrapper chạy create_mobile_app.py (tham số --user bị ignore)
├── mobile/                  # PWA offline (generated) — dùng cho Github Pages
├── data/
│   ├── users.json           # Cấu hình user: id, pin, name, avatar
│   ├── luong/
│   │   └── vocab.json       # 1500 thẻ: IPA, nghĩa, ví dụ, synonyms, collocations
│   └── khanh/
│       └── vocab.json       # vocab riêng của khanh
├── app/
│   ├── main.py              # Flask server, tất cả API endpoints (Multi-User)
│   └── templates/
│       └── index.html       # Toàn bộ frontend (HTML + CSS + JS, ~3800 lines)
```

## JSON Formats

### 1. `data/<user_id>/vocab.json` Item Schema
```json
{
  "key": "cluster_1_0",
  "term": "term",
  "example": "(Example sentence)",
  "vi": "Vietnamese meaning",
  "pron": "🇺🇸 /us-ipa/ 🇬🇧 /uk-ipa/",
  "pos": "n. / v. / adj.",
  "deck": "B1 | B2 | C1/C2",
  "topic": "Tech | Business | ...",
  "en_def": "English dictionary definition",
  "synonyms": ["word1", "word2"],
  "antonyms": ["word1"],
  "collocations": ["colloc 1", "colloc 2"],
  "cluster": "cluster_1",
  "day": 1,
  "en_def_vi": "Bản dịch tiếng Việt của en_def — hint cho nút Gợi ý ở quiz en_def",
  "synonyms_vi": {"word1": "nghĩa tiếng Việt"},
  "antonyms_vi": {"word1": "nghĩa tiếng Việt"},
  "collocations_vi": {"colloc 1": "nghĩa tiếng Việt"},
  "example_vi": "Bản dịch tiếng Việt của example (data-only, CHƯA wire vào UI)",
  "phonetic_distractors": ["word1", "word2", "word3"],
  "ipa_distractors": {"word1": "/ipa1/", "word2": "/ipa2/"}
}
```
- Các field `*_vi` (trừ `en_def_vi`) và `phonetic_distractors`/`ipa_distractors` **không bắt buộc** — chỉ có ở phần lớn card đã được backfill; term nhiều từ (vd "merge conflict") thường không có 2 field distractors vì quiz phát âm chỉ áp dụng cho từ đơn.
- `synonyms_vi`/`collocations_vi`/`antonyms_vi` là **object map** `{cụm gốc: nghĩa Việt}` (không phải mảng song song) để tránh lệch khi lọc/dedupe — dùng chung hàm `pillVi(text, viMap)` trong `index.html` để hiện `(nghĩa việt)` mờ cạnh mỗi pill, CHỈ ở flashcard back và explain box sau khi trả lời (không hiện lúc quiz đang hỏi collocations/synonym_match/antonyms vì các field gốc chính là đáp án quiz).
- `ipa_distractors` là object map `{từ: IPA}` (không phải mảng) để giữ đúng liên kết từ↔IPA khi hiển thị.
- **Bất biến quan trọng**: nếu sửa `en_def`, PHẢI generate lại `en_def_vi` tương ứng — 2 field này luôn phải khớp nội dung.

### 2. `clusters.json` Schema (Root)
Mỗi cụm chứa `id`, `name`, `type`, `level`, `desc`, và mảng `words`.

## progress.db Schema
```sql
CREATE TABLE progress (
    user_id         TEXT,
    key             TEXT,
    fav             INTEGER DEFAULT 0,
    known           INTEGER DEFAULT 0,
    introduced_date TEXT,
    updated_at      TEXT,        -- ISO timestamp, dùng để conflict resolution khi sync
    PRIMARY KEY (user_id, key)
)
```
Migration tự động khi server khởi động (ALTER TABLE nếu chưa có `updated_at`).

## Sync Mobile ↔ PC
- **API**: `POST /api/sync` — client gửi toàn bộ progress, server trả về progress đã merge.
- **Conflict resolution**: `updated_at` timestamp — phía nào mới hơn thắng cho `fav`/`known`; `introduced_date` dùng COALESCE (giữ giá trị cũ nhất).
- **Mobile dialog**: Button "Đồng bộ với PC" mở dialog nhập hostname/IP. Default: `luongblue.tail6851a5.ts.net` (Tailscale).
- **Auto-sync**: Khi mở app mobile, tự động sync silent với IP đã lưu trong localStorage.
- **URL logic** (`getSyncUrl`): nếu có `.ts.net` → dùng HTTPS; nếu IP → thêm `:5100`; nếu có prefix http/https → dùng nguyên.

## Frontend Key Patterns (index.html)
- **Tab-specific elements**: dùng class `tab-only-flash`, `tab-only-quiz`, `tab-only-cluster` — tab switch handler tự discover qua `querySelectorAll`.
- **Flash stats**: `sessionMarks = new Map()` lưu mark cuối cùng mỗi thẻ → `knownCount()`/`unknownCount()` là functions (tránh double-count khi mark lại).
- **Toast**: `showToast(msg, type)` — hiện bottom toast, tự ẩn sau 3s.
- **quickStatsBar**: hiện "Đã thuộc X/total + Streak N ngày" chỉ ở tab Flash Card.
- **cardFilter**: `'all'` | `'unknown'` (chưa thuộc) | `'new'` | `'known'` — reset về `'all'` mỗi lần `loadCards()`.
- **Lucide icons**: Dùng Lucide v0.525.0 (`<i data-lucide="name">`). **RULE**: Mỗi khi set `.innerHTML` có chứa `<i data-lucide>`, bắt buộc gọi `lucide.createIcons({ nodes: [el] })` ngay sau đó — nếu không icon sẽ không render (silent failure). Static HTML trong template tự render khi page load. Với `.textContent` phải đổi sang `.innerHTML` trước.
- **Lucide trong mobile PWA**: `lucide.min.js` được bundle vào `mobile/` và load bởi `create_mobile_app.py`. Mọi Lucide pattern trong `index.html` cũng cần được patch vào `mobile/index.html`.
- **Luyện Phát âm** (`pronMode`, Practice Home `data-practice="pron"`): khi bật, `buildQuizQuestion()` chỉ chọn trong 3 quiz type: `listening_basic` (luôn có), `listening_minimal` (cần `phonetic_distractors.length >= 3`), `ipa_pick` (cần `Object.values(c.ipa_distractors)` có ≥3 giá trị unique). Reset `pronMode = false` mỗi khi vào `showPracticeHome()` hoặc đổi mode khác.
- **Nút "Gợi ý" (quiz `en_def`)**: `.quiz-hint-btn` ẩn `.quiz-hint-text` (chứa `c.en_def_vi`) mặc định, click để reveal — chỉ dịch phần định nghĩa (câu hỏi), không lộ đáp án (term).

## Offline Mobile Build (PWA cho Github Pages)
```bash
# Build (tạo lại mobile/ từ data hiện tại)
python create_mobile_app.py

# Hoặc dùng batch wrapper
build_mobile.bat
```
Output: `mobile/vocab.js` (data tất cả users), `mobile/index.html`, `mobile/sw.js` (Network-First cache).
Sau đó commit `mobile/` lên Github Pages để chạy hoàn toàn offline.

