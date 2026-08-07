# CLAUDE.md — English Learning App

## Project Overview
Web app học từ vựng và cụm từ tiếng Anh chuyên nghiệp cho IT professional (B1 → C1).
Hỗ trợ cả chế độ Web PC (Flask Backend đa người dùng) và ứng dụng Offline HTML/Mobile App (PWA).

## Stack & Storage
- **Backend**: Python + Flask dev server (port 5100) — `app.run(debug=False, use_reloader=False, threaded=True)`. Waitress đã bị bỏ vì hung khi chạy qua subprocess trên Windows.
- **Frontend**: Single-page app, vanilla JS, HTML5, modern design
- **Storage**:
  - `data/users.json`: Danh sách người dùng và PIN để xác thực. PIN rỗng (`""`) = user không cần nhập PIN (vd `guest`) — `GET /api/users` trả thêm field dẫn xuất `no_pin: true`, frontend (`showLoginOverlay()`) bỏ qua màn hình nhập PIN và tự login luôn (`doLogin(u.id, '')`) khi click avatar user đó. Thêm user mới: thêm entry vào file này + tạo `data/<id>/tracks.json` (không cần sửa code — màn chọn user và track switcher đều fetch API động, không hardcode danh sách).
  - `data/<user_id>/vocab.json`: Bộ từ vựng **riêng của user đó** (không share) — luong: 1515 thẻ, dùng làm track "IT".
  - `data/<user_id>/tracks.json` (tùy chọn): manifest nhiều **track** (bộ từ vựng độc lập) cho user đó — xem mục "Multi-track vocab" bên dưới. User không có file này coi như chỉ có 1 track ngầm định đọc thẳng `vocab.json`.
  - `data/shared/`: vocab **dùng chung giữa nhiều user** (Common/TOEIC/IELTS) — `vocab_common.json` (1230 từ), `vocab_toeic.json` (1004 từ), `vocab_ielts.json` (933 từ), `vocab_reserve_pool.json` (từ đã rà soát nhưng không thuộc track nào, giữ lại để tái dùng sau, không phải file track active). Xem mục "Multi-track vocab" — field `shared: true` trong track entry quyết định app đọc từ `data/shared/` thay vì `data/<user_id>/`.
  - Hiện tại: Lương có 4 track (`default`="IT" đọc `vocab.json` riêng + `common`/`toeic`/`ielts` đọc từ `data/shared/`); Khánh và Guest mỗi người có 3 track (`common`/`toeic`/`ielts`, đọc từ `data/shared/`). Guest là user demo không cần PIN (xem trên).
  - `data/shared/clusters.json`: 54 cụm từ (Collocation, Grammar, Idiom, tình huống công sở IT) — mỗi cụm có field `"tracks": ["default","toeic",...]` quyết định cụm đó thuộc (những) track nào, lọc bởi `GET /api/clusters` theo `X-Track-Id` hiện tại (giống cơ chế `shared` của vocab). `"default"` = track "IT" của Lương (xem bên dưới). Hiện tại: `default` 42/33 (33 gốc + 6 cụm đời thường của `common` được gắn thêm tag `"default"` + 3 cụm phỏng vấn mới — xem note bên dưới), `toeic` 24, `common` 14, `ielts` 11 (các con số track khác không đổi vì phần thêm mới chỉ target `default`).
  - **Lưu ý cluster dùng chung giữa `default`/`common`**: 8/14 cụm `common` (Spoken Filler Phrases, Showing Agreement, Casual Agreement, Asking for Clarification, Buying Time to Think, "Raise" Collocations, Expressing Importance, Written Transition Words) vốn đã có sẵn tag `"default"` từ trước (dạy chung cho cả 2 track). Ngoài ra, 6 cụm đời thường thuần Common (Small Talk & Greetings, Making Plans/Invitations, Expressing Opinions Everyday, Asking/Giving Directions, Shopping & Bargaining, Apologizing Everyday) được bổ sung thêm tag `"default"` để Lương (chỉ học track IT, không đổi qua track Common) vẫn thấy được nhóm cụm giao tiếp đời thường này cùng lúc — theo yêu cầu "hiện cùng với track IT". Không đổi field `order` vì toàn bộ cụm trong file vốn đã dùng chung 1 dải `order` toàn cục không trùng nhau, nên các cụm thêm sau tự động interleave đúng vị trí khi gộp vào danh sách hiển thị của track `default`.
  - **Cụm phỏng vấn (`interview_common_qa`/`interview_experience`/`interview_logistics`, order 520-540, `tracks:["default"]` only)**: bổ sung sau khi review coverage phát hiện Lương có đủ từ vựng interview (topic "Career & Interview") nhưng thiếu hẳn phrase hội thoại thực tế để trả lời phỏng vấn — 3 cụm mới dạy trả lời câu hỏi thường gặp (giới thiệu bản thân/điểm mạnh/điểm yếu/lý do ứng tuyển/lý do nghỉ việc cũ), mô tả kinh nghiệm theo kiểu STAR, và phần lương bổng/logistics cuối buổi phỏng vấn.
  - `data/shared/patterns.json`: **122 khung câu ngữ pháp** cho tính năng "Luyện Pattern" — **không có field `tracks`, không phân biệt IT/Common gì cả**, dùng chung cho mọi user (chủ yếu Lương học). `GET /api/patterns` trả về toàn bộ. Bao gồm 12 pattern phỏng vấn mới (`pattern_interview_*`, order 1300-1410, vd "I have experience in/with...", "My greatest strength is...", "I'm flexible on..."). Xem chi tiết kiến trúc ở mục "Luyện Pattern" bên dưới (phần 3).
  - `progress.db`: SQLite lưu trạng thái học tập. Khóa chính là `(user_id, key)`, có thêm cột `track_id` (không nằm trong khóa chính, không dùng trong `ON CONFLICT`) để lọc/reset theo từng track. 2 user đọc cùng 1 file shared vẫn có tiến độ hoàn toàn độc lập vì khóa chính có `user_id`.

### Multi-track vocab (Common/TOEIC/IELTS, IT...)
- `data/<user_id>/tracks.json`: `{"tracks": [{"id": "common", "name": "Common", "file": "vocab_common.json", "shared": true}, ...]}`. Không có file này → app dùng track ngầm định `{"id": "default", "file": "vocab.json"}` (giống hệt hành vi cũ, không đổi gì cho user chỉ có 1 track).
- **Field `shared: true`** trên 1 track entry: `load_vocab()`/`create_mobile_app.py`/`add_ipa_distractors.py` sẽ đọc file đó từ `data/shared/<file>` thay vì `data/<user_id>/<file>`. Bỏ field này (hoặc để `false`) = track riêng của user, đọc từ `data/<user_id>/<file>` như trước — đây là cách Lương giữ track "IT" riêng (`vocab.json`, không `shared`) trong khi vẫn dùng chung Common/TOEIC/IELTS với Khánh.
- Lương's track "IT" cố tình giữ `id: "default"` (không đổi thành `"it"`) để tương thích ngược với các dòng `progress` cũ đã có sẵn `track_id='default'` — id chỉ dùng nội bộ, tên hiển thị cho user là "IT".
- Backend (`app/main.py`): `get_tracks(user_id)` / `resolve_track(user_id, track_id)` / `get_track_id()` (đọc header `X-Track-Id`). `load_vocab(user_id, track_id=None)` nhận track_id để chọn đúng file (và đúng thư mục `shared/` hay `<user_id>/`). Endpoint mới `GET /api/tracks`.
- **Bất biến quan trọng khi thêm track mới**: mỗi track phải dùng `key` với prefix riêng biệt không trùng với bất kỳ track/cluster nào khác (kể cả giữa các user khác nhau nếu track đó `shared`) — vd `toeic_...`, `ielts_...` — vì `track_id` KHÔNG nằm trong primary key của `progress`, chỉ có tác dụng lọc, nên 2 track có key trùng nhau (trong cùng user) sẽ bị coi là cùng 1 dòng progress.
- Frontend: biến `activeTrackId` (localStorage `vocabTrackId_<uid>`, **khác hoàn toàn** biến `deck` cũ vốn là filter CEFR B1/B2/C1 — không được nhầm 2 khái niệm này). Header `X-Track-Id` được tự động gắn vào mọi fetch `/api/*` qua interceptor sẵn có. UI chọn track nằm trong Settings ("BỘ TỪ VỰNG"), tự ẩn nếu user chỉ có ≤1 track — theo đúng pattern `buildDifficultyBar()`/`buildDifficultyPopupList()` (dùng chung `#topicPopupOverlay`). Frontend hoàn toàn không quan tâm 1 track có `shared` hay không — đó là chi tiết backend.
- `create_mobile_app.py`: `VOCAB_DATA_MAP` có dạng `{uid: {trackId: [cards]}}` nhưng **CHỈ chứa track riêng của user đó** (vd Lương's `default`) — track `shared:true` (Common/TOEIC/IELTS) load DUY NHẤT 1 lần vào `SHARED_VOCAB_DATA = {trackId: [cards]}` thay vì lặp lại cho từng user (2026-08-06: sửa vì `vocab.js` từng nặng ~20MB do Common/TOEIC/IELTS bị nhân bản y hệt 3 lần cho 3 user dùng chung — giảm còn ~7MB, nội dung xác nhận giống 100% qua so sánh hash trước/sau). `TRACKS_DATA_MAP[uid]` mỗi track có thêm field `shared: true/false` để mock interceptor (`getVocabForTrack(uid, trackId)`) biết tra `SHARED_VOCAB_DATA` hay `VOCAB_DATA_MAP[uid]`. Tương tự, `CLUSTERS_DATA` (đổi từ `CLUSTERS_DATA_MAP`) giờ là mảng phẳng DÙNG CHUNG cho mọi user (cluster vốn không phân biệt theo user, y hệt cách `PATTERNS_DATA` đã làm từ trước) — lọc theo track vẫn làm ở client như cũ (`.filter(c => (c.tracks||[]).includes(trackId))`), chỉ khác nguồn dữ liệu không còn nhân bản. Mock interceptor lưu progress offline theo key `vocab_progress_<uid>_<trackId>` (có migration tự động từ key cũ `vocab_progress_<uid>` nếu phát hiện cài đặt cũ).
- `add_ipa_distractors.py`: `process_user(..., shared=False)` — khi `shared=True` đọc/ghi vào `data/shared/`. `main()` dedupe theo tên file để 1 track shared (đọc bởi nhiều user) chỉ được xử lý 1 lần/lần chạy, không lặp lại theo từng user.
- Nút "Xóa toàn bộ tiến độ" trong Settings chỉ xóa **track đang active** khi user có >1 track (đổi text thành "Xóa tiến độ bộ [Track Name]"); user có đúng 1 track thì hành vi/text giữ nguyên như cũ.
- **Run**: `run.bat` — kiểm tra dependencies, chạy server, mở browser.

## Project Structure
```
ENG/
├── run.bat                  # Chạy server (double-click)
├── progress.db              # SQLite: user_id, key, fav, known, introduced_date, updated_at
├── create_mobile_app.py     # Script build offline PWA cho TẤT CẢ users trong users.json
├── build_mobile.bat         # Wrapper chạy create_mobile_app.py (tham số --user bị ignore)
├── mobile/                  # PWA offline (generated) — dùng cho Github Pages
├── data/
│   ├── users.json           # Cấu hình user: id, pin, name, avatar
│   ├── shared/               # Data dùng chung nhiều user (Common/TOEIC/IELTS + clusters)
│   │   ├── vocab_common.json
│   │   ├── vocab_toeic.json
│   │   ├── vocab_ielts.json
│   │   ├── vocab_reserve_pool.json
│   │   ├── clusters.json    # 51 cụm từ, lọc theo track qua field "tracks"
│   │   └── patterns.json    # 120 khung ngữ pháp (Luyện Pattern), KHÔNG lọc theo track
│   ├── luong/
│   │   ├── vocab.json       # 1500 thẻ IT riêng của Lương (track "IT")
│   │   └── tracks.json      # 4 track: IT (riêng) + Common/TOEIC/IELTS (shared)
│   └── khanh/
│       └── tracks.json      # 3 track: Common/TOEIC/IELTS (shared)
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
  "deck": "B1 | B2 | C1 | C2",
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
- `deck` C1/C2 đã được tách riêng (trước đây gộp chung giá trị `"C1/C2"`, coi là lỗi thiết kế) — mỗi card giờ mang đúng 1 giá trị `C1` hoặc `C2` theo phân loại CEFR thực (C1 = học thuật/chuyên môn nâng cao, C2 = hiếm/văn chương/rất tinh tế), phân bố lệch hẳn về C1 (đa số) là chủ đích, không phải lỗi. Label/filter/badge màu phân biệt rõ C1 và C2, nhưng **độ khó quiz** (`getCardTier()`/`getSmartDistractors()` trong `index.html`) vẫn coi C1 và C2 tương đương (`deck==='C1'||deck==='C2'`) — không có ý định làm C2 khó hơn C1 trong quiz.

### 2. `data/shared/clusters.json` Schema
Mỗi cụm chứa `id`, `name`, `type`, `level`, `topic`, `tip`, `tracks` (mảng track id được phép thấy cụm này, lọc bởi `GET /api/clusters`), `order` (số nguyên, gợi ý thứ tự học — KHÔNG khóa/ẩn cluster nào, chỉ dùng để sắp xếp hiển thị trong `startClusters()` ở `index.html`, thay cho sort alphabet cũ), `dialogue` (mảng hội thoại minh họa `{speaker: "A"|"B", text}`, term trong text được bọc `**...**` để in đậm — render bởi `buildDialogueHTML()`, hiển thị trong `buildBackHTML()` sau phần tip, KHÔNG dùng trong quiz, chỉ minh họa), và mảng `words` (mỗi từ có `term`/`level`/`vi`/`pron`/`register`/`example`/`note`/`situation`).

### 3. `data/shared/patterns.json` Schema — tính năng "Luyện Pattern"
Khác với vocab (từ đơn cố định) và cluster (chọn đúng cụm theo tình huống), **pattern dạy khung ngữ pháp có chỗ trống** (`give sb sth`, `blocked by [X]`) để tự tạo câu — kỹ năng cần cho giao tiếp thực tế. Mỗi pattern chứa `id`, `frame`, `vi_frame`, `level`, `order`, `note` (mẹo ngữ pháp/lỗi thường gặp, tiếng Việt), `alt_frame` (optional, cấu trúc thay thế **CÙNG nghĩa**, vd `give sb sth` ↔ `give sth to sb`), `confusable_with` (optional, id của pattern **KHÁC nghĩa** dễ nhầm — vd `stop to V` vs `stop doing sth` — KHÔNG được lẫn với `alt_frame` vì 2 khái niệm ngược nhau: alt_frame = tương đương, confusable_with = trông giống nhưng nghĩa khác hẳn), `common_slots` (optional, object map gợi ý từ điền vào chỗ trống, dùng làm nút "Gợi ý" ở Production), `examples[]` (`{en, vi}`, dùng cho cả Input lẫn Shadowing), `dialogue[]` (optional, giống cluster), `production_prompts[]` (`{situation_vi, sample_answer}`, cần ≥2 để đỡ lặp khi ôn lại). **KHÔNG có field `tracks`** — pattern không phân biệt track/user, xem note bên dưới.
- **`pickProductionPrompt(p)` cache theo `patternProdCache = {patternId: prompt}` (2026-08-07)**: chọn ngẫu nhiên 1 phần tử `production_prompts` NGAY LẦN GỌI ĐẦU cho pattern đó, cache lại — các lần gọi sau (vd re-render khi bấm "Xem câu mẫu": `patternProdRevealed = true; renderPatternPhase();`) trả về ĐÚNG prompt đã chọn, không bốc lại ngẫu nhiên. Nếu không cache, tình huống hiện trước khi bấm reveal và câu mẫu hiện sau khi bấm reveal có thể thuộc 2 phần tử `production_prompts` khác nhau — gây nhầm lẫn thật cho người học. Cache reset về `null` ở đúng 5 điểm chuyển sang pattern/unit khác (`startPatternLearn()`'s khởi tạo phiên, nút Prev/Next/Skip, và sau khi tự đánh giá "Đã ổn"/"Cần ôn thêm") — nghĩa là tình huống VẪN được bốc ngẫu nhiên mới mỗi lần học lại pattern đó ở phiên sau (giữ đúng ý đồ gốc "cần ≥2 để đỡ lặp khi ôn lại"), chỉ ổn định trong PHẠM VI 1 lượt xem hiện tại.
- **UI**: Pattern-Học là 1 trong 3 ô của `#learnHome` (tab "Học", `data-learn="pattern"`, `mode='pattern'`); Pattern-Làm bài tập là 1 trong 4 ô của `#practiceHome` (tab "Ôn luyện", `data-practice="pattern"`) — 2 flow này KHÔNG còn chung 1 pane chọn nữa (xem note "Điều hướng 2 nhóm Học/Ôn luyện" ở mục Frontend Key Patterns), mỗi flow vào thẳng từ tab tương ứng.
  - **Học** (`startPatternLearn()`/`renderPatternPhase()`): `groupPatternUnits()` gộp trước danh sách pattern đã sort theo `order` thành các **unit** — 1 pattern thường (`type:'single'`) hoặc 1 cặp `confusable_with` gộp chung (`type:'pair'`, học SO SÁNH trực tiếp trong CÙNG 1 thẻ thay vì học nối tiếp 2 thẻ riêng). Mỗi unit đi qua 3 bước: Input (`buildPatternInputHTML`/`...Single`) → Shadowing (`buildPatternShadowHTML`/`...Single`) → Production (`buildPatternProductionHTML`/`...Single`, tình huống tiếng Việt → tự thử → lật xem câu mẫu → tự đánh giá "Đã ổn"/"Cần ôn thêm"). Khi unit là `pair`, cả 2 phía hiển thị dạng khối màu xếp chồng (`.pattern-compare-block.side-a`/`.side-b`, xanh dương vs cam) ngăn cách bởi divider "VS", và nút tự đánh giá ghi `/api/known`+`/api/introduce` cho **cả 2** pattern id trong unit cùng lúc.
  - **Làm bài tập** (`startPatternQuiz()`/`buildPatQuestions()`): trắc nghiệm có chấm điểm, câu hỏi sinh **động lúc chạy** (không lưu sẵn). 3 loại câu hỏi: (1) điền từ đầu khung (`patFrameHeadWord()` bỏ qua stopword như it/could/you), nhiễu lấy từ khung của pattern khác — **bị SKIP nếu có `confusable_with`** vì 2 pattern trong 1 cặp dễ nhầm luôn chung head word (vd cả `stop to V` và `stop doing sth` đều có head word "stop", điền từ không phân biệt được 2 nghĩa); (2) nếu có `alt_frame`, hỏi "cách viết nào tương đương"; (3) nếu có `confusable_with`, hỏi "khung câu nào đúng nghĩa" với chính pattern dễ nhầm làm nhiễu sắc nét nhất (khác nhiễu ngẫu nhiên của 2 loại câu kia). Sai thì hiện `note` làm giải thích.
  - **Bộ lọc phạm vi "So sánh to-V/V-ing"**: `patternScopeFilter` (`'all'`|`'compare'`) + `getFilteredPatternData()` lọc `p.confusable_with` trước khi đưa vào cả Học lẫn Làm bài tập — tái dùng y hệt cơ chế `clusterTypeFilter`/`buildClusterTypeBar()` của Cluster (nút `.btn-topic-trigger` trong `#topicBar` mở `#topicPopupOverlay` có sẵn, KHÔNG thêm CSS mới). `buildPatternScopeBar()` tự ẩn hẳn nút filter nếu KHÔNG có pattern nào mang `confusable_with` trong toàn bộ dữ liệu (trên thực tế luôn có, nên nút này luôn hiện).
- **Pattern hoàn toàn không có khái niệm track/user riêng** — `GET /api/patterns` trả về **TOÀN BỘ** `patterns.json` cho MỌI user, field `tracks` đã bị **xóa hẳn khỏi schema** (không chỉ vestigial như trước — đã dọn sạch vì user xác nhận không cần phân biệt IT/Common gì nữa, chủ yếu Lương học tính năng này). Mobile (`create_mobile_app.py`) dùng 1 hằng số `PATTERNS_DATA` load DUY NHẤT 1 lần (không phải `..._MAP` per-user như vocab/cluster) vì nội dung giống hệt nhau cho mọi user.
- Nội dung hiện tại: **122 pattern** dùng chung cho mọi user, không còn phân biệt "IT-flavored" hay "Common-flavored" — gồm 12 pattern cơ bản (`order` 10-120), 4 cặp `confusable_with` gốc `stop`/`remember-forget`/`try`/`regret` (`order` 130-200, ví dụ IT-flavored — bản canonical duy nhất, xem note dedup bên dưới), 15 cặp `confusable_with` khác không trùng lặp (30 pattern, id prefix `pattern_common_...` chỉ còn ý nghĩa lịch sử về nguồn gốc, không còn ý nghĩa phân loại track: `mean`/`like`/`love`/`hate`/`prefer`/`go on`/`need`/`can't bear`/`can't stand`/`start`/`continue`/`used to`/`dread`/`propose`/`deserve`), 60 pattern thường theo 8 chủ đề đời thường (yêu cầu/đề nghị, xin lỗi/than phiền, lịch hẹn, mua sắm, sức khỏe, du lịch, xã giao, quan điểm/đồng ý-phản đối), và 12 pattern phỏng vấn (`pattern_interview_...`, `order` 1300-1410).
- **Dedup lịch sử (2026-08-06)**: pattern gốc từng có 2 bản riêng biệt cho 4 động từ `stop`/`remember`/`forget`/`try`/`regret` — 1 bản ví dụ IT-flavored (`pattern_stop_to_v`...) và 1 bản ví dụ đời thường (`pattern_common_stop_to_v`...), do lịch sử "pattern từng gate theo track" để lại. Điều này gây bug thật: 2 pattern khác `id` nhưng CÙNG `frame` text y hệt nhau (vd cả 2 đều là `"stop to V"`) lọt vào cùng 1 pool ở chế độ "So sánh to-V/V-ing", khiến `buildPatQuestions()`'s câu hỏi `confuse` đôi khi sinh 2 option trùng chữ (nhiễu chọn ngẫu nhiên không dedupe theo text). Đã xóa 10 pattern Common trùng lặp (giữ lại bản IT-flavored làm canonical duy nhất), vừa sửa dứt điểm bug vừa khớp yêu cầu "dùng chung hết, không chia Common/IT" của user — không renumber lại `order` các pattern còn lại (giữ nguyên giá trị cũ, có khoảng trống không sao vì chỉ dùng để sort).

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
- **Swipe Flashcard = thuần điều hướng + hiệu ứng trượt (2026-08-07, đổi từ bản đầu)**: vuốt trái/phải trên `#cardWrap` gọi thẳng `.click()` lên `#btnNavNext`/`#btnNavPrev` có sẵn (trái→Next, phải→Prev) — KHÔNG đánh dấu biết/chưa biết, hoạt động bất kể thẻ đã lật hay chưa. Bản đầu tiên từng làm kiểu "Tinder-swipe" (chỉ hoạt động sau khi lật, phải→Nhớ rồi/trái→Cần ôn qua `markCard()`) nhưng user phản hồi hành vi này phản trực giác ("vuốt để chuyển thẻ sao lại liên quan đánh dấu"), nên đổi hẳn sang thuần điều hướng.
  - `navigateFlash(dir)` (hàm chung mới, thay logic inline cũ ở `btnNavPrev`/`btnNavNext` click handler) — kiểm tra `btn.disabled` trước (thừa hưởng miễn phí giới hạn đầu/cuối danh sách, không cần duplicate check `flashIdx===0`/`>=length-1`), đổi `flashIdx`, `renderFlash()`, rồi áp class `.slide-in-left`/`.slide-in-right` lên `#cardWrap` để tạo hiệu ứng trượt nhẹ (CSS `@keyframes cardSlideInLeft/Right`, dùng `transform`+`opacity`, KHÔNG dùng chung transform với hiệu ứng lật của `.card` vì áp lên phần tử cha `#cardWrap` khác `.card`, tránh xung đột transform giữa 2 hiệu ứng). Vì vuốt gọi `.click()` lên nút Next/Prev, hiệu ứng tự động áp dụng cho CẢ vuốt lẫn bấm nút mà không cần sửa gì thêm ở phần vuốt.
  - `void wrap.offsetWidth;` (force reflow) trước khi add lại class animation — cần thiết vì CSS `animation` (khác `transition`) không tự restart nếu class tên giống nhau được add liên tiếp mà không có 1 nhịp "gỡ ra rồi thêm lại" ở giữa — quan trọng khi bấm Next/Prev hoặc vuốt liên tục cùng hướng.
- **Mode-guard sau `await` cho `ensureClusterData()`/`ensurePatternData()` (2026-08-07)**: `activateClusters()`, `startPatternLearn()`, `startPatternQuiz()`, và 2 closure `.then()` trong `#quizSection`'s click handler (nhánh `cluster_pane`/`cqFilterBtn`) — TẤT CẢ đều check lại `mode`/`practiceSubMode` NGAY SAU khi `await`/`.then()` xong, TRƯỚC khi gọi các hàm ghi vào `#topicBar`/`#deckBar` (element DÙNG CHUNG giữa Cluster và Pattern). Lý do: `_clusterPromise`/`_patternPromise` chỉ chống race khi ĐỔI USER (qua `_userGen`), KHÔNG chống được race khi user chuyển tab (Cluster↔Pattern) nhanh lúc mạng chậm — nếu không có guard này, dữ liệu của tab đã RỜI ĐI có thể ghi đè UI của tab đang XEM. Pattern chung: lưu giá trị `mode`/`practiceSubMode` mong đợi trước khi `await`, so sánh lại sau khi resolve, `return` sớm nếu khác — tương tự tinh thần `myGen === _userGen` đã dùng cho case đổi user, chỉ khác là so `mode` thay vì `_userGen`.
- **Điều hướng 2 nhóm "Học" / "Ôn luyện" (2026-08-06)**: `#modeSel` chỉ còn 2 nút (`data-section="learn"|"review"`, KHÔNG còn 3 nút phẳng Clusters/Flashcard/Practice như trước) — theo yêu cầu user tách rõ "học nội dung mới" khỏi "ôn luyện/kiểm tra", vì trước đó Pattern lại vừa Học vừa Làm bài tập chung trong tab Practice, phá vỡ quy ước ngầm Cluster+Flashcard=Học / Quiz+Phát âm=Ôn luyện.
  - `mode` giờ có 5 giá trị: `'learn_home'` (màn hình chọn của nhóm Học, 3 ô Flashcard/Cluster/Pattern, tương tự `#practiceHome` bên Ôn luyện), `'flash'`/`'cluster'` (giữ nguyên ý nghĩa cũ, chỉ đổi cách vào — qua ô trong `#learnHome` thay vì tab phẳng), `'pattern'` (MỚI — Pattern-Học, trước đây là `practiceSubMode==='pattern_learn'` lồng trong `mode==='quiz'`, giờ tách thành mode top-level riêng), `'quiz'` (giữ nguyên, giờ CHỈ còn Trắc nghiệm Từ vựng/Cụm từ/Phát âm/Pattern — Pattern-Học đã dời sang mode `'pattern'`).
  - `#learnSection` (mới, chứa `#learnHome` + `#flashSection` + `#clusterSection` + `#patternLearnArea`/`#patternLearnResult` — cả 3 đều move vào đây) và `#quizSection` (giữ nguyên tên, chứa `#practiceHome` + `#quizArea` + `#clusterPracticePane`/`#clusterQuizArea` + `#patternQuizArea` — đã bỏ `#patternPracticePane`, không còn choice "Học vs Làm bài tập" vì giờ 2 flow này vào từ 2 tab khác nhau) là 2 container top-level, `#modeSel` click handler toggle hidden giữa 2 cái này thay vì 3 section cũ.
  - `showLearnHome()` (mới, mirror `showPracticeHome()`) và `goBackHome()` (mới — `mode==='quiz' ? showPracticeHome() : showLearnHome()`, dùng chung cho MỌI nút "Về chọn môn" thay vì hardcode `showPracticeHome()`) — nút back giờ cũng hiện ở Flashcard/Cluster (trước đây luôn ẩn vì 2 mode này từng là tab gốc, không có "về đâu").
  - Mặc định mở app vẫn vào thẳng `mode='flash'` (KHÔNG qua màn `#learnHome`) — giữ nguyên trải nghiệm cũ (thao tác hằng ngày quan trọng nhất không bị thêm bước); bấm lại tab "Học" khi đang ở Flashcard/Cluster/Pattern mới về `#learnHome` (hành vi mới: bấm tab đang active = reset về home của nhóm đó, khác hành vi cũ là no-op khi bấm lại tab đang active).
  - `applyTabOnlyClasses()` (mới, tách ra từ vòng lặp cũ nằm trong tab-switch handler) — gọi lại mỗi khi `mode` đổi giá trị (ở `showLearnHome()`, `showPracticeHome()`, và cả 3 nhánh trong `#learnSection`'s click handler) để cập nhật `.tab-only-*`.
- **Tab-specific elements**: dùng class `tab-only-flash`, `tab-only-quiz`, `tab-only-cluster`, `tab-only-pattern`, `tab-only-learn_home` — `applyTabOnlyClasses()` tự discover qua `querySelectorAll` (hiện tại chỉ `tab-only-flash` có phần tử dùng thật — `#quickStatsBar`).
- **Checklist học daily (`#checklistOverlay`, icon `#btnOpenChecklist` cạnh nút Cài đặt, 2026-08-06)**: KHÔNG phải widget luôn hiện (đã đổi từ bản đầu) — 1 icon nhỏ trong header (kèm badge số "X/3") mở popup khi bấm, popup liệt kê đúng 3 mục cần đạt mỗi ngày để đủ ~30 phút học: **Flashcard** (học đủ `dailyNew` từ mới, mặc định 10) + 1 mục **Học** xoay vòng (Cluster/Pattern) + 1 mục **Ôn luyện** xoay vòng (Trắc nghiệm Từ vựng/Cụm từ/Pattern, Luyện Phát âm) — bảng xoay vòng cố định `WEEKDAY_PLAN[Date.getDay()]` (0=CN→6=T7, xem index.html để biết đúng ngày nào ứng với mục gì). Bấm vào 1 mục trong popup tự điều hướng thẳng tới đúng màn (bắn `.click()` lên đúng nút tab + tile).
  - **Cả 2 mục "Flashcard" và "Học" (Cluster/Pattern) đều tính SỐNG (live), KHÔNG dùng localStorage** — `isFlashDoneToday()` = `newIntroduced >= dailyNew`; `countLearnedToday(key)` đếm số phần tử trong `clusterData`/`patternData` (tuỳ `todayPlan().learn.key`) có `introduced_date === hôm nay`, cần đạt `LEARN_TARGET = 3`. Cả 2 đều đọc dữ liệu **progress.db đã sync PC↔mobile** (`introduced_date` set qua `/api/introduce`, gọi từ `openClusterBack()`/pattern rate handler — cả 2 đều tự cập nhật LOCAL field `introduced_date` ngay lập tức trước khi gọi API, giống hệt cơ chế `introduceCard()` của vocab, để đếm sống không bị trễ 1 nhịp fetch). Vì `clusterData`/`patternData` chỉ fetch lười (lazy) khi user thực sự mở tab đó trong phiên, `renderChecklistBadge()`/`renderChecklistPopup()` phải **`await ensureLearnDataForToday()`** trước khi đếm — nếu không sẽ báo thiếu (0/3) chỉ vì user chưa mở tab đó trong phiên hiện tại dù đã học đủ từ trước (trên máy khác hoặc phiên trước cùng ngày).
  - **Chỉ mục "Ôn luyện" (hoàn thành 1 lượt trắc nghiệm) còn cần `localStorage['dailyChecklist_<uid>'] = {date, review}`, cố tình KHÔNG sync PC↔mobile** — vì đây là 1 SỰ KIỆN (hoàn thành 1 lượt) chứ không phải đại lượng tính lại được từ progress.db, và các loại trắc nghiệm cũng không phân biệt được với nhau qua progress.db (cùng ghi `/api/known`). Set tại đúng điểm mỗi hàm `renderXxxQuiz()` đến nhánh hiện màn "Kết quả" (`quizIdx>=quizCards.length` v.v.), gate theo `todayPlan().review.key` khớp đúng mục hôm nay.
  - **3 tiêu chí "xong" khác nhau theo loại** (chốt qua AskUserQuestion sau khi user chê bản đầu "chỉ cần mở màn hình là tính xong" không đồng nhất với Flashcard): Flashcard = số lượng thật (`dailyNew`); Học (Cluster/Pattern) = số lượng thật nhưng ngưỡng nhỏ hơn hẳn (`LEARN_TARGET=3`, vì có tới 42 cụm/122 pattern, học hết 1 buổi phi thực tế); Ôn luyện = hoàn thành trọn 1 lượt quiz (điểm dừng tự nhiên có sẵn trong code, không cần đếm số câu riêng).
  - **Badge số phải re-render SAU KHI `newIntroduced` được server trả về** (`renderChecklistBadge()` gọi lại bên trong `_fetchAndRender()` ngay sau dòng gán `newIntroduced = data.today_introduced`), KHÔNG chỉ gọi 1 lần lúc đầu `loadCards()` — đây là bug cùng dạng "quên đường vào ngầm định/boot path" đã gặp nhiều lần trong cùng phiên làm việc (xem `mem:project-nav-hoc-onluyen-split`, `mem:project-daily-checklist-widget`) — bắt được ở self-review trước khi user kịp thấy.
- **Flash stats**: `sessionMarks = new Map()` lưu mark cuối cùng mỗi thẻ → `knownCount()`/`unknownCount()` là functions (tránh double-count khi mark lại).
- **Toast**: `showToast(msg, type)` — hiện bottom toast, tự ẩn sau 3s.
- **quickStatsBar**: hiện "Đã thuộc X/total + Streak N ngày" chỉ ở tab Flash Card.
- **cardFilter**: `'all'` | `'unknown'` (chưa thuộc, hiển thị "Review Needed") | `'new'` | `'known'` — reset về `'new'` mỗi lần `loadCards()` (ưu tiên học từ mới trước, không phải `'all'`). `trySwitchToReview()` trong `renderFlash()`: khi filter đang `'new'` mà hết thẻ (dù ngay từ đầu do hôm nay không có từ mới, hay học hết giữa chừng) → tự chuyển sang `'unknown'` kèm toast, gọi lại `startSession()`. Guard bằng check `cardFilter !== 'new'` nên không lặp vô hạn nếu `'unknown'` cũng rỗng (khi đó hiện màn "Xong rồi!"/"Không có thẻ nào" bình thường). `resetVocabFilters()` ("Xóa bộ lọc") vẫn về `'all'` như cũ — đây là hành động rõ ràng muốn bỏ hết filter, không nên quay lại `'new'`.
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

