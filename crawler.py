import requests
from bs4 import BeautifulSoup

class nHentaiSearcher:
    def __init__(self,title,tags):
        self.title = title
        self.tags = tags
    def searchTitle(self,num):
        response = requests.get("https://nhentai.net/g/" + num)
        soup = BeautifulSoup(response.text, "html.parser")
        self.title = [soup.find("span", {"class": "before"}).text,
        soup.find("span", {"class": "pretty"}).text,
        soup.find("span", {"class": "after"}).text]
