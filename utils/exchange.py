import requests
import pandas as pd


def fetch_moex_data(ticker, start_date="2023-01-01", end_date="2024-01-01"):
    url = f"https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/{ticker}.json"
    params = {
        "from": start_date,
        "till": end_date,
        "start": 0,
        "limit": 100,
        "sort_order": "desc",
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Ошибка при получении данных для {ticker}")
        return None

    data = response.json()
    columns = data["history"]["columns"]
    rows = data["history"]["data"]
    df = pd.DataFrame(rows, columns=columns)
    return df[["TRADEDATE", "CLOSE"]]


def fetch_moex_data_by_ticker_list(ticker_list: list):
    data = []
    for ticker in ticker_list:
        data.append(fetch_moex_data(ticker))
    return data
