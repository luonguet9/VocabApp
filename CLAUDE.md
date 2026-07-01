# CLAUDE.md — English Learning App

## Project Overview
Web app học từ vựng tiếng Anh cho IT professional người Việt (A2 → B2+).
Daily learning: ôn từ cũ + học từ mới mỗi ngày.

## Stack
- **Backend**: Python + Flask + Waitress (port 5100)
- **Frontend**: Single-page app, vanilla JS, mobile-first
- **Storage**: `vocab.csv` (từ vựng, read-only), `progress.db` (SQLite, user state)
- **Run**: `run.bat` — tự kill port cũ, check dependencies, mở browser

## Project Structure
```
ENG/
├── run.bat                  # Chạy server (double-click)
├── vocab.csv                # 1075 từ: B1(651) + B2(262) + C1(162)
├── progress.db              # SQLite: fav, known, introduced_date
├── app/
│   ├── main.py              # Flask server, tất cả API endpoints
│   └── templates/
│       └── index.html       # Toàn bộ frontend (HTML + CSS + JS)
├── tools/
│   ├── gen_vocab.py         # Generate từ vựng bằng Claude Haiku API
│   ├── update_pron.py       # Cập nhật IPA từ Free Dictionary API (không cần API key)
│   ├── add_vocab.py         # Script thêm từ thủ công
│   └── anki_gen.py          # Export sang Anki .apkg
└── docs/                    # Roadmap, tài liệu học
```

## vocab.csv Format
Tab-separated, 4 columns:
```
TERM  (example sentence)\tVietnamese meaning  |  AmE /ipa/  BrE /ipa/\ttopic\tlevel
```
- **col 0**: `TERM  (example)` — example trong ngoặc tròn, optional
- **col 1**: `Vietnamese meaning  |  pronunciation` — `|` phân cách nghĩa và IPA
- **col 2**: topic — `Tech`, `Vocabulary`, `Meetings`, `Slack`, `Business`, `Discussion`, `Idioms`, `Phrases`, `C1`
- **col 3**: level — `B1`, `B2`, `C1`

IPA format trong col 1:
- US = UK: `🇺🇸 🇬🇧 /ipa/`
- Khác nhau: `🇺🇸 /us-ipa/  🇬🇧 /uk-ipa/` (2+ spaces giữa)

## progress.db Schema
```sql
CREATE TABLE progress (
    key             TEXT PRIMARY KEY,  -- = col 0 của vocab.csv (cả phần ví dụ)
    fav             INTEGER DEFAULT 0,
    known           INTEGER DEFAULT 0,
    introduced_date TEXT               -- ISO date, set khi user lật thẻ lần đầu
)
```

## API Endpoints (main.py)
| Endpoint | Method | Mô tả |
|----------|--------|--------|
| `/` | GET | Serve index.html |
| `/api/start-day` | POST | `{new: N}` → trả cards (introduced + N pending mới) |
| `/api/introduce` | POST | `{key}` → set introduced_date = today (COALESCE, không overwrite) |
| `/api/fav` | POST | `{key, fav}` → UPSERT fav |
| `/api/known` | POST | `{key, known}` → UPSERT known |
| `/api/history` | GET | Group từ đã học theo ngày |
| `/api/reset` | POST | Xóa toàn bộ progress |

## Frontend State (index.html)
```javascript
let allCards = [], sessionCards = [];
let deck = 'all', mode = 'flash', topic = 'all';
let filterUnknown = false;
let dailyNew = parseInt(localStorage.getItem('vocabDailyNew') || '10');
let extraNew = 0;  // tăng khi bấm "Học thêm"
let reviewCount = 0, newServed = 0, newIntroduced = 0;
```

## Key Logic

### Daily learning flow
1. `loadCards()` → reset extraNew/deck/topic → `_fetchAndRender(dailyNew)`
2. Server trả: all introduced cards + N pending mới (is_new=true)
3. User lật thẻ → `introduceCard()` → POST `/api/introduce` → `newIntroduced++`
4. Kết quả: nút **🔄 Học lại** (ôn lại) + **📚 Học thêm N từ** (load thêm)

### Pronunciation display
- `parsePron(pron)` → `{us, uk}` — bỏ qua old format (không có 🇺🇸/🇬🇧), filter IPA partial (`/-x/`)
- `renderPronHTML()` → `AmE /ipa/ 🔊` / `BrE /ipa/ 🔊` trên 2 dòng
- Click 🔊 → `speak(term, accent)` dùng Web Speech API

### Introduce card
- Triggered khi user **lật thẻ** (`flipCard`) hoặc chọn đáp án quiz (`renderQuiz`)
- `introduced_date` chỉ set 1 lần (SQL `COALESCE`)

## Tools

### update_pron.py
Cập nhật IPA cho tất cả từ trong vocab.csv:
```bash
python tools/update_pron.py        # update in-place
python tools/update_pron.py --dry  # preview only
```
- Dùng Free Dictionary API (`dictionaryapi.dev`) — không cần API key
- Cần `User-Agent: Mozilla/5.0` header (không thì bị 403)
- 0.3s delay giữa các request
- Bỏ qua phrases, acronyms (SKIP là đúng, không phải lỗi)

### gen_vocab.py
Generate từ vựng bằng Claude Haiku — **cần ANTHROPIC_API_KEY**:
```bash
python tools/gen_vocab.py        # generate & append to vocab.csv
python tools/gen_vocab.py --dry  # preview
```
- Word list nằm trong `B1_WORDS`, `B2_WORDS` trong file
- Tự động bỏ qua từ đã có trong CSV

## Không có ANTHROPIC_API_KEY
Môi trường corporate network — API key không có sẵn. Nếu cần generate từ vựng:
- Dùng agent/Claude trực tiếp generate content → write thẳng vào `vocab.csv`
- Sau đó chạy `update_pron.py` để thêm IPA

## Known Limitations
- ~488/1075 entries không có IPA (phrases, acronyms) — đúng thiết kế
- `add_vocab_batch.py` là single-use script từ lần generate gần nhất — có thể xóa
- `tools/add_vocab.py` — helper script thêm từ thủ công

