import requests
from bs4 import BeautifulSoup

URL = "https://rezka.ag/animation/"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}


def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_="b-content__inline_item")
    anime = []
    for item in items:
        desc = item.find("div", class_="b-content__inline_item-link").find("div").getText().split(', ')
        anime.append({
            "title": item.find("div", class_="b-content__inline_item-link").find("a").getText(),
            "year": desc[0],
            "city": desc[1],
            "genre": desc[2],
            "link": item.find("div", class_="b-content__inline_item-link").find("a").get("href"),
            "status": item.find("span", class_="info").getText() if item.find("span",
                                                                              class_="info") is not None else "Онгоин"
        })
    return anime


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        answer = []
        for page in range(1, 2):
            html = get_html(f"{URL}page/{page}/")
            answer.extend(get_data(html.text))
        return answer
    else:
        raise Exception("Error in parser!")