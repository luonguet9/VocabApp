// Auto-generated from clusters.json
const CLUSTER_DATA = {
  "clusters": [
    {
      "id": "syn_schedule",
      "type": "synonym",
      "subtype": null,
      "name": "Arranging a Meeting",
      "level": "B2",
      "topic": "Meetings",
      "tip": "schedule/arrange → formal email; set up → Slack/chat; pencil in → tạm thời, có thể thay đổi sau",
      "words": [
        {
          "term": "schedule",
          "level": "B1",
          "vi": "lên lịch, đặt lịch",
          "pron": "🇺🇸 🇬🇧 /ˈʃɛdjuːl/",
          "register": "formal",
          "example": "Let's schedule the sprint review for Friday at 2 PM.",
          "note": "Default trong corporate email/calendar invite",
          "situation": "Bạn cần gửi calendar invite formal cho client để đề xuất thời gian họp kỹ thuật."
        },
        {
          "term": "arrange",
          "level": "B1",
          "vi": "sắp xếp, bố trí",
          "pron": "🇺🇸 🇬🇧 /əˈreɪndʒ/",
          "register": "neutral",
          "example": "Can you arrange a call with the client this week?",
          "note": "Versatile — dùng được cả viết lẫn nói",
          "situation": "Trong cuộc gọi team, bạn cần tổ chức một call với BA và dev để align requirements."
        },
        {
          "term": "set up",
          "level": "B1",
          "vi": "đặt lịch (thông thường)",
          "pron": "🇺🇸 🇬🇧 /sɛt ʌp/",
          "register": "casual",
          "example": "Hey, let's set up a quick sync tomorrow morning.",
          "note": "Phù hợp Slack, chat — tránh dùng trong formal email",
          "wrong_usage": "❌ 'setup a meeting' — setup là danh từ/tính từ, không phải động từ",
          "situation": "Trên Slack, bạn nhắn đồng nghiệp để đặt một quick sync về bug cần fix gấp."
        },
        {
          "term": "pencil in",
          "level": "B2",
          "vi": "đặt lịch tạm thời (có thể thay đổi)",
          "pron": "🇺🇸 🇬🇧 /ˈpɛnsəl ɪn/",
          "register": "casual",
          "example": "I'll pencil you in for Thursday — let me confirm later.",
          "note": "Ngụ ý 'chưa chắc chắn', có thể reschedule",
          "situation": "Bạn và manager chưa chắc về lịch, muốn giữ một slot trước nhưng sẽ confirm sau."
        }
      ],
      "vi_name": "Sắp xếp lịch họp"
    },
    {
      "id": "syn_agree",
      "type": "synonym",
      "subtype": null,
      "name": "Showing Agreement",
      "level": "B2",
      "topic": "Meetings",
      "tip": "agree/concur → formal meeting; buy into → ủng hộ về tư tưởng; get behind → nhiệt tình hậu thuẫn",
      "words": [
        {
          "term": "agree",
          "level": "B1",
          "vi": "đồng ý, nhất trí",
          "pron": "🇺🇸 🇬🇧 /əˈɡriː/",
          "register": "neutral",
          "example": "I agree with your assessment of the timeline.",
          "note": "Universal — dùng được mọi context",
          "situation": "Trong meeting, bạn muốn xác nhận đồng ý với timeline mà PM đề xuất."
        },
        {
          "term": "concur",
          "level": "B2",
          "vi": "đồng thuận (formal)",
          "pron": "🇺🇸 🇬🇧 /kənˈkɜːr/",
          "register": "formal",
          "example": "I concur — we should delay the release until testing is complete.",
          "note": "Rất formal, phù hợp executive meetings và written docs",
          "situation": "Bạn là senior engineer viết vào decision log để ghi nhận sự đồng thuận về technical approach."
        },
        {
          "term": "buy into",
          "level": "B2",
          "vi": "ủng hộ, chấp nhận (một ý tưởng)",
          "pron": "🇺🇸 🇬🇧 /baɪ ˈɪntə/",
          "register": "casual",
          "example": "I'm fully buying into this approach — let's move forward.",
          "note": "Nhấn mạnh sự tin tưởng vào ý tưởng, không chỉ là đồng ý",
          "situation": "Sau khi nghe pitch về microservices migration, bạn thực sự tin tưởng vào approach này."
        },
        {
          "term": "get behind",
          "level": "B2",
          "vi": "hậu thuẫn, đứng sau ủng hộ",
          "pron": "🇺🇸 🇬🇧 /ɡɛt bɪˈhaɪnd/",
          "register": "casual",
          "example": "I can really get behind this proposal.",
          "note": "Mang tính enthusiasm cao hơn 'agree' đơn thuần",
          "situation": "Team đang thảo luận về đổi sang TypeScript, bạn muốn thể hiện sự ủng hộ nhiệt tình."
        }
      ],
      "vi_name": "Thể hiện sự đồng ý"
    },
    {
      "id": "syn_disagree",
      "type": "synonym",
      "subtype": null,
      "name": "Disagreeing Professionally",
      "level": "C1",
      "topic": "Meetings",
      "tip": "Luôn disagree về vấn đề, không phải con người. push back < challenge < object (tăng dần độ mạnh)",
      "words": [
        {
          "term": "push back",
          "level": "B2",
          "vi": "phản đối, phản biện (nhẹ nhàng)",
          "pron": "🇺🇸 🇬🇧 /pʊʃ bæk/",
          "register": "neutral",
          "example": "I want to push back on that estimate — two weeks seems too optimistic.",
          "note": "Phổ biến nhất trong tech/startup culture",
          "situation": "Trong sprint planning, bạn thấy estimate 2 tuần là quá lạc quan, muốn phản biện nhẹ nhàng."
        },
        {
          "term": "challenge",
          "level": "B2",
          "vi": "đặt câu hỏi, phản biện",
          "pron": "🇺🇸 🇬🇧 /ˈtʃælɪndʒ/",
          "register": "neutral",
          "example": "I'd like to challenge the assumption that users want this feature.",
          "note": "challenge + assumption/claim — phổ biến trong data-driven discussions",
          "situation": "Team đang assume users muốn feature mới — bạn muốn đặt câu hỏi về assumption đó."
        },
        {
          "term": "raise concerns",
          "level": "B2",
          "vi": "nêu lên lo ngại",
          "pron": "",
          "register": "formal",
          "example": "I need to raise some concerns about the security model.",
          "note": "Lịch sự nhất — không trực tiếp nói 'bạn sai'",
          "situation": "Bạn có lo ngại về security model mới nhưng muốn nêu lên một cách chuyên nghiệp nhất."
        },
        {
          "term": "beg to differ",
          "level": "C1",
          "vi": "không đồng ý (formal, lịch sự)",
          "pron": "🇺🇸 🇬🇧 /bɛɡ tə ˈdɪfər/",
          "register": "formal",
          "example": "I beg to differ — the data tells a different story.",
          "note": "Rất formal/polite, thường trong executive context",
          "situation": "Trong executive meeting, Director đưa kết luận dựa trên data sai — bạn cần phản bác lịch sự và formal."
        }
      ],
      "vi_name": "Phản đối chuyên nghiệp"
    },
    {
      "id": "syn_emphasize",
      "type": "synonym",
      "subtype": null,
      "name": "Emphasizing a Point",
      "level": "C1",
      "topic": "Discussion",
      "tip": "highlight → có data/document để point to; underscore → viết; drive home → spoken, mang tính urgency cao",
      "words": [
        {
          "term": "emphasize",
          "level": "B1",
          "vi": "nhấn mạnh",
          "pron": "🇺🇸 🇬🇧 /ˈɛmfəsaɪz/",
          "register": "neutral",
          "example": "I want to emphasize that this deadline is non-negotiable.",
          "note": "General-purpose, phù hợp mọi context",
          "situation": "Trong standup, bạn muốn đảm bảo toàn team hiểu rằng deadline này không thể dời."
        },
        {
          "term": "highlight",
          "level": "B1",
          "vi": "nêu bật, làm nổi bật",
          "pron": "🇺🇸 🇬🇧 /ˈhaɪlaɪt/",
          "register": "neutral",
          "example": "The report highlights three critical bottlenecks.",
          "note": "Thường dùng khi có data/document để point to",
          "situation": "Khi trình bày performance report, bạn muốn chỉ ra 3 bottleneck quan trọng nhất trong data."
        },
        {
          "term": "underscore",
          "level": "B2",
          "vi": "nhấn mạnh (trong văn bản)",
          "pron": "🇺🇸 🇬🇧 /ˌʌndərˈskɔːr/",
          "register": "formal",
          "example": "This incident underscores the need for better monitoring.",
          "note": "Phổ biến trong technical writing và post-mortems",
          "situation": "Trong post-mortem document sau outage, bạn muốn nhấn mạnh tầm quan trọng của monitoring."
        },
        {
          "term": "drive home",
          "level": "C1",
          "vi": "nhấn mạnh để người nghe thực sự hiểu",
          "pron": "🇺🇸 🇬🇧 /draɪv hoʊm/",
          "register": "casual",
          "example": "Let me drive this home: if we miss the launch date, we lose the contract.",
          "note": "Mang tính urgency cao — dùng khi stakeholders chưa thực sự nắm vấn đề",
          "situation": "Stakeholders vẫn chưa hiểu mức độ nghiêm trọng của security gap — cần nói mạnh và rõ hơn."
        }
      ],
      "vi_name": "Nhấn mạnh quan điểm"
    },
    {
      "id": "syn_clarify",
      "type": "synonym",
      "subtype": null,
      "name": "Asking for Clarification",
      "level": "B2",
      "topic": "Meetings",
      "tip": "clarify → có sự mơ hồ; elaborate → cần thêm chi tiết; unpack → complex/abstract concept; walk through → hướng dẫn từng bước",
      "words": [
        {
          "term": "clarify",
          "level": "B1",
          "vi": "làm rõ, giải thích",
          "pron": "🇺🇸 🇬🇧 /ˈklærɪfaɪ/",
          "register": "neutral",
          "example": "Could you clarify what you mean by 'good enough'?",
          "note": "Dùng khi có sự mơ hồ, một câu có thể hiểu nhiều cách",
          "situation": "PM dùng từ 'done' mơ hồ — bạn không chắc ý họ là dev done hay QA passed."
        },
        {
          "term": "elaborate",
          "level": "B2",
          "vi": "trình bày chi tiết hơn",
          "pron": "🇺🇸 🇬🇧 /ɪˈlæbəreɪt/",
          "register": "neutral",
          "example": "Could you elaborate on the rollback plan?",
          "note": "Dùng khi muốn nghe nhiều hơn về một điểm cụ thể",
          "situation": "Architect trình bày solution ngắn gọn, bạn muốn nghe chi tiết hơn về rollback plan."
        },
        {
          "term": "unpack",
          "level": "B2",
          "vi": "phân tích, giải thích từng phần",
          "pron": "🇺🇸 🇬🇧 /ʌnˈpæk/",
          "register": "casual",
          "example": "Let's unpack what 'scalable' means for this system.",
          "note": "Tech/startup culture — dùng cho abstract/complex concepts",
          "situation": "Team đang dùng 'scalable' nhưng mỗi người hiểu khác nhau — cần align định nghĩa chung."
        },
        {
          "term": "walk me through",
          "level": "B2",
          "vi": "hướng dẫn từng bước, giải thích theo thứ tự",
          "pron": "",
          "register": "casual",
          "example": "Can you walk me through your deployment process?",
          "note": "Request step-by-step explanation — rất phổ biến trong code review/onboarding",
          "situation": "Bạn vừa join team mới và muốn hiểu quy trình deploy của team từng bước một."
        }
      ],
      "vi_name": "Yêu cầu làm rõ"
    },
    {
      "id": "syn_problem",
      "type": "synonym",
      "subtype": null,
      "name": "Describing Problems",
      "level": "B2",
      "topic": "Business",
      "tip": "issue/concern → polite; blocker → chặn progress; bottleneck → điểm chậm nhất; showstopper → nghiêm trọng nhất, phải fix trước khi ship",
      "words": [
        {
          "term": "issue",
          "level": "B1",
          "vi": "vấn đề (trung tính)",
          "pron": "🇺🇸 🇬🇧 /ˈɪʃuː/",
          "register": "neutral",
          "example": "We have an issue with the authentication flow.",
          "note": "General-purpose, ít cảm xúc hơn 'problem'",
          "situation": "Trong standup, bạn cần báo cáo có vấn đề với authentication flow — tone trung tính."
        },
        {
          "term": "blocker",
          "level": "B2",
          "vi": "vật cản, thứ block progress",
          "pron": "🇺🇸 🇬🇧 /ˈblɒkər/",
          "register": "casual",
          "example": "The missing API docs are a blocker for the frontend team.",
          "note": "Scrum/Agile term — dùng trong standup, Jira tickets",
          "situation": "Bạn không thể tiếp tục task vì đang chờ API docs từ team khác — phải báo cáo trong standup."
        },
        {
          "term": "bottleneck",
          "level": "B2",
          "vi": "điểm nghẽn cổ chai, điểm chậm nhất",
          "pron": "🇺🇸 🇬🇧 /ˈbɒtəlnɛk/",
          "register": "neutral",
          "example": "The database query is the bottleneck in our pipeline.",
          "note": "Thường dùng cho performance/process issues",
          "situation": "Sau khi profile hệ thống, database query là điểm chậm nhất trong toàn bộ pipeline."
        },
        {
          "term": "showstopper",
          "level": "B2",
          "vi": "vấn đề nghiêm trọng cản launch",
          "pron": "🇺🇸 🇬🇧 /ˈʃoʊstɒpər/",
          "register": "casual",
          "example": "This data loss bug is a showstopper — we can't ship with it.",
          "note": "Mức độ nghiêm trọng nhất — release bị chặn hoàn toàn",
          "situation": "Phát hiện bug data loss ngay trước ngày launch — không thể ship với bug này."
        }
      ],
      "vi_name": "Mô tả vấn đề"
    },
    {
      "id": "syn_complete",
      "type": "synonym",
      "subtype": null,
      "name": "Finishing Work",
      "level": "B2",
      "topic": "Business",
      "tip": "wrap up → meeting/session; finalize → còn bước review cuối; ship → release sản phẩm; sign off → phê duyệt chính thức",
      "words": [
        {
          "term": "wrap up",
          "level": "B1",
          "vi": "kết thúc, hoàn tất (session/meeting)",
          "pron": "🇺🇸 🇬🇧 /ræp ʌp/",
          "register": "casual",
          "example": "Let's wrap up this discussion and move to the next agenda item.",
          "note": "Thường dùng để kết thúc meeting hoặc conversation",
          "situation": "Meeting sprint planning đã gần hết giờ, bạn cần kết thúc và capture action items."
        },
        {
          "term": "finalize",
          "level": "B2",
          "vi": "hoàn thiện, chốt lại (còn bước review cuối)",
          "pron": "🇺🇸 🇬🇧 /ˈfaɪnəlaɪz/",
          "register": "neutral",
          "example": "We need to finalize the requirements before development starts.",
          "note": "Ngụ ý còn bước kiểm tra/phê duyệt cuối cùng",
          "situation": "Requirements đang ở bản draft, cần confirm với stakeholders trước khi dev bắt đầu sprint."
        },
        {
          "term": "ship",
          "level": "B1",
          "vi": "release, phát hành sản phẩm/tính năng",
          "pron": "🇺🇸 🇬🇧 /ʃɪp/",
          "register": "casual",
          "example": "We shipped the new dashboard last Friday.",
          "note": "Tech culture informal — 'ship it' = release it",
          "situation": "Feature đã pass QA và được PM approve — bạn đã deploy lên production thành công."
        },
        {
          "term": "sign off",
          "level": "B2",
          "vi": "phê duyệt, xác nhận hoàn tất",
          "pron": "🇺🇸 🇬🇧 /saɪn ɒf/",
          "register": "neutral",
          "example": "The PM needs to sign off on this before we deploy.",
          "note": "Formal approval — thường kèm email confirm hoặc LGTM",
          "situation": "Legal team cần review và confirm trước khi bạn có thể deploy lên production."
        }
      ],
      "vi_name": "Hoàn thành công việc"
    },
    {
      "id": "syn_important",
      "type": "synonym",
      "subtype": null,
      "name": "Expressing Importance",
      "level": "B2",
      "topic": "Business",
      "tip": "critical/crucial → nếu không làm sẽ có hậu quả; vital → thiếu thì không hoạt động; mission-critical → business không thể dừng; non-negotiable → không có ngoại lệ",
      "words": [
        {
          "term": "critical",
          "level": "B1",
          "vi": "cực kỳ quan trọng, quyết định",
          "pron": "🇺🇸 🇬🇧 /ˈkrɪtɪkəl/",
          "register": "neutral",
          "example": "Getting the architecture right is critical for long-term scalability.",
          "note": "Không làm = có hậu quả. Phân biệt với 'critical feedback' (nhận xét góp ý)",
          "situation": "Bạn giải thích cho junior dev tại sao viết tests cho payment module là bắt buộc."
        },
        {
          "term": "crucial",
          "level": "B2",
          "vi": "thiết yếu, không thể thiếu",
          "pron": "🇺🇸 🇬🇧 /ˈkruːʃəl/",
          "register": "neutral",
          "example": "User feedback is crucial at this stage of development.",
          "note": "Gần nghĩa với critical — nhấn vào 'không có thì không được'",
          "situation": "Trong sprint review, bạn nhấn mạnh tầm quan trọng của việc collect user feedback giai đoạn này."
        },
        {
          "term": "mission-critical",
          "level": "B2",
          "vi": "không thể gián đoạn, sống còn với business",
          "pron": "🇺🇸 🇬🇧 /ˈmɪʃən ˈkrɪtɪkəl/",
          "register": "formal",
          "example": "The payment service is mission-critical — zero downtime acceptable.",
          "note": "Ops/DevOps context — implies 24/7 uptime requirement",
          "situation": "Bạn giải thích với manager tại sao payment service phải đảm bảo 99.99% uptime SLA."
        },
        {
          "term": "non-negotiable",
          "level": "B2",
          "vi": "không thể thương lượng, phải giữ nguyên",
          "pron": "🇺🇸 🇬🇧 /nɒn nɪˈɡoʊʃiəbəl/",
          "register": "formal",
          "example": "Security compliance is non-negotiable.",
          "note": "Dùng khi muốn nói rõ không có ngoại lệ",
          "situation": "Security compliance là hard requirement — không có exception dù deadline có tight đến đâu."
        }
      ],
      "vi_name": "Diễn đạt tầm quan trọng"
    },
    {
      "id": "casual_buy_time",
      "type": "casual",
      "subtype": "buy_time",
      "name": "Buying Time to Think",
      "level": "B2",
      "topic": "Meetings",
      "tip": "Dùng khi cần vài giây suy nghĩ — tránh im lặng awkward. Đừng overuse cùng một phrase.",
      "words": [
        {
          "term": "That's a good question.",
          "level": "B1",
          "vi": "Câu hỏi hay đấy.",
          "pron": "",
          "register": "neutral",
          "example": "That's a good question — let me think about that for a moment.",
          "note": "Classic buy-time phrase. Đừng dùng quá nhiều sẽ nghe giả tạo",
          "situation": "Trong demo với client, họ hỏi về product roadmap — bạn chưa chuẩn bị câu trả lời cụ thể."
        },
        {
          "term": "Let me think about that.",
          "level": "B1",
          "vi": "Để tôi suy nghĩ một chút.",
          "pron": "",
          "register": "neutral",
          "example": "Let me think about that — I want to give you a proper answer.",
          "note": "Honest và professional — không có gì sai khi cần thêm thời gian",
          "situation": "CTO hỏi về tradeoff của approach bạn đang propose — bạn cần vài giây suy nghĩ kỹ."
        },
        {
          "term": "Off the top of my head...",
          "level": "B2",
          "vi": "Ngay lúc này không cần suy nghĩ nhiều...",
          "pron": "",
          "register": "casual",
          "example": "Off the top of my head, I'd say around two weeks — but let me verify.",
          "note": "Ngụ ý 'đây là rough estimate, chưa chắc chính xác'",
          "situation": "Trong standup, bạn được hỏi về timeline — bạn có estimate nhưng chưa verify con số chính xác."
        },
        {
          "term": "I'll need to circle back on that.",
          "level": "B2",
          "vi": "Tôi cần xem lại và trả lời sau.",
          "pron": "",
          "register": "casual",
          "example": "I don't have that number handy — I'll circle back on that.",
          "note": "Dùng khi thực sự không biết — tốt hơn là đoán mò",
          "situation": "Trong meeting, bạn được hỏi về performance metric cụ thể mà bạn không nhớ lúc này."
        }
      ],
      "vi_name": "Câu giờ để suy nghĩ"
    },
    {
      "id": "casual_agree",
      "type": "casual",
      "subtype": "agree",
      "name": "Casual Agreement",
      "level": "B2",
      "topic": "Slack",
      "tip": "Dùng thay cho 'yes/ok' trong Slack và informal meetings. Sounds much more native!",
      "words": [
        {
          "term": "Sounds good.",
          "level": "B1",
          "vi": "Nghe được đấy / Đồng ý.",
          "pron": "",
          "register": "casual",
          "example": "— Can we move the meeting to 3 PM? — Sounds good to me!",
          "note": "Extremely common trong tech teams — thân thiện và natural",
          "situation": "Đồng nghiệp nhắn Slack hỏi có thể dời meeting từ 2PM sang 3PM được không."
        },
        {
          "term": "Absolutely.",
          "level": "B1",
          "vi": "Chắc chắn rồi / Hoàn toàn đồng ý.",
          "pron": "🇺🇸 🇬🇧 /ˈæbsəluːtli/",
          "register": "neutral",
          "example": "— Do you think we should prioritize the API first? — Absolutely.",
          "note": "Stronger than 'yes' — thể hiện enthusiasm và agreement mạnh",
          "situation": "PM hỏi bạn có đồng ý nên prioritize API layer trước khi làm frontend không."
        },
        {
          "term": "Fair enough.",
          "level": "B2",
          "vi": "Hợp lý đấy / Thôi được.",
          "pron": "",
          "register": "casual",
          "example": "— Let's skip the demo and just do a screen share. — Fair enough.",
          "note": "'Tôi chấp nhận' — không nhất thiết hoàn toàn đồng ý",
          "situation": "Team lead đề xuất skip formal demo và dùng screen share thay vì setup presentation phức tạp."
        },
        {
          "term": "Makes sense.",
          "level": "B1",
          "vi": "Hợp lý / Có lý đấy.",
          "pron": "",
          "register": "casual",
          "example": "— We should test on staging before prod. — Makes sense.",
          "note": "Thể hiện bạn hiểu và thấy logical — rất tự nhiên",
          "situation": "Đồng nghiệp giải thích lý do tại sao nên test kỹ trên staging trước khi deploy prod."
        }
      ],
      "vi_name": "Đồng ý thông thường"
    },
    {
      "id": "casual_soft_disagree",
      "type": "casual",
      "subtype": "soft_disagree",
      "name": "Disagreeing Softly",
      "level": "B2",
      "topic": "Meetings",
      "tip": "Tránh 'you're wrong' — dùng question/suggestion thay. Phản biện về vấn đề, không về con người.",
      "words": [
        {
          "term": "I'm not sure about that.",
          "level": "B1",
          "vi": "Tôi không chắc về điều đó.",
          "pron": "",
          "register": "neutral",
          "example": "I'm not sure about that — have we looked at the actual metrics?",
          "note": "Nhẹ nhàng nhất — tạo không gian để discuss thêm",
          "situation": "PM estimate 1 tuần cho feature phức tạp, bạn nghĩ không đủ nhưng muốn hỏi nhẹ nhàng."
        },
        {
          "term": "Have you considered...?",
          "level": "B2",
          "vi": "Bạn đã cân nhắc... chưa?",
          "pron": "",
          "register": "neutral",
          "example": "Have you considered the impact on existing users?",
          "note": "Polite redirect — đưa thêm góc nhìn mà không bác bỏ trực tiếp",
          "situation": "Team đang plan feature mới mà không consider impact đến existing users — bạn muốn raise."
        },
        {
          "term": "What if we...?",
          "level": "B1",
          "vi": "Nếu chúng ta... thì sao?",
          "pron": "",
          "register": "casual",
          "example": "What if we delayed the launch by one sprint to get more testing done?",
          "note": "Propose alternative — redirect constructively",
          "situation": "Team định launch ngay sau dev xong, bạn muốn đề xuất thêm 1 sprint để test kỹ hơn."
        },
        {
          "term": "I see it differently.",
          "level": "B2",
          "vi": "Tôi nhìn nhận khác một chút.",
          "pron": "",
          "register": "neutral",
          "example": "I see it differently — I think the risk is higher than we're estimating.",
          "note": "Rõ ràng nhưng không aggressive — acknowledge sự khác biệt quan điểm",
          "situation": "Tech lead assess risk là low nhưng bạn thấy ngược lại — muốn express khác biệt quan điểm respectfully."
        }
      ],
      "vi_name": "Phản đối nhẹ nhàng"
    },
    {
      "id": "casual_follow_up",
      "type": "casual",
      "subtype": "follow_up",
      "name": "Following Up",
      "level": "B2",
      "topic": "Slack",
      "tip": "Dùng trong email/Slack sau meeting hoặc khi task chưa có phản hồi. Lịch sự hơn 'Hey, did you do it?'",
      "words": [
        {
          "term": "Just following up on...",
          "level": "B1",
          "vi": "Tôi chỉ muốn hỏi thêm về...",
          "pron": "",
          "register": "neutral",
          "example": "Just following up on the PR I submitted — any blockers on your end?",
          "note": "Standard email/Slack opener khi chờ reply",
          "situation": "Bạn submit PR 2 ngày trước, chưa có reviewer nào comment — muốn nhắc nhẹ."
        },
        {
          "term": "Circling back on...",
          "level": "B2",
          "vi": "Quay lại vấn đề... (nhắc nhở)",
          "pron": "",
          "register": "casual",
          "example": "Circling back on the design review — are we still on for Thursday?",
          "note": "Casual alternative cho 'following up' — phổ biến trong tech teams",
          "situation": "Design review đã thảo luận hôm qua nhưng chưa confirm có diễn ra Thursday không."
        },
        {
          "term": "Any update on...?",
          "level": "B1",
          "vi": "Có cập nhật gì về... chưa?",
          "pron": "",
          "register": "casual",
          "example": "Any update on the server issue from last week?",
          "note": "Direct và casual — phù hợp Slack hơn email",
          "situation": "Server issue từ tuần trước chưa thấy update — bạn muốn hỏi thẳng trên Slack."
        },
        {
          "term": "Wanted to check in on...",
          "level": "B2",
          "vi": "Muốn hỏi thăm tình hình của...",
          "pron": "",
          "register": "neutral",
          "example": "Wanted to check in on the migration timeline.",
          "note": "Softer than 'following up' — nghe ít transactional hơn",
          "situation": "Bạn muốn hỏi thăm tiến độ migration một cách nhẹ nhàng, không tạo áp lực."
        }
      ],
      "vi_name": "Theo dõi tiến độ"
    },
    {
      "id": "casual_wrap_up",
      "type": "casual",
      "subtype": "wrap_up",
      "name": "Wrapping Up a Meeting",
      "level": "B2",
      "topic": "Meetings",
      "tip": "Dùng để kết thúc meeting có cấu trúc — recap action items trước khi close",
      "words": [
        {
          "term": "Let's wrap up.",
          "level": "B1",
          "vi": "Chúng ta kết thúc thôi.",
          "pron": "",
          "register": "casual",
          "example": "We're almost out of time — let's wrap up and capture action items.",
          "note": "Standard meeting closer",
          "situation": "Meeting sprint planning đã gần hết 1 tiếng, còn 5 phút — cần kết thúc ngay."
        },
        {
          "term": "To summarize...",
          "level": "B1",
          "vi": "Tóm lại...",
          "pron": "",
          "register": "neutral",
          "example": "To summarize: we'll delay the release by one week and add load testing.",
          "note": "Signal cho recap — giúp mọi người align trước khi rời meeting",
          "situation": "Sau 30 phút thảo luận về release date, cần recap quyết định cuối trước khi mọi người log off."
        },
        {
          "term": "On that note...",
          "level": "B2",
          "vi": "Nhân đây... / Với điều đó...",
          "pron": "",
          "register": "neutral",
          "example": "On that note, I think we've covered everything. Thanks everyone!",
          "note": "Elegant meeting closer — transition từ thảo luận sang kết thúc",
          "situation": "Sau khi xong tất cả agenda items, bạn muốn kết thúc meeting lịch sự và gọn gàng."
        },
        {
          "term": "Let's take this offline.",
          "level": "B2",
          "vi": "Chúng ta thảo luận riêng sau nhé.",
          "pron": "",
          "register": "casual",
          "example": "This is getting detailed — let's take this offline.",
          "note": "Khi topic phức tạp cần thảo luận riêng, không chiếm thời gian cả nhóm",
          "situation": "Cuộc tranh luận kỹ thuật giữa 2 người quá chi tiết, đang chiếm thời gian của cả nhóm 10 người."
        }
      ],
      "vi_name": "Kết thúc cuộc họp"
    },
    {
      "id": "theme_pr_review",
      "type": "thematic",
      "subtype": null,
      "name": "Code Review Vocabulary",
      "level": "B2",
      "topic": "Tech",
      "tip": "Những từ/cụm standard trong GitHub/GitLab PR review — cần biết để đọc và viết comment",
      "words": [
        {
          "term": "LGTM",
          "level": "B1",
          "vi": "Looks Good To Me — ok, approve",
          "pron": "",
          "register": "spoken",
          "example": "LGTM! Nice clean implementation.",
          "note": "Acronym phổ biến nhất trong code review — = approved",
          "situation": "Bạn review PR của đồng nghiệp — code clean, logic đúng, tests pass — muốn approve."
        },
        {
          "term": "nit",
          "level": "B1",
          "vi": "nhận xét nhỏ (không bắt buộc sửa)",
          "pron": "🇺🇸 🇬🇧 /nɪt/",
          "register": "casual",
          "example": "Nit: this variable name could be more descriptive.",
          "note": "Short for 'nitpick' — optional to fix, không ảnh hưởng logic",
          "situation": "Logic PR ổn nhưng tên biến có thể descriptive hơn — muốn comment nhẹ, không blocking."
        },
        {
          "term": "blocking",
          "level": "B1",
          "vi": "comment bắt buộc phải fix trước khi merge",
          "pron": "🇺🇸 🇬🇧 /ˈblɒkɪŋ/",
          "register": "casual",
          "example": "Blocking: this will cause a memory leak in production.",
          "note": "Blocking = must fix. Non-blocking = nice to have",
          "situation": "Bạn phát hiện memory leak nghiêm trọng trong PR — không thể merge với bug này."
        },
        {
          "term": "request changes",
          "level": "B1",
          "vi": "yêu cầu chỉnh sửa (không approve)",
          "pron": "",
          "register": "neutral",
          "example": "I'll request changes — the error handling needs work.",
          "note": "GitHub action — khác với 'comment' (không approve/reject)",
          "situation": "Error handling trong PR chưa đúng, bạn không approve nhưng cũng không reject hẳn."
        },
        {
          "term": "out of scope",
          "level": "B2",
          "vi": "ngoài phạm vi (của PR này)",
          "pron": "",
          "register": "neutral",
          "example": "This refactor is out of scope for this PR — open a separate ticket.",
          "note": "Quan trọng để keep PRs focused và reviewable",
          "situation": "PR để fix bug nhưng author thêm cả refactor module khác không liên quan đến issue."
        }
      ],
      "vi_name": "Từ vựng Review Code"
    },
    {
      "id": "theme_meeting_vocab",
      "type": "thematic",
      "subtype": null,
      "name": "Meeting Outcomes",
      "level": "B2",
      "topic": "Meetings",
      "tip": "Những từ dùng sau meeting để document kết quả — biết để viết meeting notes chuẩn",
      "words": [
        {
          "term": "action item",
          "level": "B1",
          "vi": "việc cần làm (sau meeting, có người chịu trách nhiệm)",
          "pron": "🇺🇸 🇬🇧 /ˈækʃən ˈaɪtəm/",
          "register": "neutral",
          "example": "Action item: Nguyen to set up load testing by Friday.",
          "note": "Luôn có owner và deadline — phân biệt với 'todo' chung chung",
          "situation": "Sau meeting, cần document công việc cụ thể của từng người với owner và deadline rõ ràng."
        },
        {
          "term": "takeaway",
          "level": "B2",
          "vi": "điều rút ra, bài học từ meeting",
          "pron": "🇺🇸 🇬🇧 /ˈteɪkəweɪ/",
          "register": "neutral",
          "example": "Key takeaway: we need better monitoring before scaling up.",
          "note": "Insight/conclusion rút ra từ discussion",
          "situation": "Sau incident review, bạn muốn note lại insight quan trọng rút ra từ outage này."
        },
        {
          "term": "next steps",
          "level": "B1",
          "vi": "các bước tiếp theo",
          "pron": "",
          "register": "neutral",
          "example": "Let's align on next steps before we close out.",
          "note": "Thường cuối meeting để ensure clarity trước khi mọi người rời đi",
          "situation": "Trước khi kết thúc planning meeting, cần ensure mọi người biết phải làm gì tiếp theo."
        },
        {
          "term": "owner",
          "level": "B1",
          "vi": "người chịu trách nhiệm",
          "pron": "🇺🇸 🇬🇧 /ˈoʊnər/",
          "register": "neutral",
          "example": "Who's the owner for this action item?",
          "note": "Mỗi task/story cần có owner rõ ràng — tránh 'we all own it'",
          "situation": "Action item vừa được tạo nhưng chưa ai nhận trách nhiệm — cần assign người chịu trách."
        }
      ],
      "vi_name": "Kết quả cuộc họp"
    },
    {
      "id": "theme_feedback",
      "type": "thematic",
      "subtype": null,
      "name": "Giving Constructive Feedback",
      "level": "B2",
      "topic": "Discussion",
      "tip": "Frame feedback về impact và solution, không phải cá nhân. 'The code has an issue' not 'you made a mistake'.",
      "words": [
        {
          "term": "it would be stronger if...",
          "level": "B2",
          "vi": "sẽ tốt hơn nếu...",
          "pron": "",
          "register": "neutral",
          "example": "This PR would be stronger if it included unit tests.",
          "note": "Positive framing — gợi ý cải tiến thay vì chỉ trích",
          "situation": "Review PR: code logic đúng nhưng thiếu unit tests — muốn suggest thêm mà không harsh."
        },
        {
          "term": "one suggestion would be...",
          "level": "B2",
          "vi": "một gợi ý là...",
          "pron": "",
          "register": "neutral",
          "example": "One suggestion would be to extract this into a helper function.",
          "note": "Softer than 'you should' — tạo không gian để người nhận quyết định",
          "situation": "Code chạy được nhưng có thể extract helper function để cleaner — muốn suggest nhẹ nhàng."
        },
        {
          "term": "I wonder if...",
          "level": "B2",
          "vi": "Tôi tự hỏi liệu... (gợi ý nhẹ nhàng)",
          "pron": "",
          "register": "neutral",
          "example": "I wonder if this edge case has been handled?",
          "note": "Raise concern mà không accuse — 'perhaps you missed this'",
          "situation": "Trong code review, bạn nghi ngờ edge case chưa được handle nhưng không chắc chắn."
        },
        {
          "term": "that said...",
          "level": "B2",
          "vi": "dù vậy... / tuy nhiên...",
          "pron": "",
          "register": "neutral",
          "example": "The architecture is solid. That said, the error handling needs work.",
          "note": "Balance feedback — acknowledge strengths trước khi critique",
          "situation": "Bạn muốn acknowledge điểm mạnh của PR trước khi nêu vấn đề cần cải thiện."
        }
      ],
      "vi_name": "Góp ý xây dựng"
    },
    {
      "id": "theme_deadline",
      "type": "thematic",
      "subtype": null,
      "name": "Deadline & Time Pressure",
      "level": "B2",
      "topic": "Business",
      "tip": "on track ↔ behind schedule ↔ ahead of schedule. slip = trượt nhẹ (neutral). miss = thất bại (negative).",
      "words": [
        {
          "term": "behind schedule",
          "level": "B2",
          "vi": "trễ tiến độ",
          "pron": "",
          "register": "neutral",
          "example": "We're behind schedule by three days — the migration took longer than expected.",
          "note": "Contrast: 'on track' = đúng tiến độ, 'ahead of schedule' = sớm hơn dự kiến",
          "situation": "Bạn update status cho PM: migration mất lâu hơn dự kiến, trễ 3 ngày so với plan."
        },
        {
          "term": "crunch time",
          "level": "B2",
          "vi": "giai đoạn nước rút, làm overtime trước deadline",
          "pron": "🇺🇸 🇬🇧 /krʌntʃ taɪm/",
          "register": "casual",
          "example": "It's crunch time — everyone needs to prioritize the launch blockers.",
          "note": "Informal — implies high pressure, possible overtime",
          "situation": "1 tuần trước launch date, team cần tập trung 100% vào blocking issues."
        },
        {
          "term": "buffer",
          "level": "B2",
          "vi": "thời gian dự phòng, đệm",
          "pron": "🇺🇸 🇬🇧 /ˈbʌfər/",
          "register": "neutral",
          "example": "Let's add a two-day buffer to account for unexpected issues.",
          "note": "Planning term — mọi estimation đều nên có buffer",
          "situation": "Estimate 2 tuần nhưng muốn add thêm thời gian để cover unexpected issues."
        },
        {
          "term": "slip",
          "level": "B2",
          "vi": "trượt deadline, bị lùi",
          "pron": "🇺🇸 🇬🇧 /slɪp/",
          "register": "neutral",
          "example": "The release date slipped by a week due to a critical bug.",
          "note": "Neutral — không negative như 'miss deadline'",
          "situation": "Release date phải dời vì phát hiện critical bug muộn — cần thông báo stakeholders."
        }
      ],
      "vi_name": "Deadline & Áp lực thời gian"
    },
    {
      "id": "coll_raise",
      "type": "collocation",
      "subtype": null,
      "name": "\"Raise\" Collocations",
      "level": "B2",
      "topic": "Business",
      "tip": "raise = đưa vấn đề lên để thảo luận/giải quyết. Khác với 'open' chỉ dùng cho ticket (GitHub/Jira).",
      "words": [
        {
          "term": "raise an issue",
          "level": "B2",
          "vi": "nêu ra một vấn đề",
          "pron": "",
          "register": "neutral",
          "example": "I'd like to raise an issue regarding the deployment process.",
          "note": "Formal way to introduce a problem",
          "contrast": "drop an issue",
          "wrong_usage": "❌ 'open an issue' trong meeting — chỉ dùng cho GitHub/Jira ticket",
          "situation": "Trong retrospective, bạn muốn đưa vấn đề về deployment process lên để team thảo luận."
        },
        {
          "term": "raise concerns",
          "level": "B2",
          "vi": "bày tỏ lo ngại",
          "pron": "",
          "register": "formal",
          "example": "Several team members have raised concerns about the timeline.",
          "note": "Professional cách express worry — tốt hơn 'I'm worried'",
          "situation": "Bạn lo ngại về security implications của feature mới — muốn voice một cách professional."
        },
        {
          "term": "raise a question",
          "level": "B1",
          "vi": "đặt ra câu hỏi",
          "pron": "",
          "register": "neutral",
          "example": "Your proposal raises an interesting question about data privacy.",
          "note": "Polite way to question something — không trực tiếp phản đối",
          "situation": "Sau khi nghe proposal về new architecture, bạn muốn hỏi về data privacy implications."
        },
        {
          "term": "raise awareness",
          "level": "B2",
          "vi": "nâng cao nhận thức",
          "pron": "",
          "register": "neutral",
          "example": "We need to raise awareness about security best practices.",
          "note": "Dùng khi vấn đề chưa được team biết/chú ý đến",
          "situation": "Team chưa ai biết về API security best practices mới — bạn muốn share thông tin này."
        }
      ],
      "vi_name": "Cụm từ với \"Raise\""
    },
    {
      "id": "filler_spoken",
      "type": "filler",
      "subtype": "spoken_pause",
      "name": "Spoken Filler Phrases",
      "level": "B1",
      "topic": "Discussion",
      "tip": "Dùng để fill khoảng lặng tự nhiên khi nói — tránh 'uh... uh...' nhưng đừng overuse một phrase",
      "words": [
        {
          "term": "So...",
          "level": "B1",
          "vi": "Vậy... / Thế thì...",
          "pron": "",
          "register": "spoken",
          "example": "So... where were we? Oh right, the authentication issue.",
          "note": "Universal transition khi bắt đầu nói hoặc sau pause",
          "situation": "Bạn bị interrupt khi đang giải thích solution, muốn resume lại conversation sau khoảng dừng."
        },
        {
          "term": "Actually...",
          "level": "B1",
          "vi": "Thực ra... / Thật ra là...",
          "pron": "🇺🇸 🇬🇧 /ˈæktʃuəli/",
          "register": "spoken",
          "example": "Actually, I think we should reconsider the approach.",
          "note": "Introduce correction hoặc different perspective",
          "situation": "Bạn vừa nói xong một điểm nhưng muốn correct lại hoặc add góc nhìn khác."
        },
        {
          "term": "I mean...",
          "level": "B1",
          "vi": "Ý tôi là...",
          "pron": "",
          "register": "spoken",
          "example": "It's not that simple. I mean, we have to consider the edge cases too.",
          "note": "Clarify hoặc elaborate on something just said",
          "situation": "Bạn vừa dùng technical jargon, muốn elaborate thêm để người nghe non-technical hiểu rõ."
        },
        {
          "term": "You know what I mean?",
          "level": "B1",
          "vi": "Bạn hiểu ý tôi không?",
          "pron": "",
          "register": "spoken",
          "example": "The performance was just... not great, you know what I mean?",
          "note": "Check understanding — informal, tránh dùng với senior/executive",
          "situation": "Bạn vừa mô tả performance issue khá vague, muốn check xem người nghe có hiểu ý không."
        }
      ],
      "vi_name": "Câu đệm khi nói"
    },
    {
      "id": "filler_written",
      "type": "filler",
      "subtype": "written_transition",
      "name": "Written Transition Words",
      "level": "B2",
      "topic": "Discussion",
      "tip": "Dùng trong email, Confluence, PR description. Đừng overuse 'however' — vary your connectors.",
      "words": [
        {
          "term": "However,",
          "level": "B1",
          "vi": "Tuy nhiên,",
          "pron": "🇺🇸 🇬🇧 /haʊˈɛvər/",
          "register": "neutral",
          "example": "The feature works as expected. However, performance on mobile needs improvement.",
          "note": "Contrast — phổ biến nhất trong technical writing",
          "situation": "Trong email gửi PM: feature đã chạy đúng nhưng cần đề cập performance concern trên mobile."
        },
        {
          "term": "Therefore,",
          "level": "B1",
          "vi": "Do đó, / Vì vậy,",
          "pron": "🇺🇸 🇬🇧 /ˈðɛrəfɔːr/",
          "register": "formal",
          "example": "The API is deprecated. Therefore, we need to migrate by Q2.",
          "note": "Logical consequence — formal trong documents",
          "situation": "Trong Confluence: API này đã deprecated, cần viết rõ hệ quả và action cần làm."
        },
        {
          "term": "In addition,",
          "level": "B1",
          "vi": "Ngoài ra,",
          "pron": "",
          "register": "neutral",
          "example": "We reduced load time by 40%. In addition, memory usage dropped significantly.",
          "note": "Add more information. Alternatives: Moreover, Furthermore (more formal)",
          "situation": "Trong release notes: ngoài feature chính, còn có performance improvement cần mention."
        },
        {
          "term": "That said,",
          "level": "B2",
          "vi": "Dù vậy, / Tuy nhiên,",
          "pron": "",
          "register": "neutral",
          "example": "The solution is elegant. That said, it adds complexity to the codebase.",
          "note": "Balance positive và negative — sounds more natural than 'however'",
          "situation": "Trong PR description: acknowledge architecture decision tốt nhưng cần note complexity thêm."
        },
        {
          "term": "As a result,",
          "level": "B1",
          "vi": "Kết quả là,",
          "pron": "",
          "register": "neutral",
          "example": "We deployed the hotfix at midnight. As a result, error rates dropped to zero.",
          "note": "Show cause-effect — good cho incident reports, post-mortems",
          "situation": "Trong incident report: sau khi deploy hotfix lúc nửa đêm, kết quả đạt được là gì."
        }
      ],
      "vi_name": "Từ nối văn viết"
    },
    {
      "id": "filler_presentation",
      "type": "filler",
      "subtype": "presentation",
      "name": "Presentation Phrases",
      "level": "B2",
      "topic": "Meetings",
      "tip": "Dùng khi trình bày trong meeting hoặc demo — giúp structure bài nói và transition smoothly",
      "words": [
        {
          "term": "Moving on to...",
          "level": "B1",
          "vi": "Chuyển sang...",
          "pron": "",
          "register": "neutral",
          "example": "Moving on to the next slide — let's look at the performance metrics.",
          "note": "Standard presentation transition khi chuyển topic/slide",
          "situation": "Trong demo với stakeholders, bạn cần chuyển từ architecture overview slide sang live demo."
        },
        {
          "term": "Building on that...",
          "level": "B2",
          "vi": "Mở rộng từ ý đó...",
          "pron": "",
          "register": "neutral",
          "example": "Building on that, I'd like to show how this affects our SLA.",
          "note": "Connect ý tiếp theo với ý vừa nói — flow tốt hơn 'and also'",
          "situation": "Sau khi trình bày về problem, bạn muốn kết nối smooth sang proposed solution."
        },
        {
          "term": "With that in mind...",
          "level": "B2",
          "vi": "Với điều đó trong đầu...",
          "pron": "",
          "register": "neutral",
          "example": "With that in mind, let's look at our proposed solution.",
          "note": "Bridge từ problem sang solution — rất professional",
          "situation": "Sau khi show performance metrics đáng lo ngại, bạn muốn transition sang proposed solution."
        },
        {
          "term": "To put it simply...",
          "level": "B2",
          "vi": "Nói đơn giản là...",
          "pron": "",
          "register": "neutral",
          "example": "To put it simply, we're trading latency for consistency.",
          "note": "Dùng khi muốn simplify technical concept cho non-technical audience",
          "situation": "Bạn vừa giải thích distributed systems concept phức tạp, cần simplify cho non-technical PM."
        }
      ],
      "vi_name": "Câu mở đầu thuyết trình"
    }
  ]
};
