import json
import os
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html_to_markdown import convert_to_markdown


class RSS:
    def __init__(self, rss_url, cache_file="rss-cache.json"):
        self.rss_url = rss_url
        self.cache_file = cache_file

    def __get_last_update(self):
        if not os.path.isfile(self.cache_file):
            return 0

        with open(self.cache_file, "r") as f:
            cache_json = json.load(f)

        return cache_json.get(self.rss_url) or 0

    def __set_last_update(self, last_update):
        cache_json = {}
        if os.path.isfile(self.cache_file):
            with open(self.cache_file, "r") as f:
                cache_json = json.load(f)

        cache_json[self.rss_url] = last_update

        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, "w") as f:
            json.dump(cache_json, f)

    def __get_rss(self):
        req = urllib.request.Request(self.rss_url)
        r = urllib.request.urlopen(req)
        root = ET.fromstring(r.read())
        if root.find("channel") is None:
            raise ValueError("Not a RSS feed")
        return root.find("channel")

    def __handle_article(self, embed, article):
        title = article.find("title")
        description = article.find("description")

        if title is not None:
            embed["title"] = title.text
        if description is not None:
            embed["description"] = convert_to_markdown(description.text)

        categories = article.findall("category")
        if categories:
            embed["fields"] = []
            for cat in categories:
                embed["fields"].append({
                    "name": "Category",
                    "value": cat.text,
                    "inline": True
                })

    def get_news(self):
        last_newest = self.__get_last_update()
        newest = last_newest

        try:
            root = self.__get_rss()
        except ET.ParseError as e:
            print("Invalid RSS", e)
            return []

        title = root.find("title").text
        link = root.find("link").text
        # description = channel.find("description").text

        image_url = None
        if root.find("image") is not None:
            if root.find("image").find("url") is not None:
                image_url = root.find("image").find("url").text

        articles = root.findall("item")

        embeds = []

        for article in articles:
            pub_date = article.find("pubDate").text
            dt = parsedate_to_datetime(pub_date)
            timestamp = int(dt.timestamp())

            if timestamp > newest:
                newest = timestamp
            if timestamp <= last_newest:
                break

            embed = {
                "color": 0x5300a3,
                "author": {
                    "name": title,
                    "url": link
                }
            }
            if image_url:
                embed["author"]["icon_url"] = image_url

            self.__handle_article(embed, article)
            embeds.append(embed)

        self.__set_last_update(newest)
        return embeds

