from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown
import json
import os


class Logger:
    name = ""

    def set_logger_name(self, name):
        self.name = name

    def __send(self, level, msg):
        self.name = self.name or self.__class__.__name__

        print(f"[{datetime.now().strftime("%D %H:%M:%S")}] [{self.name}/{level}]: {msg}")

    def debug(self, msg): self.__send("DBUG", msg)
    def info(self, msg): self.__send("INFO", msg)
    def warn(self, msg): self.__send("WARN", msg)
    def error(self, msg): self.__send("EROR", msg)
    def critical(self, msg): self.__send("CRIT", msg)


def find_callsign(callsign):
    file_path = "data/callsigns.json"
    if not os.path.exists(file_path):
        return None

    callsign = callsign.upper()

    with open(file_path) as f:
        calls = json.load(f)

    for call in calls:
        start, end, name = call["start"], call["end"], call["name"]

        if len(callsign) <= len(start):
            continue

        prefix = callsign[:len(start)]
        next_char = callsign[len(start)]

        if next_char.isdigit() and start <= prefix <= end:
            return name

    return None


def get_r4uab_articles():
    url = "https://r4uab.ru/feed/"

    with urllib.request.urlopen(url) as response:
        data = response.read()

    root = ET.fromstring(data)

    articles = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        pub_date = item.find("pubDate").text
        categories = [c.text for c in item.findall(".//category")]
        post_id = item.find("wp:post-id", {'wp': 'com-wordpress:feed-additions:1'}).text
        articles.append({
            "post_id": post_id,
            "title": title,
            "link": link,
            "pub_date": pub_date,
            "categories": categories
        })
    return articles


def get_r4uab_article(post_id):
    with urllib.request.urlopen(f"https://r4uab.ru/?p={post_id}") as response:
        data = response.read().decode()

    soup = BeautifulSoup(data, "html.parser")

    image_url = soup.find("img", class_="size-colormag-featured-image").attrs["src"]
    content_html = soup.find("div", class_="entry-content")

    content_html = str(content_html).split("<span")[0]

    content = convert_to_markdown(content_html)
    return {"image_url": image_url, "content": content}


def get_new_r4uab_articles():
    if os.path.exists("cache/r4uab_articles.json"):
        with open("cache/r4uab_articles.json", "r") as f:
            already_sent = json.load(f)
    else:
        already_sent = []

    new_articles = [
        a for a in get_r4uab_articles()
        if a["post_id"] not in already_sent
    ]

    already_sent.extend([a["post_id"] for a in new_articles])

    if not os.path.exists("cache"): os.mkdir("cache")
    with open("cache/r4uab_articles.json", "w") as f:
        json.dump(already_sent, f)

    return new_articles
