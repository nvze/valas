from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/harga/<pair>')
def get_harga(pair):
    pair_upper = pair.upper()
    
    # Menyesuaikan simbol dengan format Yahoo Finance
    if pair_upper == 'EURUSD':
        yahoo_symbol = 'EURUSD=X'
        spread = 0.0002
    elif pair_upper == 'XAUUSD':
        yahoo_symbol = 'XAUUSD=X'  # Simbol Emas Spot di Yahoo
        spread = 0.50
    else:
        # Jika Anda menambahkan GBPUSD, USDJPY, dll
        yahoo_symbol = f'{pair_upper}=X'
        spread = 0.0005

    # Endpoint rahasia Yahoo Finance Chart API (Gratis & Tanpa Key)
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}?region=US&lang=en-US'
    
    # Yahoo Finance mewajibkan "User-Agent" agar tidak diblokir
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Mengambil harga saat ini (regularMarketPrice) dari struktur JSON Yahoo
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
        # Menampilkan detail error jika gagal agar mudah dilacak
        return jsonify({"error": f"Gagal mengambil data dari Yahoo"})

if __name__ == '__main__':
    app.run()