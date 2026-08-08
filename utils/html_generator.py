def create_html(question, index):
    labels = ["A", "B", "C", "D"]

    options_html = ""
    for i, opt in enumerate(question["options"]):
        options_html += f"""
        <div class="option">
            <b>{labels[i]}.</b> {opt}
        </div>
        """

    return f"""
    <html>
    <head>
    <style>
        body {{
            background: black;
            color: white;
            font-family: Arial;
            text-align: center;
        }}
        .question {{
            font-size: 50px;
            margin-top: 200px;
        }}
        .option {{
            font-size: 40px;
            margin: 20px;
        }}
    </style>
    </head>

    <body>
        <div class="question">Q{index+1}: {question["question"]}</div>
        {options_html}
    </body>
    </html>
    """