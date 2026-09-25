from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/harga/<pair>')
def get_harga(pair):
    pair_upper = pair.upper()
    
    # Menyesuaikan simbol dengan format Yahoo Finance
    if pair_upper == 'USDIDR':
        yahoo_symbol = 'IDR=X'
        spread = 15.0  # Spread simulasi 15 Rupiah
    elif pair_upper == 'XAUUSD':
        yahoo_symbol = 'XAUUSD=X'
        spread = 0.50
    else:
        yahoo_symbol = f'{pair_upper}=X'
        spread = 0.0005

    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}?region=US&lang=en-US'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        result = data['chart']['result'][0]
        current_price = result['meta']['regularMarketPrice']
        
        if not current_price:
            return jsonify({"error": "Harga tidak ditemukan di server"})

        return jsonify({
            "symbol": pair_upper,
            "bid": current_price,
            "ask": round(current_price + spread, 4)
        })
        
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil data dari Yahoo"})

if __name__ == '__main__':
    app.run()