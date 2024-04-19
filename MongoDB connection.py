import requests
from pymongo import MongoClient
from datetime import datetime
import time
 
COINBASE_API_BASE_URL = 'https://api.coinbase.com/v2/prices'
CURRENCIES = [ 'LTC', 'DOT', 'TON','WBTC', 'AVAX', 'BCH', 'DAi', 'SHIB', 'LINK', 'XLM', 'BUSD', 'UNI', 'XMR', 'ETC', 'OKB',
              'FIL', 'MNT', 'LDO', 'APT', 'ARB', 'CRO', 'VET', 'NEAR', 'QNT', 'MKR', 'AAVE', 'GRT',
              'OP', 'ALGO', 'EGLD','BTC', 'ETH', 'USDT', 'XRP', 'BNB', 'USDC', 'DOGE', 'ADA', 'SOL', 'TRX', 'MATIC',
             'SAND', 'STX', 'THETA', 'EOS', 'XDC', 'XTZ', 'IMX', 'SNX', 'APE']
 
 
def fetch_crypto_prices(api_token, api_code):
    crypto_data = []
 
    for currency in CURRENCIES:
        url = f"{COINBASE_API_BASE_URL}/{currency}-CAD/spot"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'CB-ACCESS-SIGN': api_code,
        }
 
        response = requests.get(url, headers=headers)
 
        if response.status_code == 200:
            data = response.json()
            symbol = data.get('data', {}).get('base')
            price = float(data.get('data', {}).get('amount'))
            timestamp = datetime.utcnow().isoformat()
 
            crypto_data.append({
                'timestamp': timestamp,
                'symbol': symbol,
                'price': price
            })
        else:
            print(f"Failed to fetch {currency} price. Status code: {response.status_code}")
 
    return crypto_data
 
 
def save_data_to_db(data_to_save):
    try:
        client = MongoClient("mongodb+srv://richiegeorgethomas:RtchDBPhpfSIjZCI@cluster0.l5yxd1m.mongodb.net/")
        db = client['crypto']
        collection = db['crypto_table']
 
        result = collection.insert_many(data_to_save)
        print(f"{len(result.inserted_ids)} records inserted into MongoDB.")
    except Exception as e:
        print(f"An error occurred while saving data to MongoDB: {str(e)}")
 
 
def main():
    api_key = 'VadZPud6yXvGcJvz'
    api_secret = 'T7PWzvMMp5DXzYY5VJAxEVh0ovNLwt7c'
 
    while True:
        crypto_prices = fetch_crypto_prices(api_key, api_secret)
        save_data_to_db(crypto_prices)
        print('Data stored successfully')
 
        # Fetch data every 24 hours
        time.sleep(86400)  # Sleep for 24 hours
        print('Data fetching process completed')
 
 
if __name__ == "__main__":
    main()

