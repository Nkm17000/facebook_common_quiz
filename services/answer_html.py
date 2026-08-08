def answer_format(page, correct, correct_index, options):
    highlighted = []

    for i, opt in enumerate(options):
        if i == correct_index:
            highlighted.append(
                f"<div class='option correct'>✔ {opt}</div>"
            )
        else:
            highlighted.append(
                f"<div class='option'>{opt}</div>"
            )

    options_html = "".join(highlighted)

    return f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            font-family: Arial;
            height: 100vh;
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

        .title {{
            font-size: 50px;
            margin-bottom: 30px;
        }}

        .option {{
            margin: 20px 0;
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #00c3ff;
            font-size: 30px;
        }}

        .correct {{
            background: #00ff9d;
            color: black;
            box-shadow: 0 0 25px #00ff9d;
            font-weight: bold;
        }}
    </style>
    </head>

    <body>
        <div class="container">
            <div class="title">✅ Answer</div>
            {options_html}
        </div>
    </body>
    </html>
    """