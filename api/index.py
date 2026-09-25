from flask import Flask, jsonify
import requests

app = Flask(__name__)

# API Key Finnhub Anda
FINNHUB_API_KEY = 'darc61hr01qn6lve6mmg'

@app.route('/api/harga/<pair>')
def get_harga(pair):
    pair_upper = pair.upper()
    
    # Mengubah format pair ke standar Finnhub (menggunakan data OANDA)
    if pair_upper == 'EURUSD':
        finnhub_symbol = 'OANDA:EUR_USD'
        spread = 0.0002 # Spread simulasi 2 pips
    elif pair_upper == 'XAUUSD':
        finnhub_symbol = 'OANDA:XAU_USD'
        spread = 0.50   # Spread simulasi 50 cents
    else:
        # Jika Anda menambah pair lain (misal GBPUSD), otomatis jadi OANDA:GBP_USD
        finnhub_symbol = f'OANDA:{pair_upper[:3]}_{pair_upper[3:]}'
        spread = 0.0003

    # URL Endpoint API Finnhub
    url = f'https://finnhub.io/api/v1/quote?symbol={finnhub_symbol}&token={FINNHUB_API_KEY}'
    
    try:
        # Menarik data dari Finnhub
        response = requests.get(url)
        data = response.json()
        
        # 'c' adalah Current Price (Harga saat ini) dari Finnhub
        current_price = data.get('c')
        
        # Validasi jika pasar sedang tutup akhir pekan atau API limit
        if current_price is None or current_price == 0:
            return jsonify({"error": "Data tertunda / pasar tutup"})

        # Mengembalikan format JSON Bid & Ask ke Web HTML Anda
        return jsonify({
            "symbol": pair_upper,
            "bid": current_price,
            "ask": round(current_price + spread, 4)
        })
        
    except Exception as e:
        return jsonify({"error": "Gagal terhubung ke server harga"})

# Wajib ada untuk lingkungan Vercel Serverless
if __name__ == '__main__':
    app.run()