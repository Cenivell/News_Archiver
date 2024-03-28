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
import re
import sqlite3
import datetime
import requests


def fetch_rss(url):
    '''Function to fetch RSS content'''
    response = requests.get(url)
    return response.text if response.status_code == 200 else None


def get_list_of_posts(data):
    '''Function to get a list of posts'''
    pattern = r'<item>(.*?)</item>'
    posts = re.findall(pattern, data, re.DOTALL)
    return posts


def post_already_exists(cursor, title):
    '''Function to check if a post already exists'''
    cursor.execute("SELECT * FROM news WHERE title = ?", (title,))
    return cursor.fetchone() is not None


def save_news_to_file(news, file_path):
    '''Function to save posts as HTML file'''
    # Connecting to the database
    connection = sqlite3.connect('news_archive.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS news
                    (day DATETIME, title VARCHAR(50) PRIMARY KEY, link VARCHAR(50))''')

    with open(file_path, 'a', encoding='utf-8') as html_file:
        html_file.write('<html>\n<head>\n<title>RSS Feed</title>\n</head>\n<body>\n')

        for post in news:
            title_match = re.search('<title>(.*?)</title>', post)
            link_match = re.search('<link>(.*?)</link>', post)
            description_match = re.search('<description>(.*?)</description>', post)
            image_match = re.search('<enclosure\s+url="(.*?)"', post)
            if title_match and link_match:
                title = title_match.group(1)
                link = link_match.group(1)
                description = description_match.group(1) if description_match else ''
                image_url = image_match.group(1) if image_match else ''
                try:
                    # Check if the post already exists
                    if not post_already_exists(cursor, title):
                        cursor.execute("INSERT INTO news (day, title, link) VALUES (?, ?, ?)",
                                       (current_datetime, title, link))
                        html_file.write(f'<img src="{image_url}">\n')  # Add image tag
                        html_file.write(f'<h2>{title}</h2>\n')
                        html_file.write(f'<p><a href="{link}">Read more</a></p>\n')
                        html_file.write(f'<p>{description}</p>\n')
                        print("Post successfully added")
                    else:
                        print("Post already exists")
                except Exception as e:
                    print("An error occurred: ", e)
        html_file.write('</body>\n</html>')

    # Commit the changes
    connection.commit()
    # Close the cursor and connection
    cursor.close()
    connection.close()


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

