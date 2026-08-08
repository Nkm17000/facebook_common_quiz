def create_html(q, index):
    question = q["question"]
    options = q["options"]

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

        .timer {{
            font-size: 50px;
            color: #ffcc00;
            margin-bottom: 20px;
            animation: pulse 1s infinite;
        }}

        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
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
    </style>
    </head>

    <body>
        <div class="container">
            <div class="timer">⏳ 5</div>

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