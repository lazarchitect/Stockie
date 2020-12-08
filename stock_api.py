from datetime import date
from requests import get
from time import sleep

API_KEY = "K7S4C5A154C6WILN"

def get_time_series_daily(ticker):
    SYMBOL = ticker
    HOST = "https://www.alphavantage.co"
    FUNCTION = "TIME_SERIES_DAILY"
    URL = HOST + "/query?function="+ FUNCTION + "&symbol=" + SYMBOL + "&apikey=" + API_KEY

    sleep(12)
    response_dict = get(URL).json()

    keys = response_dict.keys()
    today = date.today()
    yesterday = date(year=today.year, month=today.month, day=today.day-1)
    # return response_dict['Time Series (Daily)'][str(yesterday)]
    try:
        daily_data = response_dict['Time Series (Daily)']
    except KeyError:
        print(response_dict)
        return ""
    most_recent_date = list(daily_data.keys())[0]

    most_recent_data_dict = daily_data[most_recent_date]

    most_recent_data = ""
    most_recent_data += ticker + "\n"
    most_recent_data += most_recent_date + "\n"
    most_recent_data += "HIGH: " + most_recent_data_dict['2. high'] + "\n"
    most_recent_data += "LOW: " + most_recent_data_dict['3. low'] + "\n"
    #most_recent_data += "OPEN: " + most_recent_data_dict['1. open'] + "\n"
    most_recent_data += "CLOSE: " + most_recent_data_dict['4. close'] + "\n"
    most_recent_data += "---------------------------------------" + "\n"

    return most_recent_data

def get_stock_data(ticker_list):

    message = ""

    for ticker in ticker_list:
        most_recent_data = get_time_series_daily(ticker)

        message += most_recent_data

    return message

if __name__ == "__main__":
    ticker = input(">>")
    print(get_time_series_daily(ticker))
