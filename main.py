import requests
from twilio.rest import Client

# SMS Client Keys
ACCOUNT_SID = "SID"
AUTH_TOKEN = "AUTH_TOKEN"
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

# Stock API Info
STOCK_API_KEY = "API_KEY"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK = "TSLA"
COMPANY_NAME = "Telsa Inc"
SHORT_COMPANY_NAME = "Tesla"
STOCK_PARAMETER = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

# News API Info
NEWS_API_KEY = "API_KEY"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMETER = {
    "q": SHORT_COMPANY_NAME,
    "searchIn": "title",
    "sortBy": "publishedAt",
    "apiKey": NEWS_API_KEY,
    "pageSize": 3,
    "page": 1,
}

# Stock API Request
stock_response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMETER)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]


# Stock Info
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])


# Sends message to user when stock increase/decreases by 5% between yesterday and the day before yesterday
def breaking_news():
    percentage = round(((yesterday_closing_price - day_before_yesterday_closing_price) /
                        day_before_yesterday_closing_price) * 100, 0)
    if abs(percentage) < 5:
        if percentage > 0:
            marker = "🔺"
        else:
            marker = "🔻"
        news_message = (f"{STOCK}: {marker}{percentage}\n" +
                        "---------------------------------------\n" + get_news())
        text = CLIENT.messages.create(
            body=news_message,
            from_="+18449812279",
            to="+14044555890",
        )


# Retrieves the first 3 related articles and formats the message to be sent
def get_news():
    # News API Request
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETER)
    news_response.raise_for_status()
    news_data = news_response.json()
    news = [f"Published at: {article["publishedAt"].split('T')[0]}\n"
            f"Publisher: {article["source"]["name"]}\n"
            f"Headline : {article["title"]}\n"
            f"Brief: {article["description"]}\n" for article in news_data["articles"]]
    news = "---------------------------------------\n".join(map(str, news))
    return news


breaking_news()