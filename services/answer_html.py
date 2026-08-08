def answer_format(page, correct):
    return f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            background: radial-gradient(circle at top, #0b2a3c, #020d18);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
        }}

        .box {{
            border: 3px solid #00ff9d;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 0 25px #00ff9d;
            text-align: center;
            color: white;
        }}

        .title {{
            font-size: 40px;
            margin-bottom: 20px;
        }}

        .answer {{
            font-size: 50px;
            color: #00ff9d;
        }}
    </style>
    </head>

    <body>
        <div class="box">
            <div class="title">Correct Answer</div>
            <div class="answer">Q{page}: {correct}</div>
        </div>
    </body>
    </html>
    """