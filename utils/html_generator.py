from services.video_service import get_logo_base64
def create_html(q, index, timer=3):
    question = q["question"]
    options = q["options"]

    logo_base64 = get_logo_base64()

    return f"""
<html>
<head>
<style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        height: 100vh;
        background: linear-gradient(180deg, #020d18, #0a2a43);
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    .container {{
        width: 90%;
        text-align: center;
    }}

    /* 🔥 LOGO */
    .logo {{
        width: 260px;              /* 🔥 bigger size */
        height: 260px;             /* keep equal for perfect circle */
        border-radius: 50%;        /* 🔥 makes it round */
        object-fit: cover;         /* avoids distortion */
        margin-bottom: 25px;        /* 🔥 premium glow */
        box-shadow: 0 0 25px #00c3ff, 0 0 50px rgba(0,195,255,0.5);

        /* 🔥 optional border */
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
</head>

<body>
    <div class="container">

        <!-- ✅ FIXED LOGO (BASE64) -->
        <img src="data:image/png;base64,{logo_base64}" class="logo"/>

        <div class="timer">⏳ {timer}</div>

        <div class="question">
            Q{index+1}. {question}
        </div>

        <div class="option">A. {options[0]}</div>
        <div class="option">B. {options[1]}</div>
        <div class="option">C. {options[2]}</div>
        <div class="option">D. {options[3]}</div>

        <div class="footer">
            🔥 Comment your answer!
        </div>

    </div>
</body>
</html>
"""