from services.video_service import get_logo_base64

def create_html(q, index, timer=3):

    # ✅ HANDLE BOTH (dict + string)
    if isinstance(q["question"], dict):
        question = f'{q["question"]["en"]}<br><span style="font-size:30px">{q["question"]["hi"]}</span>'

        options = [
            f'{opt["en"]}<br><span style="font-size:22px">{opt["hi"]}</span>'
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
    background: black;
    color: white;
    font-family: Arial;
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
    margin-bottom: 25px;
}}

.timer {{
    font-size: 70px;
    color: #ffcc00;
}}

.question {{
    font-size: 45px;
    margin: 40px 0;
}}

.option {{
    margin: 20px 0;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #00c3ff;
    font-size: 30px;
}}
</style>
</head>

<body>
<div class="container">

<img src="data:image/png;base64,{logo_base64}" class="logo"/>

<div class="timer">⏳ {timer}</div>

<div class="question">
Q{index+1}. {question}
</div>

<div class="option">A. {options[0]}</div>
<div class="option">B. {options[1]}</div>
<div class="option">C. {options[2]}</div>
<div class="option">D. {options[3]}</div>

</div>
</body>
</html>
"""