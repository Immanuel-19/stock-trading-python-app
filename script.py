import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY")

LIMIT = 1000

url = f'https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={MASSIVE_API_KEY}'
response = requests.get(url)

tickers = []
data = response.json()

while True:
    if 'results' not in data:
        print("API Error:", data)
        break

    for ticker in data['results']:
        tickers.append(ticker)

    next_url = data.get('next_url')

    if not next_url:
        break

    print('requesting next page...', next_url, data.keys())
    response = requests.get(next_url + f'&apiKey={MASSIVE_API_KEY}')
    data = response.json()


example_ticker = {
    'ticker': 'GMF',
    'name': 'State Street SPDR S&P Emerging Asia Pacific ETF',
    'market': 'stocks',
    'locale': 'us',
    'primary_exchange': 'ARCX',
    'type': 'ETF',
    'active': True,
    'currency_name': 'usd',
    'cik': '0001168164',
    'composite_figi': 'BBG000Q8QY82',
    'share_class_figi': 'BBG001SRXRB9',
    'last_updated_utc': '2026-11-17T07:10:15.801176212Z'
}

fieldnames = list(example_ticker.keys())
output_csv = 'tickers.csv'

with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames,
        extrasaction='ignore',
    )
    writer.writeheader()
    for t in tickers:
        row = {key: t.get(key, '') for key in fieldnames}
        writer.writerow(row)

print(f'Wrote {len(tickers)} rows to {output_csv}')