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
import xml.etree.ElementTree as ET


def fetch_rss(url):
    '''Function to fetch RSS content'''
    response = requests.get(url)
    return response.text if response.status_code == 200 else None


def get_list_of_posts(xml_data):
    '''Function to get a list of posts'''
    root = ET.fromstring(xml_data)
    items = root.findall('.//item')
    return items


def post_already_exists(title, file_path):
    '''Function to check if post already exists'''
    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r', encoding='utf-8') as html_file:
        content = html_file.read()
        return title in content


def save_news_to_file(news, file_path):
    '''Function to save posts as HTML file'''
    with open(file_path, 'w', encoding='utf-8') as html_file:
        html_file.write('<html>\n<head>\n<title>RSS Feed</title>\n</head>\n<body>\n')

        for post in news:
            title = post.find('title').text
            # Checking if post does not already exist
            if not post_already_exists(title, file_path):
                url = post.find('link').text

                enclosure = post.find('.//enclosure')
                image_url = enclosure.get('url', '') if enclosure is not None else ''  # Checking if it exists

                description_element = post.find('description')
                description = description_element.text if description_element is not None else ''  # Checking if it exists

                # Limit description to 100 characters
                limited_description = description[:100] if description else ''

                html_file.write(f'<h2>{title}</h2>\n')
                html_file.write(f'<p><a href="{url}">Read more</a></p>\n')
                html_file.write(f'<img src="{image_url}" alt="{title}">\n')
                html_file.write(f'<p>{limited_description}</p>\n')

        html_file.write('</body>\n</html>')


rss_url = 'https://www.pravda.com.ua/rss/'
current_datetime = datetime.datetime.now().strftime('%Y-%m-%d')
news_folder_path = 'news'
# If news folder doesn't exist create one
if not os.path.exists(news_folder_path):
    os.makedirs(news_folder_path)
file_path = f'news/news_{current_datetime}.html'
rss_data = fetch_rss(rss_url)
posts = get_list_of_posts(rss_data)
save_news_to_file(posts, file_path)

