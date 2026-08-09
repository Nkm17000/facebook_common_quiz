from services.video_service import get_logo_base64

def answer_html(q, index):
    logo_base64 = get_logo_base64()

    # ✅ HANDLE BOTH (dict + string)
    if isinstance(q["question"], dict):
        question = f'{q["question"]["en"]}<br><span class="hi">{q["question"]["hi"]}</span>'
    else:
        question = q["question"]

    # ✅ HANDLE OPTIONS (dict + string)
    formatted_options = []
    for opt in q["options"]:
        if isinstance(opt, dict):
            formatted_options.append(
                f'{opt["en"]}<br><span class="hi-opt">{opt["hi"]}</span>'
            )
        else:
            formatted_options.append(opt)

    # ✅ OPTIONS HTML
    options_html = ""
    for i, opt in enumerate(formatted_options):
        if i == q["answer_index"]:
            options_html += f'<div class="option correct">{chr(65+i)}. {opt}</div>'
        else:
            options_html += f'<div class="option">{chr(65+i)}. {opt}</div>'

    # ✅ EXPLANATION (SAFE)
    explanation_html = ""
    if "explanation" in q:
        if isinstance(q["explanation"], dict):
            explanation_html = f"""
            <div class="explanation">
                💡 {q["explanation"]["en"]}
                <span class="hi-exp">{q["explanation"]["hi"]}</span>
            </div>
            """
        else:
            explanation_html = f"""
            <div class="explanation">
                💡 {q["explanation"]}
            </div>
            """

    return f"""
<html>
<head>
<style>

body {{
    width: 1080px;
    height: 1920px;
    margin: 0;
    font-family: Arial;
    background: linear-gradient(180deg, #020d18, #0a2a43);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: 90%;
    text-align: center;
}}

/* 🔥 LOGO (same as old) */
.logo {{
    width: 260px;
    height: 260px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 25px;
    box-shadow: 0 0 25px #00c3ff, 0 0 50px rgba(0,195,255,0.5);
    border: 4px solid rgba(255,255,255,0.2);
}}

/* ❓ QUESTION */
.question {{
    font-size: 50px;
    margin-bottom: 40px;
    line-height: 1.4;
}}

/* Hindi question */
.hi {{
    display: block;
    font-size: 30px;
    color: #cce6ff;
    margin-top: 10px;
}}

/* 🔘 OPTIONS */
.option {{
    font-size: 36px;
    margin: 15px 0;
    padding: 20px;
    border-radius: 12px;
    background: rgba(255,255,255,0.1);
    border: 2px solid #00c3ff;
}}

/* Hindi option */
.hi-opt {{
    display: block;
    font-size: 24px;
    color: #b3d9ff;
    margin-top: 5px;
}}

/* ✅ CORRECT ANSWER */
.correct {{
    background: #00ff9d;
    color: black;
    box-shadow: 0 0 20px #00ff9d;
    font-weight: bold;
}}

/* 💡 EXPLANATION (MATCH DESIGN) */
.explanation {{
    margin-top: 40px;
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #ffcc00;
    background: rgba(255,204,0,0.1);
    font-size: 30px;
    color: #ffcc00;
    box-shadow: 0 0 15px rgba(255,204,0,0.5);
}}

/* Hindi explanation */
.hi-exp {{
    display: block;
    font-size: 24px;
    color: #ffe599;
    margin-top: 10px;
}}

</style>
</head>

<body>
<div class="container">

    <!-- 🔥 LOGO -->
    <img class="logo" src="data:image/png;base64,{logo_base64}" />

    <!-- ❓ QUESTION -->
    <div class="question">
        Q{index+1}. {question}
    </div>

    <!-- 🔘 OPTIONS -->
    {options_html}

    <!-- 💡 EXPLANATION -->
    {explanation_html}

</div>
</body>
</html>
"""