import requests
from bs4 import BeautifulSoup
target = requests.get("https://dashboard.heroku.com/apps/yeager-master/activity")
page = BeautifulSoup(target.text,"html.parser")
verStr = page.find_all("div","f5 gray")
print(verStr)
# ver = verStr[2]
# print(ver)