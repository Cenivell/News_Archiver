# АРХІВАТОР НОВИН
#
# Опис завдання:
# Потрбіно створити механізм збереження новин з сайту у файлову систему за певним форматом.
# Новина стрічка буде братися з RSS-стрічки сайту pravda.com.ua. (https://www.pravda.com.ua/rss/)
#
# Розробка:
# Програма повинна стягнути новини з RSS-стрічки, відфільтрувати їх за певними критеріями та зберегти у файлову систему,
# використовуючи певний формат збереження у HTML форматі (та відповідному файлі).
# Новини зберігаються у папці news, де файли формуються кожного дня (під час кожного запуску програми відповідно).
# Файли мають назву за форматом: news_YYYYMMDD.html, де YYYYMMDD - дата створення файлу.
#
# Технічне завдання:
# 1) Стягнути новини з RSS-стрічки сайту pravda.com.ua (https://www.pravda.com.ua/rss/).
# 2) Бібліотеки, окрім вбудованих: re, os, datetime, requests.
import os
import datetime
import requests


def fetch_rss(url):
    '''Function to fetch RSS content'''
    response = requests.get(url)
    return response.text if response.status_code == 200 else None


def save_news_to_file(news, file_path):
    '''Function to save news to a text file'''
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> \n')
        file.write(news)


# RSS feed URL
rss_url = 'https://www.pravda.com.ua/rss/'

# Fetching RSS content
rss_content = fetch_rss(rss_url)

if rss_content:
    # Saving news
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d')
    new_folder_path = 'news'
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    file_path = f'news/news_{current_datetime}.html'
    save_news_to_file(rss_content, file_path)
    print(f"News successfully saved to {file_path}")
else:
    print("Failed to fetch RSS content.")

