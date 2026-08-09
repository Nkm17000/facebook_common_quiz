from services.video_service import get_logo_base64

def create_html(q, index, timer=3):

    # ✅ HANDLE BOTH (dict + string)
    if isinstance(q["question"], dict):
        question = f'{q["question"]["en"]}<br><span class="hi">{q["question"]["hi"]}</span>'

        options = [
            f'{opt["en"]}<br><span class="hi-opt">{opt["hi"]}</span>'
            for opt in q["options"]
        ]
    else:
        question = q["question"]
        options = q["options"]

    logo_base64 = get_logo_base64()

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
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}}

.container {{
    width: 90%;
    text-align: center;
}}

/* 🔥 LOGO */
.logo {{
    width: 240px;
    height: 240px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 20px;
    box-shadow: 0 0 25px #00c3ff, 0 0 50px rgba(0,195,255,0.5);
    border: 4px solid rgba(255,255,255,0.2);
}}

/* ⏳ TIMER */
.timer {{
    font-size: 75px;
    color: #ffcc00;
    margin-bottom: 20px;
    font-weight: bold;
}}

/* ❓ QUESTION */
.question {{
    font-size: 46px;
    margin: 30px 0;
    line-height: 1.4;
}}

/* Hindi text */
.hi {{
    display: block;
    font-size: 30px;
    color: #cce6ff;
    margin-top: 10px;
}}

/* 🔘 OPTIONS */
.option {{
    margin: 18px 0;
    padding: 22px;
    border-radius: 18px;
    border: 2px solid #00c3ff;
    font-size: 32px;
    background: rgba(255,255,255,0.05);
    transition: 0.3s;
}}

/* Hover effect (for image rendering feel) */
.option:hover {{
    transform: scale(1.02);
    background: rgba(0,195,255,0.15);
}}

/* Hindi option */
.hi-opt {{
    display: block;
    font-size: 22px;
    color: #b3d9ff;
    margin-top: 5px;
}}

/* 🔥 FOOTER CTA */
.footer {{
    margin-top: 40px;
    font-size: 28px;
    color: #00ff9d;
    text-shadow: 0 0 10px #00ff9d;
}}

</style>
</head>

<body>

<div class="container">

    <!-- ✅ LOGO -->
    <img src="data:image/png;base64,{logo_base64}" class="logo"/>

    <!-- ⏳ TIMER -->
    <div class="timer">⏳ {timer}</div>

    <!-- ❓ QUESTION -->
    <div class="question">
        Q{index+1}. {question}
    </div>

    <!-- 🔘 OPTIONS -->
    <div class="option">A. {options[0]}</div>
    <div class="option">B. {options[1]}</div>
    <div class="option">C. {options[2]}</div>
    <div class="option">D. {options[3]}</div>

    <!-- 🔥 CTA -->
    <div class="footer">
        🔥 Comment your answer!
    </div>

</div>

</body>
</html>
"""