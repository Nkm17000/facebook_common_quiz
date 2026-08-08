def create_html(q, index):
    labels = ["A", "B", "C", "D"]

    options_html = ""
    for i, opt in enumerate(q["options"]):
        options_html += f"""
        <div class="option">
            <b>{labels[i]}.</b> {opt}
        </div>
        """

    return f"""
    <html>
    <head>
    <meta charset="UTF-8">

    <!-- ✅ Hindi Font Fix -->
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');

    body {{
        font-family: 'Noto Sans Devanagari', 'Mangal', Arial, sans-serif;
        background: black;
        color: white;
        margin: 0;
        padding: 40px;
    }}

    .container {{
        width: 100%;
        height: 100%;
    }}

    .question {{
        font-size: 60px;
        font-weight: bold;
        margin-bottom: 40px;
        line-height: 1.3;
    }}

    .option {{
        font-size: 45px;
        margin: 15px 0;
        padding: 10px 20px;
        border-radius: 10px;
        background: #1e1e1e;
    }}

    .footer {{
        position: absolute;
        bottom: 20px;
        right: 40px;
        font-size: 30px;
        color: gray;
    }}
    </style>

    </head>

    <body>
        <div class="container">

            <div class="question">
                Q{index + 1}. {q["question"]}
            </div>

            {options_html}

            <div class="footer">
                #Quiz #SSC #UPSC
            </div>

        </div>
    </body>
    </html>
    """