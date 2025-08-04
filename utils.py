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
