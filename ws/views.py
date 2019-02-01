from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
import json
import re
from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters
from ws.models import BusStatus
from ws.selealizer import BusStatusSerializer
from collections import OrderedDict
from django.http import HttpResponse


class BusStatusViewSet(viewsets.ModelViewSet):
    queryset = BusStatus.objects.all()
    serializer_class = BusStatusSerializer


def render_json_response(request, data, status=None):
    """response を JSON で返却"""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get('callback')
    if not callback:
        callback = request.POST.get('callback')  # POSTでJSONPの場合
    if callback:
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(
            json_str, content_type='application/javascript; charset=UTF-8', status=status)
    else:
        response = HttpResponse(
            json_str, content_type='application/json; charset=UTF-8', status=status)
    return response


@csrf_exempt
def busstatus_list(request):
    """書籍と感想のJSONを返す"""
    busstatuses = []
    url = "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110168&goalId=00110123"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "lxml")
    plots = soup.select("ul#resultList li")
    message = ''
    for plot in plots:
        courseNames = plot.find_all("div", class_="courseName")
        courseName = ''
        departureAt = ''
        for courseName in courseNames:
            courseName = re.sub(r'(＜|＞)', '', courseName.string)
        if (len(courseName) == 0):
            continue
        departureTimes = plot.find_all(
            "div", text=re.compile(u"発車まで"))
        for departureTime in departureTimes:
            departureAt = re.sub(r'(\n|\t)', '', departureTime.string)
        if (len(departureAt) == 0):
            continue

        message += courseName + ' ' + departureAt + ':'

        # busstatus_dict = OrderedDict([
        #     ('line', courseName),
        #     ('departureAt', departureAt)
        # ])
        # busstatuses.append(busstatus_dict)

#    data = OrderedDict([('busstatuses', busstatuses)])
    if (message == ''):
        message = '30分以内に発車するバスはありません。'
    return render_json_response(request, {'fullfillmentText', message)
