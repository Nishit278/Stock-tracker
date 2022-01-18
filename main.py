import os
import requests 
from dotenv import load_dotenv
import smtplib
load_dotenv()

STOCK_API = os.getenv("STOCK_API_KEY")
NEWS_API = os.getenv("NEWS_API_KEY")
STOCK_ENDPOINT = os.getenv("STOCK_ENDPOINT")
USERNAME = os.getenv("MY_MAIL")
DEST_MAIL = os.getenv("DEST_MAIL")
PASSWORD = os.getenv("PASSWORD")




stocks = ["TATAMOTORS.BO", "TATAPOWER.BO", "RELIANCE.BO", "BHARTIARTL.BO"]
article_titles = ["Tata Motors", "tata power", "reliance", "bharti airtel"]
messages = []

def send_mail():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=USERNAME, password=PASSWORD)
        connection.sendmail(from_addr=USERNAME, to_addrs=DEST_MAIL, msg=f"Subject: Your daily stock update!\n\n{mail}")


def get_news(company):
    # COMPANY = company.split(".")[0].lower()
    # print(company)
    news_params = {
    "qInTitle": company,
    "sortyBy": "popularity",
    "apikey": NEWS_API,
    }
    news_res = requests.get("https://newsapi.org/v2/everything", params=news_params)
    # print(news_res.status_code)
    news = news_res.json()
    # print(news)
    articles = news["articles"][:2]

    for article in articles:
        source = article["source"]["name"]
        headline = article["title"]
        description= article["description"]
        url = article["url"]
        message = f"{headline}\n{url}\n{source}\n"
        messages.append(message)
        # print(message)

def get_quote(STOCK):
    stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey":STOCK_API,
    }
    res = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = res.json()["Time Series (Daily)"]
    # print(data)
    company = res.json()["Meta Data"]["2. Symbol"].split(".")[0]
    data_list = [values for (index, values) in data.items()]
    data_required = data_list[:2]

    yesterday_closing_price = float(data_required[0]["4. close"])
    day_before_yesterday_closing_price = float(data_required[1]["4. close"])
    p_l = round(yesterday_closing_price - day_before_yesterday_closing_price, 3)
    p_l_percentage = round(p_l/yesterday_closing_price*100, 2)
    # print(p_l_percentage)
    if p_l < 0:
        stock_report = f"{company}\nYesterday's Closing Price: {yesterday_closing_price}\nDay before yesterday's closing price: {day_before_yesterday_closing_price} \nLoss: {abs(p_l)} INR, {p_l_percentage}%\n"
        messages.append(stock_report)
    
    else:
        if p_l <= 10:
            stock_report = f"{company}\nYesterday's Closing Price: {yesterday_closing_price}\nDay before yesterday's closing price: {day_before_yesterday_closing_price} \nGain: {abs(p_l)} INR, {p_l_percentage}%\n"
            messages.append(stock_report)

        else:
            stock_report =   f"{company}\nYesterday's Closing Price: {yesterday_closing_price}\nDay before yesterday's closing price: {day_before_yesterday_closing_price} \nGain: {abs(p_l)} INR, {p_l_percentage}%\n"
            messages.append(stock_report)
            get_news(article_titles[stocks.index(stock)])

for stock in stocks:
    get_quote(stock)

mail = "\n".join(messages)
send_mail()