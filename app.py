import random
from flask import Flask, render_template, jsonify
# Hapus tanda pagar (#) di bawah ini jika Anda sudah mendaftar di metaapi.cloud
# import asyncio
# from metaapi_cloud_sdk import MetaApi

app = Flask(__name__)

# Konfigurasi MetaApi 
# META_API_TOKEN = 'isi_token_metaapi_disini'
# ACCOUNT_ID = 'isi_id_akun_mt4_disini'
# api = MetaApi(META_API_TOKEN)

@app.route('/')
def index():
    # Menampilkan file index.html yang ada di folder templates/
    return render_template('index.html')

@app.route('/api/harga/<pair>')
def get_harga(pair):
    """
    ENDPOINT API: Web di HP Anda akan meminta data ke URL ini setiap 1 detik.
    """
    
    # --- BLOK KODE MT4 ASLI (Gunakan ini jika token MetaApi sudah Anda miliki) ---
    # async def fetch_mt4():
    #     account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
    #     await account.wait_connected()
    #     connection = account.get_rpc_connection()
    #     await connection.connect()
    #     return await connection.get_symbol_price(pair)
    # 
    # try:
    #     data = asyncio.run(fetch_mt4())
    #     return jsonify({"symbol": pair, "bid": data['bid'], "ask": data['ask']})
    # except Exception as e:
    #     return jsonify({"error": str(e)})
    # ----------------------------------------------------------------------------

    # --- SIMULASI HARGA LIVE (Agar web bisa langsung dites bergerak di HP) ---
    # Jika EURUSD harga dasar sekitar 1.1050, jika pair lain set ke 150.00
    base_price = 1.1050 if pair.upper() == 'EURUSD' else 150.20
    fluctuation = random.uniform(-0.0005, 0.0005)
    
    bid_price = round(base_price + fluctuation, 4)
    ask_price = round(bid_price + 0.0002, 4) # Spread simulasi
    
    return jsonify({
        "symbol": pair.upper(),
        "bid": bid_price,
        "ask": ask_price
    })

if __name__ == '__main__':
    app.run(debug=True)
