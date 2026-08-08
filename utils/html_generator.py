def create_html(q, index):
    question = q["question"]
    options = q["options"]

    return f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: radial-gradient(circle at top, #0b2a3c, #020d18);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}

        .container {{
            width: 90%;
            text-align: center;
        }}

        .question-box {{
            border: 2px solid #00c3ff;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 0 20px #00c3ff;
            font-size: 40px;
            font-weight: bold;
        }}

        .options {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}

        .option {{
            border: 2px solid #00c3ff;
            border-radius: 15px;
            padding: 20px;
            font-size: 28px;
            box-shadow: 0 0 10px #00c3ff;
        }}
    </style>
    </head>

    <body>
        <div class="container">
            <div class="question-box">
                Q{index+1}. {question}
            </div>

            <div class="options">
                <div class="option">A. {options[0]}</div>
                <div class="option">B. {options[1]}</div>
                <div class="option">C. {options[2]}</div>
                <div class="option">D. {options[3]}</div>
            </div>
        </div>
    </body>
    </html>
    """