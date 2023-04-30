from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


def latest_news(channel_name):
    telegram_url = 'https://t.me/s/'
    url = telegram_url+channel_name
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    link = soup.find_all('a')
    url = link[-1]['href']
    url = url.replace('https://t.me/', '')
    channel_name, news_id = url.split('/')
    urls = []
    for i in range(10):
        urls.append(f'{channel_name}/{int(news_id) - 1}')
    return urls


@app.route('/',methods=["POST","GET"])
def main_page():
    urls = []
    if request.method == "GET":
        return render_template('index.html', url=urls)
    else:
        channel_name = request.form['adress']
        urls = latest_news(channel_name)
        return render_template('index.html', urls=urls)


if __name__ == '__main__':
    app.run()