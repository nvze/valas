from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ! WAJIB DIGANTI !
# Masukkan API Key dari Dashboard Finnhub Anda di sini
FINNHUB_API_KEY = 'darbl8pr01qn6lve0s5gdarbl8pr01qn6lve0s60'

@app.route('/api/harga/<pair>')
def get_harga(pair):
    # Mengubah format pair standar menjadi format Finnhub (menggunakan data broker OANDA)
    if pair.upper() == 'EURUSD':
        finnhub_symbol = 'OANDA:EUR_USD'
        spread = 0.0002 # Spread simulasi 2 pips
    elif pair.upper() == 'XAUUSD':
        finnhub_symbol = 'OANDA:XAU_USD'
        spread = 0.50   # Spread simulasi emas 50 pips
    else:
        finnhub_symbol = f'OANDA:{pair}'
        spread = 0.0005

    # URL Endpoint Finnhub
    url = f'https://finnhub.io/api/v1/quote?symbol={finnhub_symbol}&token={FINNHUB_API_KEY}'
    
    try:
        # Mengambil data dari Finnhub
        response = requests.get(url)
        data = response.json()
        
        # Finnhub mengembalikan 'c' sebagai Current Price (Harga Saat Ini)
        current_price = data.get('c')
        
        # Jika current_price tidak ada atau 0, berarti pasar sedang tutup / simbol salah
        if not current_price:
            return jsonify({"error": "Data tidak ditemukan atau pasar tutup"})

        # Membuat output JSON yang sesuai dengan format HTML kita sebelumnya
        return jsonify({
            "symbol": pair.upper(),
            "bid": current_price,
            "ask": round(current_price + spread, 4)
        })
        
    except Exception as e:
        return jsonify({"error": "Gagal terhubung ke server harga"})