from services.video_service import get_logo_base64

def answer_html(q, index):
    logo_base64 = get_logo_base64()

    # ✅ FIX: bilingual question
    question_en = q["question"]["en"]
    question_hi = q["question"]["hi"]

    # ✅ FIX: explanation
    explanation_en = q["explanation"]["en"]
    explanation_hi = q["explanation"]["hi"]

    options_html = ""

    for i, opt in enumerate(q["options"]):
        text = f"{opt['en']} / {opt['hi']}"

        if i == q["answer_index"]:
            options_html += f'<div class="option correct">{chr(65+i)}. {text}</div>'
        else:
            options_html += f'<div class="option">{chr(65+i)}. {text}</div>'

    return f"""
<html>
<head>
<style>
    body {{
        width: 1080px;
        height: 1920px;
        margin: 0;
        font-family: Arial;
        background: black;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .container {{
        width: 90%;
        text-align: center;
    }}

    .logo {{
        width: 260px;
        height: 260px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 25px;
        box-shadow: 0 0 25px #00c3ff, 0 0 50px rgba(0,195,255,0.5);
        border: 4px solid rgba(255,255,255,0.2);
    }}

    .question {{
        font-size: 50px;
        margin-bottom: 40px;
    }}

    .option {{
        font-size: 40px;
        margin: 15px 0;
        padding: 20px;
        border-radius: 12px;
        background: rgba(255,255,255,0.1);
    }}

    .correct {{
        background: #00ff9d;
        color: black;
        box-shadow: 0 0 20px #00ff9d;
    }}

    /* ✅ NEW (minimal addition, no design break) */
    .explanation {{
        margin-top: 40px;
        font-size: 32px;
        color: #ffcc00;
    }}
</style>
</head>

<body>
    <div class="container">
        <img class="logo" src="data:image/png;base64,{logo_base64}" />

        <div class="question">
            Q{index+1}. {question_en}<br/>
            <span style="color:#ccc">{question_hi}</span>
        </div>

        {options_html}

        <!-- ✅ NEW: Explanation below answer -->
        <div class="explanation">
            💡 {explanation_en}<br/>
            <span style="color:#ccc">{explanation_hi}</span>
        </div>

    </div>
</body>
</html>
"""