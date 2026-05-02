from flask import Flask, request, render_template
import requests
import os
import urllib3

# 關閉 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
zh_ko_dict = {
    "你好": "안녕하세요",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個詞的韓文對應。")
        return render_template('ask.html', question=question, answer=answer)

    return render_template('ask.html', question="", answer="")

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    result = None
    stock_no = ""

    if request.method == 'POST':
        stock_no = request.form.get('question', '').strip()

        if stock_no == "":
            result = "請輸入股票代號"
            return render_template('stock.html', result=result, question=stock_no)

        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_no}.TW"

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            info = data["chart"]["result"][0]
            meta = info["meta"]

            result = {
                "name": stock_no + ".TW",
                "price": meta.get("regularMarketPrice", "-"),
                "open": meta.get("regularMarketDayLow", "-"),
                "high": meta.get("regularMarketDayHigh", "-"),
                "low": meta.get("regularMarketDayLow", "-"),
                "volume": meta.get("regularMarketVolume", "-")
            }

        except Exception as e:
            result = "系統錯誤：" + str(e)

    return render_template('stock.html', result=result, question=stock_no)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
