# CLAUDE.md — English Learning App

## Project Overview
Web app học từ vựng và cụm từ tiếng Anh chuyên nghiệp cho IT professional (B1 → C1).
Hỗ trợ cả chế độ Web PC (Flask Backend đa người dùng) và ứng dụng Offline HTML/Mobile App (PWA).

## Stack & Storage
- **Backend**: Python + Flask + Waitress (port 5100)
- **Frontend**: Single-page app, vanilla JS, HTML5, modern design
- **Storage**:
  - `data/users.json`: Danh sách người dùng và PIN để xác thực.
  - `data/<user_id>/vocab.json`: Bộ từ vựng được gen riêng biệt cho từng người dùng (Ví dụ: `luong` có 1500 từ vựng chia thành 150 ngày học).
  - `clusters.json` (root): 21 cụm từ (Collocation, Grammar, Idiom) gốc dùng chung cho mọi user.
  - `progress.db`: SQLite lưu trạng thái học tập của người dùng. Khóa chính là `(user_id, key)`.
- **Run**: `run.bat` — tự động kiểm tra dependencies, chạy server và mở browser ở chế độ PC.

## Project Structure
```
ENG/
├── run.bat                  # Chạy server (double-click)
├── clusters.json            # 21 cụm từ chuyên đề gốc dùng chung (Grammar, Collocations)
├── progress.db              # SQLite: user_id, key, fav, known, introduced_date
├── create_mobile_app.py     # Script Python build offline app sang thư mục mobile/
├── build_mobile.bat         # Chạy tool build mobile nhanh gọn cho từng user (vd: luong, khanh)
├── mobile/                  # Gói ứng dụng HTML/JS offline (PWA) chạy không cần server (Dùng cho Github Pages)
├── data/                    # Nơi chứa thông tin User và Database từ vựng cá nhân hoá
│   ├── users.json           # File cấu hình user đăng nhập (id, pin, name, avatar)
│   ├── luong/               # Dữ liệu từ vựng riêng của user luong
│   │   └── vocab.json       # 1500 thẻ từ vựng đầy đủ IPA, nghĩa, ví dụ, synonyms, collocations
│   └── khanh/               # Dữ liệu từ vựng riêng của user khanh (1200 thẻ)
├── app/
│   ├── main.py              # Flask server, tất cả API endpoints (Đã hỗ trợ Multi-User)
│   └── templates/
│       └── index.html       # Toàn bộ frontend (HTML + CSS + JS)
```

## JSON Formats

### 1. `data/<user_id>/vocab.json` Item Schema
Dữ liệu được tổ chức thành 2 mảng chính: `clusters` (các nhóm/ngày học) và `cards` (các từ vựng cụ thể).
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
  "collocations": ["colloc 1", "colloc 2"],
  "cluster": "cluster_1",
  "day": 1
}
```

### 2. `clusters.json` Schema (Root)
Mỗi cụm chứa `id`, `name`, `type`, `level`, `desc`, và mảng `words` chứa các từ/cụm từ con trong chuyên đề để học riêng biệt tại tab Clusters.

## progress.db Schema
Đã nâng cấp để hỗ trợ nhiều người dùng (Multi-user) trên cùng 1 CSDL.
```sql
CREATE TABLE progress (
    user_id         TEXT,
    key             TEXT,
    fav             INTEGER DEFAULT 0,
    known           INTEGER DEFAULT 0,
    introduced_date TEXT,
    PRIMARY KEY (user_id, key)
)
```

## Offline Mobile Build (PWA cho Github Pages)
Để tạo hoặc cập nhật bản Offline chạy trên di động hoặc trình duyệt tĩnh (Github Pages):
```bash
# Sử dụng Batch script (Khuyên dùng)
build_mobile.bat

# Hoặc dùng lệnh thủ công:
python create_mobile_app.py --user luong
```
Script sẽ bóc tách cả 2 file `data/<user_id>/vocab.json` và `clusters.json` (dùng chung) đóng gói chung thành file `mobile/vocab.js`.
File `mobile/index.html` và service worker (`mobile/sw.js`) sau đó có thể được commit lên Github Pages để chạy hoàn toàn Offline bằng Network-First strategy.
