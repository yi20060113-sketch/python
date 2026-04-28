
from flask import Flask, request, render_template
import urllib.request
import json
import os
app = Flask(__name__)

# 建立題庫
zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요" : "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "Pikmin": "皮克敏",
    "家人": "가족",
    "愛": "사랑"
}




# homepage process
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        # 2. 讀取學生的問題
        question = request.form.get('question', '').strip()
        # 3. 查詢題庫的對應答案
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個詞的韓文對應。")
        # 4. 回傳答案給學生
        return render_template('ask.html', question=question, answer=answer)
    # GET 時給空白欄位
    return render_template('ask.html', question="", answer="")


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        stock_no = request.form.get('question', '').strip()

        if stock_no == "":
            return render_template('stock.html', question="", answer="請輸入股票代號")

        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={stock_no}"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0"
        })
    
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    
            if data.get("stat") == "OK" and len(data.get("data", [])) > 0:
                answer = data["data"][-1][6]
            else:
                answer = "查無資料，請確認股票代號"
    
    except Exception as e:
        answer = "系統錯誤：" + str(e)

        return render_template('stock.html', question=stock_no, answer=answer)

    return render_template('stock.html', question="", answer="")

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
