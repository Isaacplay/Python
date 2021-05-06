# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
import random
import json
from lxml import etree
from bs4 import BeautifulSoup
import requests
import xpinyin
import urllib2

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="interfaceby202151124" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType ==  'text':
            content = xml.find("Content").text
            if content[0:4] == u"查询天气":
                post = content[4:]
                pin = xpinyin.Pinyin()
                post2 = pin.get_pinyin(post,"")
                url = u"http://www.tianqi.com/" + post2
                
                # 代理ip
                #proxy_addr = "1.196.160.101:9999"
                #proxy = urllib2.ProxyHandler({'http': proxy_addr})
                #opener = urllib2.build_opener(proxy, urllib2.HTTPHandler)
                #urllib2.install_opener(opener)
                
                # 伪装报头
                #req = urllib2.Request(url)
                #req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0")
                a = urllib2.urlopen(url).read()
                soup = BeautifulSoup(a)
                ad = soup.findAll("b",limit=19)
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"您要查询的地点是："+post+u",现在的气温是："+ad[0].string+u" ℃,"+ad[1].string+u" , "+ad[2].string+u" , "+ad[3].string+u" , "+ad[4].string+u" . ")
            elif content.__contains__(u"笑话"):
                f = open("xiaohua.txt")
                line = f.readlines()
                return self.render.reply_text(fromUser,toUser,int(time.time()),line[int(random.random()*14)])                                                
            else:
                url_api = 'http://www.tuling123.com/openapi/api'
                data = {'key': "2b9858b2287b41dba59f9db4d4f9855d", 'info': content, }
                s = requests.post(url_api, data=json.dumps(data))
                info1 = json.loads(s.text)
                if info1['code'] == 100000:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),info1['text'])
                else :
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u"Monika出现问题了，错误代码是："+info1['code'])
                    
        elif msgTpe == "image":
            
            pass
        else:
            pass
      