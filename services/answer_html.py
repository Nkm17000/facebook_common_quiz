from services.video_service import get_logo_base64
def answer_html(q, index):
    logo_base64 = get_logo_base64()
    correct = q["options"][q["answer_index"]]

    options_html = ""
    for i, opt in enumerate(q["options"]):
        if i == q["answer_index"]:
            options_html += f'<div class="option correct">{chr(65+i)}. {opt}</div>'
        else:
            options_html += f'<div class="option">{chr(65+i)}. {opt}</div>'

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
            width: 120px;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 15px #00c3ff);
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
    </style>
    </head>

    <body>
        <div class="container">
            <img class="logo" src="data:image/png;base64,{logo_base64}" />

            <div class="question">
                Q{index+1}. {q["question"]}
            </div>

            {options_html}
        </div>
    </body>
    </html>
    """