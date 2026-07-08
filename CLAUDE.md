# CLAUDE.md — English Learning App

## Project Overview
Web app học từ vựng và cụm từ tiếng Anh chuyên nghiệp cho IT professional (B1 → C1).
Hỗ trợ cả chế độ Web PC (Flask Backend) và ứng dụng Offline HTML/Mobile App.

## Stack & Storage
- **Backend**: Python + Flask + Waitress (port 5100)
- **Frontend**: Single-page app, vanilla JS, HTML5, modern design
- **Storage**:
  - `vocab.json`: 1402 từ vựng B1/B2/C1 cấu trúc JSON phong phú (term, vi, ipa, ex, type, level, topic, quiz options...).
  - `clusters.json`: 21 cụm từ (Collocation, Grammar, Idiom) cấu trúc chuỗi/chủ đề B1/B2/C1.
  - `progress.db`: SQLite lưu trạng thái học tập của người dùng (fav, known, introduced_date).
- **Run**: `run.bat` — tự động kiểm tra dependencies, chạy server và mở browser.

## Project Structure
```
ENG/
├── run.bat                  # Chạy server (double-click)
├── vocab.json               # 1402 thẻ từ vựng đầy đủ IPA, nghĩa, ví dụ, quiz
├── clusters.json            # 21 cụm từ chuyên đề (Grammar, Collocations, Phrasal verbs)
├── progress.db              # SQLite: fav, known, introduced_date
├── create_mobile_app.py     # Build offline app sang thư mục mobile/
├── mobile/                  # Gói ứng dụng HTML/JS offline chạy không cần server
├── app/
│   ├── main.py              # Flask server, tất cả API endpoints
│   └── templates/
│       └── index.html       # Toàn bộ frontend (HTML + CSS + JS)
└── docs/                    # Tài liệu học tập
```

## JSON Formats

### 1. `vocab.json` Item Schema
```json
{
  "key": "term (example)",
  "term": "term",
  "vi": "Vietnamese meaning",
  "ipa_us": "/us-ipa/",
  "ipa_uk": "/uk-ipa/",
  "type": "n. / v. / adj.",
  "deck": "B1 | B2 | C1",
  "topic": "IT & Software | Business | ...",
  "ex_en": "Example sentence",
  "ex_vi": "Dịch ví dụ"
}
```

### 2. `clusters.json` Schema
Mỗi cụm chứa `id`, `name`, `type`, `level`, `desc`, và mảng `words` chứa các từ/cụm từ con trong chuyên đề.

## progress.db Schema
```sql
CREATE TABLE progress (
    key             TEXT PRIMARY KEY,
    fav             INTEGER DEFAULT 0,
    known           INTEGER DEFAULT 0,
    introduced_date TEXT
)
```

## Offline Mobile Build
Để tạo hoặc cập nhật bản Offline chạy trên di động hoặc trình duyệt không cần backend Python:
```bash
python create_mobile_app.py
```
Script tự động đóng gói `vocab.json` và `clusters.json` thành `mobile/vocab.js` & `mobile/clusters.js`, cùng với `mobile/index.html` và service worker.

