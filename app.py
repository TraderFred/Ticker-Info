from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape halted stocks from NASDAQ
def get_halted_stocks():
    url = "https://www.nasdaqtrader.com/trader.aspx?id=TradeHalts"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    halted_stocks = []
    table = soup.find("table", {"class": "datatable"})
    if table:
        rows = table.find_all("tr")[1:]  # Skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 4:
                halted_stocks.append({
                    "Symbol": cols[0].text.strip(),
                    "Company": cols[1].text.strip(),
                    "Reason": cols[3].text.strip(),
                    "Time": cols[4].text.strip()
                })
    return halted_stocks

@app.route('/')
def index():
    halted_stocks = get_halted_stocks()
    return render_template('index.html', halted_stocks=halted_stocks)

if __name__ == '__main__':
    app.run(debug=True)
