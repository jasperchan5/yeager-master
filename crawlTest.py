import requests

from bs4 import BeautifulSoup

num = input()
response = requests.get("https://nhentai.net/g/" + num)
soup = BeautifulSoup(response.text, "html.parser")

title = [soup.find("span", {"class": "before"}),
            soup.find("span", {"class": "pretty"}),
            soup.find("span", {"class": "after"})]
for i in range(0,3):
    target = title[i].text
    print(target)