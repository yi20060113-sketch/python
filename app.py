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


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    result = None
    stock_no = ""

    if request.method == 'POST':
        stock_no = request.form.get('question', '').strip()

        if stock_no == "":
            return render_template('stock.html', result="請輸入股票代號")

        try:
            # 🔥 使用穩定 API
            url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_no}.tw"

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=10, verify=False)

            data = response.json()

            if "msgArray" in data and len(data["msgArray"]) > 0:
                stock = data["msgArray"][0]

                result = {
                    "name": stock.get("n", "未知"),
                    "price": stock.get("z", "-"),
                    "open": stock.get("o", "-"),
                    "high": stock.get("h", "-"),
                    "low": stock.get("l", "-"),
                    "volume": stock.get("v", "-")
                }
            else:
                result = "查無資料"

        except Exception as e:
            result = "系統錯誤：" + str(e)

    return render_template('stock.html', result=result, question=stock_no)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
