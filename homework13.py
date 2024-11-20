import requests
from bs4 import BeautifulSoup
import csv

def get_page(url):
    try:
        # Завантажує HTML-сторінку з заданого URL та повертає об'єкт BeautifulSoup для парсингу
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні: {e}")
        return None

def parse_news(soup):
    #  Парсить новини зі сторінки, переданої у вигляді об'єкта BeautifulSoup
    try:
        articles = soup.find_all('article')
        for article in articles:
            return [
                {
                    'title': article.find('h2').get_text(strip=True) if article.find('h2') else "Немає заголовка",
                    'link': article.find('a')['href'] if article.find('a') else "Немає посилання",
                    'date': article.find('time').get_text(strip=True) if article.find('time') else "Немає дати",
                    'summary': article.find('p').get_text(strip=True) if article.find('p') else "Немає опису"
                }

            ]
    except Exception as e:
        print(f"Помилка під час парсингу: {e}")
        return None

def save_to_csv(data, filename='news.csv'):
    # Зберігає дані в CSV файл
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'link', 'date', 'summary'])
            writer.writeheader()
            writer.writerows(data)
        print(f"Дані успішно збережені в {filename}")
    except Exception as e:
        print(f"Помилка під час збереження у файл: {e}")

if __name__ == '__main__':
    url = 'https://www.bbc.com/news'
    soup = get_page(url)
    if soup:
        news = parse_news(soup)
        if news:
            save_to_csv(news)

