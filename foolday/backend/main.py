# -*- coding:utf-8 -*-
#!/usr/bin/env python2

from flask import Flask, request
import urllib2
import json
import time
import os

app = Flask(__name__)
ip_list = []
qq_list = []

@app.route('/get_nick_name/<string:qqNumber>', methods=['GET'])
@app.route('/api/get_nick_name/<string:qqNumber>', methods=['GET'])
def get_nick_name(qqNumber):
    ret = {"status": "", "errMsg": "", "data": {}}
    if request.headers.get('remote-ip') in ip_list:
        ret['status'] = "fail"
        ret['errMsg'] = "说了只有一次机会你还想玩第二次？"
        return json.dumps(ret, ensure_ascii=False), 200
    url = 'http://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins=' + qqNumber
    header = {
        "User-Agent": 'Mozilla/5.0 (Linux; U; Android 4.4.1; zh-cn; R815T Build/JOP40D) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.5 Mobile Safari/533.1'
    }
    req  = urllib2.Request(url=url, headers=header)
    try:
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        data = response.replace('portraitCallBack(', '').replace('_Callback(', '').strip().rstrip(');')
        dataObj = json.loads(data, encoding="gbk")
        
        ip = request.headers.get('remote-ip')
        ip_list.append(ip)
        qq_list.append({
            "nickName": dataObj.get(qqNumber, [''] * 6)[6],
            "qq": qqNumber,
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
        })
        ret['status'] = "success"
        ret['data'] = {
            'count': len(qq_list),
            'nickName': dataObj.get(qqNumber, [''] * 6)[6]
        }
        return json.dumps(ret, ensure_ascii=False), 200
    except Exception as e:
        print str(e)
        return "Server Error", 500

@app.route('/get_all_list', methods=['GET'])
@app.route('/api/get_all_list', methods=['GET'])
def get_all_list():
    ret = {"status": "success", "errMsg": "", "data": qq_list}
    return json.dumps(ret, ensure_ascii=False), 200

@app.route('/fool/static/<path:path>', methods=['GET'])
def static_file(path):
    if not os.path.isfile('static/' + path):
        return "Not found", 404
    with open('static/' + path) as file:
        return file.read(), 200

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    with open('dist/index.html') as file:
        return file.read(), 200

if __name__ == "__main__":
    app.run(debug=True)