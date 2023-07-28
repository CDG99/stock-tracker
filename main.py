import requests
from twilio.rest import Client
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

# the if-statement would need to be un-commented out if this was to be hosted so that it could check for a specified
# percent change.

# this is where the company is selected
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

PARAMS_STOCK = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv('api_key_stock')
}

PARAMS_NEWS = {
    "q": "tesla",
    "from": dt.date.today(),
    "sortBy": "publishedAt",
    "apiKey": os.getenv('api_key_news')
}

# find the percent change
stock_response = requests.get(url="https://www.alphavantage.co/query?", params=PARAMS_STOCK)
stock_response.raise_for_status()
stock_data = stock_response.json()
print(stock_data)
one_day_ago_close = float(stock_data['Time Series (Daily)'][str(dt.date.today() - dt.timedelta(days=1))]["4. close"])
two_days_ago_close = float(stock_data['Time Series (Daily)'][str(dt.date.today() - dt.timedelta(days=2))]["4. close"])
change = round(((one_day_ago_close - two_days_ago_close) / two_days_ago_close) * 100, 2)


# retrieve the top 3 articles related to the chosen company
news_response = requests.get(url="https://newsapi.org/v2/everything?", params=PARAMS_NEWS)
news_response.raise_for_status()
news_data = news_response.json()
news_names = []
news_title = []
news_brief = []
for num in range(0, 3):
    news_names.append(news_data['articles'][num]["source"]["name"])
    news_title.append(news_data['articles'][num]["title"])
    news_brief.append(news_data['articles'][num]["description"])

# text the stock change and the news articles to yourself
client = Client(os.getenv('account_sid'), os.getenv('auth_token'))
for num in range(0, 3):
    message = client.messages.create(
        body=f"\n{COMPANY_NAME}: {change}% \n{news_names[num]}: {news_title[num]} \nBrief: {news_brief[num]} ",
        from_=os.getenv('twilio_number'),
        to=os.getenv('personal_number'),
    )
