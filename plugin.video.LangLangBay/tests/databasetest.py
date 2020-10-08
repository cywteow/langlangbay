# -*- coding: utf-8 -*-
import os
import sqlite3
from bs4 import BeautifulSoup
import re
import requests
import urlparse


class InternalDatabase:
    _connection = None
    _cursor = None
    _database = '../resources/data/drama.db'

    @classmethod
    def add(cls, values):
        cls._cursor.execute('INSERT INTO drama VALUES (?, ?, ?, ?)', values)

    @classmethod
    def connect(cls):
        if cls._connection is None:
            cls._connection = sqlite3.connect(cls._database)
            cls._connection.text_factory = str
            cls._cursor = cls._connection.cursor()
            cls._cursor.row_factory = sqlite3.Row
            cls.create()

    @classmethod
    def close(cls):
        if cls._connection is None:
            return

        cls._connection.commit()
        cls._cursor.close()
        cls._connection.close()
        cls._connection = None

    @classmethod
    def create(cls):
        cls._cursor.execute('CREATE TABLE IF NOT EXISTS drama ('
                            'path TEXT PRIMARY KEY ON CONFLICT IGNORE, '
                            'poster TEXT, '
                            'title TEXT, '
                            'plot TEXT)')

    @classmethod
    def fetchone(cls, path):
        cls._cursor.execute('SELECT * FROM drama WHERE path = ?', (path,))
        result = cls._cursor.fetchone()

        if result is None:
            return None
        else:
            result = dict(result)
            result.pop('path')
            return result

def getDescription(page):
    plot = ""
    try:
        headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
        response = requests.get(page, headers=headers)
        
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('div', class_="description")
        for element in description.contents:
            if element.name == "font":
                plot = plot[:-1]
                plot += element.string.strip() + "\n"
            elif element.name != "br":
                plot += element.strip() + "\n"
    except:
        plot = "Error Reading Description"
    return plot

imageUrl = "https://chinaq.img-ix.net/uploads/d"
response = requests.get("https://chinaq.tv/all.html")
response.encoding = 'utf-8'
document = BeautifulSoup(response.text, 'html.parser').find('ul', class_='drama_list')
InternalDatabase.connect()
for li in document.find_all('li'):
    a = li.find('a')
    title = a.string[:-3].strip()
    # print(title)
    if "https://chinaq.tv" in a['href']:
        location = urlparse.urlparse(a['href'].strip())
        path = location.path
    else:
        path = a['href']
    img = imageUrl+path[:-1]+".jpg"
    print(path)
    plot = getDescription("https://chinaq.tv"+path)

    InternalDatabase.add((path, img, title, plot))

InternalDatabase.close()

# response = requests.get("https://chinaq.tv/legend-of-miyue/")
# response.encoding = 'utf-8'
# document = BeautifulSoup(response.text, 'html.parser')
# h1 = document.find('div', id='contain').find('h1')
# print(h1.contents[0][:-3].strip())
