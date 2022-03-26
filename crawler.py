import requests
from bs4 import BeautifulSoup
import random as rd
import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class covid19:
    def __init__(self) -> None:
        self.__target = requests.get("https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php")
    def getDailyInfo(self):
        page = BeautifulSoup(self.__target.text,"html.parser")
        tempStr = ""
        totalInfected = page.find("h1","country_recovered mb-1 text-info").text
        newTotalInfected = totalInfected.replace('+','')
        # 日期
        info = page.find("div","col-lg-12 main")
        date = info.find_all("span")[1].text
        newDate = date.split(' ')[18]
        tempStr += newDate + '\n\n'
        # 本土確診
        domesticStr = page.find_all("span","country_confirmed_percent")[1].text
        newDomesticStr = domesticStr.replace('本土病例 ','')
        tempStr += '本土： ' + newDomesticStr + "\n"
        # 境外確診
        foreignStr = str(int(newTotalInfected) - int(newDomesticStr))
        tempStr += '境外： ' + foreignStr + "\n"
        # 死亡人數
        deathStr = page.find("span","country_deaths_change").text
        newDeathStr = deathStr.replace('+','')
        tempStr += '死亡： ' + newDeathStr
        return tempStr
