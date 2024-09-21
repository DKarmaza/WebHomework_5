import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys


API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"

#запит до  ПриватБанку
async def fetch_exchange_rate(session, date: str):
    url = API_URL.format(date=date)
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Error: Received status code {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching data for {date}: {e}")
        return None

#обробка отриманих даних
def process_exchange_data(data):
    date = data['date']
    rates = data.get('exchangeRate', [])

    result = {
        date: {
            'EUR': {},
            'USD': {}
        }
    }
    for rate in rates:
        if rate.get('currency') == 'EUR':
            result[date]['EUR'] = {
                'sale': rate.get('saleRate', 'N/A'),
                'purchase': rate.get('purchaseRate', 'N/A')
            }
        if rate.get('currency') == 'USD':
            result[date]['USD'] = {
                'sale': rate.get('saleRate', 'N/A'),
                'purchase': rate.get('purchaseRate', 'N/A')
            }

    return result

#отримання курсів валют за кілька днів
async def get_exchange_rates(days: int):
    results = []
    async with aiohttp.ClientSession() as session:
        for i in range(days):
            date = (datetime.now() - timedelta(days=i+1)).strftime('%d.%m.%Y')
            data = await fetch_exchange_rate(session, date)
            if data:
                result = process_exchange_data(data)
                results.append(result)
    return results

#функція для запуску
def main():
    try:
        days = int(input("Write number of days (must be between 1 and 10): "))
        if days < 1 or days > 10:
            raise ValueError("Number of days must be between 1 and 10.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    #Запуск логіки та виведення результатів
    results = asyncio.run(get_exchange_rates(days))
    print(results)

if __name__ == "__main__":
    main()
