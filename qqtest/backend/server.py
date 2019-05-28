# -*- coding:utf-8 -*-

from flask import Flask, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import urllib,urllib2
import os
import time
import json

app = Flask(__name__)

image_path = "static/img"

def request_api(qqNumber):
    """从聚合接口获取测试结果
    """
    key = 'ea23f1332982a5b528bc61c0f64629d0'
    params = {
        'key': key,
        'qq': qqNumber
    }
    url = 'http://japi.juhe.cn/qqevaluate/qq'
    api = url + '?' + urllib.urlencode(params)
    req = urllib2.Request(api)
    res = urllib2.urlopen(req)
    return res.read()

def cut_words(str, fontSize, width):
    """根据输入的宽度来切割文字
    """
    font = ImageFont.truetype('Songti.ttf', fontSize)
    strList = []
    line = ''
    index = 0
    while True:
        if font.getsize(str[index:])[0] < width:
            strList.append(str[index:])
            break
        while font.getsize(line)[0] < width:
            line += str[index]
            index += 1
        strList.append(line)
        line = ''
    return strList

def generate_result(qqNumber):
    """根据输入的qq号码生成结果
    """
    resStr = request_api(qqNumber)
    res = json.loads(resStr)
    conclusion = res['result']['data']['conclusion']
    analysis = res['result']['data']['analysis']

    img = Image.open("qqtest.jpeg")
    draw = ImageDraw.Draw(img)
    typeface1 = ImageFont.truetype('Songti.ttf', 30)
    strList1 = cut_words(conclusion, 30, 1000)
    typeface2 = ImageFont.truetype('Songti.ttf', 24)
    strList2 = cut_words(analysis, 24, 1000)
    index = 0
    for str in strList1:
        draw.text((20, 20 + index * 30), str, fill=(255, 255, 255), font=typeface1)
        index += 1
    index = 0
    for str in strList2:
        draw.text((20, 30 + len(strList1) * 30 + 20 + index * 24), str, fill=(255, 255, 255), font=typeface2)
        index += 1
    name = int(time.time())
    path = image_path + '/' +  repr(name) + '.jpg'
    img.save(path)
    return path

@app.route('/application/qqtest/<path:req_path>', methods = ['GET'])
def index(req_path):
    return redirect('/' + req_path)

@app.route('/result/<qqNumber>')
def test_result(qqNumber):
    path = generate_result(qqNumber)
    return '/' + path

@app.route('/index.html')
def main():
    return redirect('/static/index.html')

if __name__ == '__main__':
    app.run(debug=True)