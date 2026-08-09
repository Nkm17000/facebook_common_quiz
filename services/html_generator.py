from services.video_service import get_logo_base64

def create_html(q, index, timer=3):

    # ✅ FIX: handle bilingual structure
    question_en = q["question"]["en"]
    question_hi = q["question"]["hi"]

    options = q["options"]

    logo_base64 = get_logo_base64()

    return f"""
<div class="container">

<style>
.container {{
    width: 90%;
    text-align: center;
}}

/* 🔥 LOGO */
.logo {{
    width: 260px;
    height: 260px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 25px;
    box-shadow: 0 0 25px #00c3ff, 0 0 50px rgba(0,195,255,0.5);
    border: 4px solid rgba(255,255,255,0.2);
}}

.timer {{
    font-size: 70px;
    color: #ffcc00;
    margin-bottom: 20px;
}}

.question {{
    font-size: 45px;
    margin-bottom: 40px;
}}

.option {{
    margin: 20px 0;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #00c3ff;
    font-size: 30px;
}}

.footer {{
    margin-top: 40px;
    font-size: 25px;
    color: #00ff9d;
}}
</style>

<!-- ✅ LOGO -->
<img src="data:image/png;base64,{logo_base64}" class="logo"/>

<div class="timer">⏳ {timer}</div>

<div class="question">
    Q{index+1}. {question_en}<br/>
    <span style="color:#ccc">{question_hi}</span>
</div>

<div class="option">A. {options[0]['en']} / {options[0]['hi']}</div>
<div class="option">B. {options[1]['en']} / {options[1]['hi']}</div>
<div class="option">C. {options[2]['en']} / {options[2]['hi']}</div>
<div class="option">D. {options[3]['en']} / {options[3]['hi']}</div>

<div class="footer">
    🔥 Comment your answer!
</div>

</div>
"""