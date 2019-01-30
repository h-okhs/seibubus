# coding: UTF-8
import requests
import re
import json
from ws.models import BusStatus
from bs4 import BeautifulSoup

url = "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110168&goalId=00110123"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.content, "lxml")

plots = soup.select("ul#resultList li")

for plot in plots:
    #  print(plot.encode('utf-8'))
    courseNames = plot.find_all("div", class_="courseName")
    for courseName in courseNames:
        print(re.sub(r'(＜|＞)', '', courseName.string))
    departureTimes = plot.find_all(
        "div", text=re.compile(u"発車まで"))
    for departureTime in departureTimes:
        print(re.sub(r'(\n|\t)', '', departureTime.string))
