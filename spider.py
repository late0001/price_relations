# * coding=utf-8 *
#https://www.ds54.xyz/torrent/ce2551480accf08f3937865dd00ec965ad1fcb83.torrent
import urllib
#import urllib2
#import urllib.request
from urllib import request, parse
import re
import os
import io
import sys
import imp
import time
from urllib.parse import urlparse
import base64
#import http.cookiejar
import http.cookiejar
import socket
import ssl
import random
from dbhelp import DbHelp 
import json
import requests
from encode import multipart_encode
from poster.streaminghttp import register_openers
import httpx
#import socket 
#socket.setdefaulttimeout(5.0)
total_item=0
cur_item_no=0
allpic_x = 0
opener = 0


class Spider:
    def __init__(self):
        # 初始化起始页位置
        self.page = 1
        # 爬取开关，如果为True继续爬取
        self.switch = True
        #通过CookieJar()类构建一个cookieJar对象，用来保存cookie的值
        cookie = http.cookiejar.CookieJar()
        cookie.clear()
        self.cookie = cookie
        self.cookies = httpx.Cookies()
        #通过HTTPCookieProcessor()处理器类构建一个处理器对象，用来处理cookie
        #参数就是构建的CookieJar()对象
        cookie_handler = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(cookie_handler, request.HTTPHandler)
        #opener = request.build_opener(cookie_handler) 
        request.install_opener(opener) 
        self.opener = opener
        self.db = DbHelp()
        
    def mymkdirs(self, spath):
        if(not os.path.exists(spath)):
            os.makedirs(spath)    

    def printDelimiter(self):
        print ('-'*80);
        
    #打开一个网页
    def getHtml(self, url):
        global cur_item_no
        #try:
        time.sleep(1)
        page = urllib.urlopen(url)
        html = page.read()
        #except IOError:
        #    print 'frequency too high ,please try again late'
        print ('=================================')
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url', url)
        print ('http status:',page.getcode())
        return html
    
    def post(self, url, data):
        global cur_item_no
        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
        #'accept-encoding': 'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9', 
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cache-Control':'max-age=0', 
       #'referer': 'https://cn.torrentkitty.app/search/',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'none',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = headers.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        deal_data = bytes(parse.urlencode(data), encoding='utf8')
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = headers)
                req = request.Request(url= url, data= deal_data, headers = headers, method='POST')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=2)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s', url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('=================================')
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('post url: ', url)
        print ('http status:',page.getcode())
        return html
    
    def spr_post(self, url, data, timeout = 2):
        global cur_item_no
        headers = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       #'Host': 'certsign.realtek.com',
       #'Origin': 'https://certsign.realtek.com',
       #'Content-Type': 'application/x-www-form-urlencoded',
       #'Referer': 'https://certsign.realtek.com/SMSOTP.jsp',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'same-origin',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        #'Cookie': '_pk_ses.2.a6f7=1; JSESSIONID=50CB9A0B10EAC7F72F84B66923CC2E21; _pk_id.2.a6f7=a596b944cc4c029a.1620272182.15.1623237968.1623236515.'
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        deal_data = bytes(parse.urlencode(data), encoding='utf8')
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url, data=deal_data, headers = headers, method='POST')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('='*80)
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url: ', url)
        print ('http status:',page.getcode())
        print ('='*80)
        return html

    def spr_post_h2(self, url, headers, data):
        for i in range(1,15):
            try:
                with httpx.Client(headers=headers, params=data, http2=True) as client:
                    # with 内部请求共用一个client，参数也共用
                    # 替换client的参数
                    #headers = {'X-Custom': 'from-request'}
                    r = client.post(url, headers=headers, params=data, cookies = self.cookies)
                    self.cookies.update(r.cookies)
                    print ('url: ', url)
                    print ('http status:', r.status_code)
                    print ('cookies', r.cookies)
                    #print ('self.cookies', self.cookies)
                    return r
            except (httpx.ConnectTimeout, httpx.ReadTimeout) as e:
                print("Error occuer:", e )
                print("retry get url: %s\n Count: %d"% (url, i))
        if(i >= 15):
            print("failed, retry 15 times can not get response text")    

    def spr_post_h11(self, url, headers, data, timeout = 2):
        global cur_item_no
       
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        deal_data = bytes(parse.urlencode(data), encoding='utf8')
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                #req = request.Request(url, data=deal_data, headers = headers, method='POST')     
                req = request.Request(url, data=deal_data, method='POST')   
                req.add_header('Content-type', 'application/x-www-form-urlencoded')          
                req.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
                req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                #html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('='*80)
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no += 1
        print ('get url: ', url)
        print ('http status:', page.getcode())
        print ('='*80)
        return page

    def spr_post(self, url, data, header = None, timeout = 2, http2 = False):
        global cur_item_no
        headers = {
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           #'Host': 'certsign.realtek.com',
           #'Origin': 'https://certsign.realtek.com',
           #'Content-Type': 'application/x-www-form-urlencoded',
           #'Referer': 'https://certsign.realtek.com/SMSOTP.jsp',
           'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
           'sec-ch-ua-mobile': '?1',
           'sec-fetch-dest':'document',
           'sec-fetch-mode':'navigate',
           'sec-fetch-site': 'same-origin',
           'sec-fetch-user':'?1',
           'upgrade-insecure-requests':'1',
           'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
        #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            #'Cookie': '_pk_ses.2.a6f7=1; JSESSIONID=50CB9A0B10EAC7F72F84B66923CC2E21; _pk_id.2.a6f7=a596b944cc4c029a.1620272182.15.1623237968.1623236515.'
        }
            # 用于模拟http头的User-agent
        ua_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        #user_agent = random.choice(ua_list)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        #opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        #deal_data = bytes(parse.urlencode(data), encoding='utf8')
        if(http2):
            r = self.spr_post_h2(url, headers, data)
        else:
            r = self.spr_post_h11(url, headers, data)
        return r 

    def spr_post_gethtml(self, url, data, timeout = 2, http2 = False):
        r = self.spr_post(url, data, timeout=timeout, http2=http2)
        if(http2):
            return r.text
        return r.read()  
 
    


    def spr_get_h2(self, url, headers, timeout =2):
        with httpx.Client(headers=headers, http2=True) as client:
            # with 内部请求共用一个client，参数也共用
            # 替换client的参数
            #headers = {'X-Custom': 'from-request'}
            headers.update({'X-Custom': 'from-request'})
            while True:
                try:
                
                    r = client.get(url, headers=headers, cookies = self.cookies)
                    break
                except httpx.ConnectTimeout as e:
                    print(e)
                    print("请求超时")
                    time.sleep(1)
                except httpx.ConnectError as e:
                    print(e)
                    time.sleep(1)

            self.cookies.update(r.cookies)
            print ('http status:', r.status_code)
            print ('encoding:', r.encoding)
            print ('cookies: ', r.cookies)
            #print ('self.cookies', self.cookies)
            return r

    def spr_get_h11(self, url, headers, timeout = 2):
        global cur_item_no
        
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        print ('='*80)
        print ('get url: ', url)
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url,  headers = headers, method='GET')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                #html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
                timeout = 2 + fails if timeout < 6 else 6 
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        #print ('get url: ', url)
        print ('http status:',page.getcode())
        print ('='*80) 
        return page

    def spr_get(self, url, header, timeout=2, http2=False):
        global cur_item_no
        headers = {
       #'referer': 'https://cn.torrentkitty.app/search/',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       #'Host': 'certsign.realtek.com',
       #'Origin': 'https://certsign.realtek.com',
       #'Content-Type': 'application/x-www-form-urlencoded',
       #'Referer': 'https://certsign.realtek.com/SMSOTP.jsp',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'same-origin',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        #'Cookie': '_pk_ses.2.a6f7=1; JSESSIONID=50CB9A0B10EAC7F72F84B66923CC2E21; _pk_id.2.a6f7=a596b944cc4c029a.1620272182.15.1623237968.1623236515.'
        }
        if(header != None):
            headers.update(header)
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        print ('='*80)
        print ('get url: ', url)

        if http2 == True:
            print(" http2 request: ", url)
            r = self.spr_get_h2(url, headers, timeout)
        else:
            r = self.spr_get_h11(url, headers, timeout)
        return r

    def spr_get_html(self, url, header=None , timeout = 2, http2 =False):
        r = self.spr_get(url, header, timeout, http2)
        if(http2):
            return r.text
        else:
            return r.read()


    def getHtml3(self, url):
        global cur_item_no
        heads = {
       #'referer': 'https://cn.torrentkitty.app/search/',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
       'sec-ch-ua-mobile': '?0',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'none',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url )               
                req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=2)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s', url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('=================================')
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url: ', url)
        print ('http status:',page.getcode())
        return html
    
    def callbackDownload(self, blocknum, blocksize, totalsize):
        '''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        sys.stdout.write('#####'+ '->' + '\b\b\b\b\b')
        sys.stdout.write("%.2f%%"% percent)
        #print "%.2f%%"% percent
    
    def autoDown(self, url, filename, dcallback):
        # try:
            # urllib.urlretrieve(url, filename, dcallback)
        # except urllib.ContentTooShortError,IOError:
            # print 'Network is not good reloading.'
            # time.sleep(1)
            # autoDown(url, filename, dcallback)
        # finally:
            # urllib.urlcleanup()
        #url='http://www.facebook.com/'
        heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
    'Accept-Language':'zh-cn,zh;q=0.5', 
    'Cache-Control':'max-age=0', 
    'Connection':'keep-alive', 
    'Keep-Alive':'115', 
    'Referer':url, 
    'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'}
        fails = 0
        while True:
            try:
                if fails >= 20:
                    break
                print ("get url:" + url)
                req = urllib2.Request(url, headers = heads)
                print (u'开始发起 %d 次请求: ' % fails)
                response = urllib2.urlopen(req,data=None, timeout=3)
                page = response.read()
            except:
                fails += 1
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            else:
                break
        #response=urllib2.Request(url)
        #rs=urllib2.urlopen(response)
        f=open(filename,'wb')#以二进制写模式打开,rb+:以二进制读写模式打开 
        f.write(page)
        f.close()
    
    #获取网页里的图片
    def getImg2_(self, html):
        global allpic_x
        reg = r'<dd>(.+?\.jpg)<dd>'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        s = set(imglist) #用一个集合去除重复
        pic_savepath = r'E:\myzhpic\x2'
        #os.path.join(pic_savepath, )
        #x = 0
        mymkdirs(pic_savepath)
        for imgurl in s:
            print (u"%s --> %s.jpg" % (imgurl, allpic_x))
            autoDown(imgurl, '%s\\%s.jpg' % (pic_savepath, allpic_x), self.callbackDownload)
            print 
            allpic_x+=1
            time.sleep(1)
        
    #获取单个网页里的图片 "/siwameitui/201607/0FQ93P2016.shtml"
    def getSingle(self, shtml):
        html = getHtml(shtml)
        #print '++++++++++++++++++++++++++++++++++++++++'
        #print html
        #print '++++++++++++++++++++++++++++++++++++++++'
        getImg(html)
    
    #获取图片
    def getImg(self, imgurl):
        global allpic_x
        print ("get "+ imgurl)
        #/picture/5ee8f061d4bc13bdf0e9fc6f846982a863486af9/01914.jpg
        reg = r'/picture/(\w+?)/(\d+?).jpg'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, imgurl)
        print ("============ getImg ==============")
        print (imglist)
        s = set(imglist) #用一个集合去除重复
        pic_savepath = os.getcwd()
        #os.path.join(pic_savepath, )
        #x = 0
        #mymkdirs(pic_savepath)
        for img in imglist:
            filename = img[0]+"_"+img[1]+'.jpg'
            print (u"%s --> %s" % (imgurl, filename))
            self.autoDown(imgurl, '%s\%s' % (pic_savepath, filename), self.callbackDownload)
            print ()
            allpic_x+=1
            time.sleep(1)
            
    def get_plain_text(self, jsStr):
        #jsStr='6aKc5YC85LiN6ZSZ5b6h5aeQ55u05pKtIOa/gOaDheiHquaFsOWkp+engA=='
        a = base64.b64decode(jsStr)
        re.escape(a)
        s = unquote(a)
        #print(s.decode("utf8"))
        return s.decode("utf8")

        
    def getNestedPage(self, url):
        html = self.getHtml3(url)
        #<img src="/picture/5ee8f061d4bc13bdf0e9fc6f846982a863486af9/00015.jpg"></img>
        reg = r'''<img src="(.+?)"[^<]*></img>'''
        shtmlre = re.compile(reg)
        shtmllist = re.findall(shtmlre, html)
        print ("==========getNestedPage >>>===========")
        print (shtmllist[0])
        return shtmllist[0]
    
        
    def getSingle(self, url):
        #url = "https://www.ds54.xyz" + url_x
        url_base = "https://www.ds222.xyz" #"https://www.ds57.xyz"
        url = url_base + url #"/movie.php?id=7200657455250621"
        html = self.getHtml3(url)
        '''
        print "url content:"
        print html
        '''
        xitem = {}
        xitem['movlink'] = url
        #<a href='/picture.php?hash=5ee8f061d4bc13bdf0e9fc6f846982a863486af9&name=00015.jpg' target='_blank'><img src='/picture/5ee8f061d4bc13bdf0e9fc6f846982a863486af9/thumb/00015.jpg' width='220'></a>
        reg = r'''<a href='(.+?)' target='_blank'[^<]*>(.+?)</a>'''
        shtmlre = re.compile(reg)
        shtmllist = re.findall(shtmlre, html)
        print (shtmllist)
        s = os.getcwd()
        print ('========================================')
        for x in shtmllist:
            print (x[0])
            #imgurl=self.getNestedPage(url_base + x[0])
            #self.getImg(url_base+imgurl)
        #<a href="/torrent/ce2551480accf08f3937865dd00ec965ad1fcb83.torrent" target="_blank"><b><font size=6px>>>种子下载<<</font></b></a>
        reg = r'''<a href="(.+?)" target="_blank"[^<]*>''' #(.+?)</a>'''
        shtmlre = re.compile(reg)
        shtmllist = re.findall(shtmlre, html)
        print (shtmllist)
        xitem['torrent'] = url_base + shtmllist[1] #/torrent/ce2551480accf08f3937865dd00ec965ad1fcb83.torrent
        #<h2><script type="text/javascript">document.write(d('6aKc5YC85LiN6ZSZ55qE6YeR54mM5Li75pKtIOmcsuWltua8j+mAvOivseaDkSDlj6PkuqTlgYdKSiDmpIXlrZDkuIrmiYvmjIfmj4npmLTokoIg5YGHSkrmj5LpgLwg5b+r6YCf5oq95o+SIOa1geeZvea1hiDpqpHkuZgg6Z2e5bi46K+x5Lq6'));</script>
        reg = r'''<h2><script type="text/javascript">document.write\(d\('(.+?)'\)\);</script>'''
        shtmlre = re.compile(reg)
        shtmllist = re.findall(shtmlre, html)
        try:
            xitem['description'] = self.get_plain_text(shtmllist[0])
            print (xitem['description']    )
        except UnicodeEncodeError as e:
            print (e)
            #xitem['description'] = shtmllist[0]
        print (xitem)
        
        sql = '''INSERT INTO table1 ( pid, description, torrent, movlink )
            VALUES (1, '%s', '%s', '%s')'''%(xitem['description'], xitem['torrent'], xitem['movlink'])
        self.db.mdb_insert(sql)
        
    #获取单个网页url 'list_12_2.html'
    def getPageList(self, roothtml):
        global total_item
        #html = getHtml(roothtml)
        html = self.getHtml3(roothtml)
        #reg = r'<a href="(.+?\.shtml)" target="_blank" title="'
        #<li>[04-11] <a href="/movie.php?id=4589199209585786" target='_blank'><script type="text/javascript">document.write(d('6auY6aKc5YC85pyJ5oOF6Laj5YWo56iL6Zyy6IS46YeR54mM5aWz5Li75pKt5LyX56255aSn56eA77yM5aW25a2Q5LiK6L+Y5pyJ57q56Lqr77yM6YC86IKl5rC05aSa6YGT5YW35oq95o+S5rWq5Y+r77yM5Yeg5oqK6L+b5Y676IO95re55q2756ysNuW8uQ=='));</script></a></li>
        # '<li>[04-12] <a href="/movie.php?id=7095802831463516" target=\'_blank\'><script type="text/javascript">document.write(d(\'6aKc5YC85LiN6ZSZ5b6h5aeQ55u05pKtIOa/gOaDheiHquaFsOWkp+engA==\'));</script></a></li>'
        #reg = r'<li>(?P<nima>.*)<a href="(?P<bb>.+)" target=\'_blank\'><script type="text/javascript">(.+)</script></a></li>'
        reg = r'''<li>\[(.+?)\] <a href="(.+?)" target='_blank'><script type="text/javascript">document\.write\(d\('(.+?)'\)\);</script></a></li>'''
        shtmlre = re.compile(reg)
        shtmllist = re.findall(shtmlre, html)
        #for shtmlpage in shtmllist:
        #    print shtmlpage
        print ('==============================')
        print (shtmllist)
        s = []
        s = set(shtmllist)
        total_item= len(s)
        print (u"总共 %d 项数据"% total_item)
        for x in s:
            try:
                a = self.get_plain_text(x[2])
                print (x[0], ' ', x[1], ' ', a)
            except UnicodeEncodeError as e:
                print (e)
                
            
            self.getSingle(x[1]) #/movie.php?id=2026360030286014
        #getSingle("http://www.xgxz.com/" + s.pop())    
    

    
    def getNumOfPages(self, province, city):
        #url = "https://m.xinkeshequ.com////#/local?id=-3"
        #url = '0/20/214/1/10' #214 广东深圳
        #url = '0/15/143/1/10' #吉安
        #url = '0/15/0/1/30'  #江西
        #url = '0/20/213/1/30'  #广州
        url = "https://m.xinkeshequ.com/cmsv3api/h5/local/news/0/%d/%d/1/30" % (province, city) 
        html = self.getHtml3(url)
        tops = json.loads(html.decode('utf-8'))
        print(html)
        #data = json.loads(tops['data'])
        print ("共 %d 页, 每页 %d 条, 共 %d 条"% (tops['data']['pages'], tops['data']['pageSize'],
        tops['data']['total']))
        pages = tops['data']['pages']
        pages = pages if pages > 0 else 0
        return pages
        
    def decode_x_content(self, str):
        text = str.replace(',oc','\\u') 
        text = text.replace(u'\\u00a0', u' ')
        text = text.replace(u'\\u2200', u' ')
        text = text.replace(u'\\u260e', u' ')
        text = text.replace(u'\\ufe0f', u' ')
        text = text.replace(u'\\u2006', u' ')
        text = text.replace(u'\\u2795', u' ')
        #print(text.encode('utf-8').decode('unicode_escape'))
        #return text.encode('utf-8').decode('unicode_escape')
        return text.encode("utf-8").decode('unicode_escape', 'ignore').encode('gbk', 'ignore').decode('gbk')
           
    def getPageList(self, province, city, page_idx):
        #url = "https://m.xinkeshequ.com////#/local?id=-3"
        #url = '0/20/214/%d/10' % page_idx #深圳 每页10条
        #url =  '0/20/214/%d/30' % page_idx #深圳 每页30条
        #url = '0/15/143/%d/10' % page_idx#吉安
        #url = '0/15/0/%d/30' % page_idx #江西
        #url = '0/20/213/%d/30' % page_idx #广州
        url_base = "https://m.xinkeshequ.com/cmsv3api/h5/local/news/0/%d/%d/%d/30"%(province, city, page_idx)
        url = url_base #+ url #"/movie.php?id=7200657455250621"
        html = self.getHtml3(url)
        tops = json.loads(html.decode('utf-8'))
        print(html)
        #data = json.loads(tops['data'])
        
        #list = data['list']
        list = tops['data']['list']
        i = 0
        for item in list:
            i+=1
            #print ( i, ' -> ', item['title'])            
            #temp_str = item['title']
            #chinese_str = self.decode_x_content(temp_str)
            print ( i, ' -> ', self.decode_x_content(item['title']))

            str_info = "第 %d 页, 第 %d 条，共 %d 页 %d 条"% (tops['data']['pageNum'], (tops['data']['pageNum'] - 1)*tops['data']['pageSize']+i, tops['data']['pages'] ,tops['data']['total']) 
            print (str_info)
            did = item['id']
            details_url = "https://m.xinkeshequ.com/cmsv3api/h5/local/news/detail/" + str(did)
            #details_url = "https://m.xinkeshequ.com/cmsv3api/h5/local/news/detail/4255"
            self.getDetails(details_url)
            time.sleep(0.5)
        #doc_ids = []
        #for item in list[1:]:
        #    print (item)
            #doc_ids.append(item[])
        
        #for x in tops['data']['list']
        #    print (i++, ' -> ', x)
    def getXiaoJieItems(self, province, city):
        pages = self.getNumOfPages(province, city) #获取页面数
        for pg_idx in range(1, pages): #遍历页码////////////////////////////////////////////////////////////////////////////
            self.getPageList(province, city, pg_idx) 
                
    def getcityList(self):
        url = 'https://m.xinkeshequ.com/cmsv3api/h5/local/detail'
        html = self.getHtml3(url)
        citys = json.loads(html.decode('utf-8'))
        #print(citys)
        i = 0
        for province in citys['data']:
            i+=1
            print( province['id'], province['name'])
    
        selflag = 0
        cityList = []
        #pid = '0'
        while selflag == 0:
            pid = input("input province you want get: ")
            for province in citys['data']:
                if province['id'] == int(pid):
                    cityList = province['cityList']
                    print( '你输入了 ', pid , province['name'])
                    selflag = 1
            if( selflag == 0):
                print('输入有误 -------- ')
        

        for city in cityList:
            print( city['id'], city['name'])
        print( '0', '该省(直辖市)所有市(区)')
        
        selflag = 0
        while selflag == 0:
            cid =  input("input city you want get: ")
            for city in cityList:
                if city['id'] == int(cid):
                    print( '你选择了', city['name'])
                    selflag = 1
                elif int(cid) == 0:
                    selflag = 2
                    break;
            if( selflag == 0):
                print('输入有误 -------- ')
        if(selflag == 2):
            for city in cityList:
                cid = city['id']
                self.getXiaoJieItems(int(pid), int(cid)) #获取页面数
        else:
            #self.getXiaoJieItems(int(pid), int(cid)) #获取页面数
            self.getXiaoJieItems(int(pid), int(cid)) #获取页面数
        print("---------------The end--------------------")
        
    def find_itm(self, str1, it):
        #idx= str1.find(it+'：')
        idx = -1
        if str1[0:4] == it:
            idx = 0
        slen = len(str1)
        #print('str1 = ', str1, " find ", it)
        #print('idx = ', idx)
        if idx >= 0 :
            #过滤 ：
            idx+=5 
            while idx<slen and str1[idx]==' ':
                idx+=1
            return True, str1[idx:]
        else: 
            return False, ''
        
    def getDetails(self, url):
        #Request URL: https://m.xinkeshequ.com/cmsv3api/h5/local/news/detail/23304
        xitem = {}
        html = self.getHtml3(url)
        print('details raw :', html)
        tops = json.loads(html.decode('utf-8'))
        chinese_str = self.decode_x_content(tops['data']['content'])
        title_str = self.decode_x_content(tops['data']['title'])
        print('标题：', title_str,'\n内容：', chinese_str)
        chinese_str +='<br>'
        xitem['news_time']='1970-01-01'
        xitem['title']=''
        xitem['region']=''
        xitem['category']=''
        xitem['detail_addr']=''
        xitem['info_from']=''
        xitem['go_out']=''
        xitem['xj_count']=''
        xitem['xj_age']=''
        xitem['xj_appearance']=''
        xitem['srv_attitude']=''
        xitem['srv_menu']=''
        xitem['env_equip']=''
        xitem['buss_hours']=''
        xitem['xj_price']=''
        xitem['safety_asse']=''
        xitem['cph_evaluation']='',
        xitem['contact']=''
        xitem['detail_intro']=''
        xitem['site_id'] = tops['data']['id']
        xitem['news_time'] = tops['data']['newsTime']
        xitem['title'] = title_str
        #reg = r'''(.+?)<br>'''
        reg = r'''(.*?)<br>+'''
        shtmlre = re.compile(reg)
        shtmllist = re.findall(shtmlre, chinese_str)
        #for shtmlpage in shtmllist:
        #    print shtmlpage
        print ('==============================')
        print (shtmllist)
        its={'region': '妹子地区', 
            'category': '信息分类', 
            'detail_addr': '详细地址', 
            'info_from': '信息来源',
            'go_out': '外卖与否',
            'xj_count': '妹子数量',
            'xj_age': '妹子年龄',
            'xj_appearance': '妹子容貌',
            'srv_attitude': '服务态度',
            'srv_menu': '服务菜单',
            'env_equip': '环境设备',
            'buss_hours': '营业时间',
            'xj_price': '妹子价格',
            'safety_asse': '安全评估',
            'cph_evaluation': '综合评估',
            'contact': '联系方式',
            'detail_intro': '详细介绍'}
        #s = []
        #s = set(shtmllist)
        s = shtmllist
        #reg = r'''<br>([^<]*)$'''
        #shtmlre = re.compile(reg)
        #shtmllist = re.findall(shtmlre, chinese_str)
        #print('<br>详细介绍： (.*?)$ matched ',shtmllist)
        #if len(shtmllist) > 0 :
        #   xitem['detail_intro'] = shtmllist[0]
        #   print('xitem[\'detail_intro\']: ', xitem['detail_intro'])
        total_item= len(s)
        print (u"共匹配 %d 项数据"% total_item)
        for x in s:
            a = x
            print(a)
            for key in its:
                try:
                    
                    ret,str_i = self.find_itm(x, its[key])
                    if ret :
                        xitem[key] = str_i
                        print('xitem[\'%s\'] = %s'%( key, xitem[key]))
                        break
                except UnicodeEncodeError as e:
                    print (e)
        sql = ''' select * from xiaojie_hebei where site_id = %s'''% xitem['site_id']
        rcd=self.db.db_select(sql)
        if len(rcd) > 0:
            print( "数据库中已存在该记录")
            return 
        sql = '''INSERT INTO xiaojie_hebei ( site_id, news_time, title, region, category, 
           detail_addr, info_from, go_out, xj_count, xj_age,
           xj_appearance, srv_attitude, srv_menu, env_equip, buss_hours, 
           xj_price, safety_asse, cph_evaluation, contact, detail_intro)
            VALUES ( %d, '%s', '%s', '%s', '%s',
             '%s', '%s', '%s', '%s', '%s',
             '%s', '%s', '%s', '%s', '%s',
             '%s', '%s', '%s', '%s', '%s'
            )'''%(xitem['site_id'], xitem['news_time'], xitem['title'], xitem['region'], xitem['category'],
            xitem['detail_addr'], xitem['info_from'], xitem['go_out'], xitem['xj_count'], xitem['xj_age'],
            xitem['xj_appearance'], xitem['srv_attitude'], xitem['srv_menu'], xitem['env_equip'], xitem['buss_hours'],
            xitem['xj_price'], xitem['safety_asse'], xitem['cph_evaluation'], xitem['contact'], xitem['detail_intro'],
            )
        print("sql :", sql)
        self.db.exec_sql(sql)
        
    def get_urlcode_text(self):
        #jsStr='6aKc5YC85LiN6ZSZ5b6h5aeQ55u05pKtIOa/gOaDheiHquaFsOWkp+engA=='
        #a = u'壹屌寻花'
        #https://m.huangsewangzhi.net/
        #https://m.yunyuanad.com/cmsv3api/h5/local/news/0/20/214/1/10
        a = 'https://m.xinkeshequ.com/cmsv3api/h5/local/news/0/20/214/1/10'
        re.escape(a)
        #对url编码解码
        s = urllib.parse.unquote(a)
        print('decode url: %s'%s)
        s = urllib.parse.quote(s)
        print('quote url: %s'%s)
        return s #.decode("utf8")
#getPageList("https://www.ds333.xyz/index.php?page=1")    
#html = getHtml("http://www.xgxz.com/siwameitui/201606/0603192C2016.shtml")
#print getImg(html)
    def ungzip(self, data):
        try:
            data = gzip.decompress(data)
        except Exception as e:
            print('未经压缩, 无需解压')
            pass  # print('未经压缩, 无需解压')
        return data
        
    def spr_post_file(self, url, data, timeout = 2):
        global cur_item_no
        headers = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       #'Host': 'certsign.realtek.com',
       #'Origin': 'https://certsign.realtek.com',
       #'Content-Type': 'application/x-www-form-urlencoded',
       #'Referer': 'https://certsign.realtek.com/SMSOTP.jsp',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'same-origin',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        #'Cookie': '_pk_ses.2.a6f7=1; JSESSIONID=50CB9A0B10EAC7F72F84B66923CC2E21; _pk_id.2.a6f7=a596b944cc4c029a.1620272182.15.1623237968.1623236515.'
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        deal_data = bytes(parse.urlencode(data), encoding='utf8')
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url, data=deal_data, headers = headers, method='POST')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('='*80)
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url: ', url)
        print ('http status:',page.getcode())
        print ('='*80)
        return html
        
    def putFileToCertSign(self, url, path, file_name, timeout=2):
        #file_name='test'
        #url=
        ifile =  path + "\\" + file_name
            
        register_openers()   
        datagen, headers = multipart_encode({file_name: open(ifile, "rb")})
       
       
        # 创建请求对象
        req = request.Request(url, datagen, headers)
        # 实际执行请求并取得返回
        respone = request.urlopen(req).read()
        self.printDelimiter()
        print("\nrespone:", respone )
        '''
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
               
                #req = request.Request(url, data=body, headers = header, method='POST')
                req = request.Request(url, data=body, method='POST')                      
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                req.add_header('Content-type', form.get_content_type())
                req.add_header('Content-length', len(body))
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('='*80)
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url: ', url)
        print ('http status:',page.getcode())
        print ('='*80)
        return html
        '''
    def dl_mail(self):
        '''
        print("Uploading file Win720210604.zip")
        html = self.putFileToCertSign(url="https://certsign.realtek.com/advanceConvert", path="D:\\test", file_name="Win720210604.zip", timeout=60)
        data ={
        'login_username': 'jingdong_qiu',
        'login_password': 'Qq369369'
        }
        html = self.post(url="https://certsign.realtek.com/Login", data=data)
        print(html.decode("utf-8"))
        self.printDelimiter()
        data =[
           ("flag", "otp_c"),
           ("flag", "null")
        ]
        #https://certsign.realtek.com/ADVerify?flag=otp_c&flag=null
        html = self.spr_post("https://certsign.realtek.com/ADVerify",data, 6)#测过浏览器完成这个request大概要5.16s
        print(html.decode("utf-8"))
        '''
        self.printDelimiter()
        
        data1 = {
        'destination': 'https://mail.realtek.com/owa',
        'flags': 4,
        'forcedownlevel': 0,
        'username': 'xx@realtek.com',
        'password': 'hello',
        'isUtf8': 1
        }
        html = self.spr_post(url="https://mail.realtek.com/owa/auth.owa", data=data1);
        html = self.ungzip(html)
        print(html.decode("utf-8"))
        self.printDelimiter()
        #html = self.getHtml3("https://mail.realtek.com/owa/?ae=Folder&t=IPF.Note&id=LgAAAACZpfPyFZDkTIBBuJbamineAQB3JuyQcogkSZTumckl5UoQAAAApGXlAAAB&slUsng=0")
        #print(html.decode("utf-8"))
       
        respHtml = html.decode("utf-8");
        #<input type="checkbox" name="chkmsg" value="RgAAAACZpfPyFZDkTIBBuJbamineBwB3JuyQcogkSZTumckl5UoQAAAApGXlAABmstg4X0+IQL1SPLvPP4CPAAFbGrirAAAJ" title="&#36873;&#25321;&#39033;&#30446;" onclick="onClkChkBx(this);">&nbsp;</td><td nowrap class="frst">motp@realtek.com&nbsp;</td>
        foundTokenVal = re.search("<input type=\"checkbox\" name=\"chkmsg\" value=\"(?P<id>[^>]+)\" title=\"[^>]+\" onclick=\"[^>]+\">&nbsp;</td><td nowrap( class=\"frst\")?>motp@realtek.com&nbsp;<[^>]+>", respHtml) #(.*)motp@realtek.com
        bFindMOTP = False
        tokenVal=""
        if(foundTokenVal):
            tokenVal = foundTokenVal.group("id")
            print ("=> ",tokenVal)
            bFindMOTP = True
        else:
            print("not found")
        
        if(bFindMOTP):
            url_id = parse.quote(tokenVal)
            url = "https://mail.realtek.com/owa/?ae=Item&t=IPM.Note&id=%s"% url_id
            #rspHtml = self.getHtml3(url)
            html = self.spr_get(url)
            #rspHtml = self.getHtml3("https://mail.realtek.com/owa/?ae=Item&t=IPM.Note&id=RgAAAACZpfPyFZDkTIBBuJbamineBwB3JuyQcogkSZTumckl5UoQAAAApGXlAABmstg4X0%2bIQL1SPLvPP4CPAAFbGrjJAAAJ") 
            print(html.decode("utf-8"))
            rspHtml = html.decode("utf-8")
            #<font color="#0000FF">995253</font>
            foundOtpVal = re.search("<font color=\"#0000FF\">(?P<otp>\d{6})</font>",rspHtml)
            if(foundOtpVal):
                otpcode = foundOtpVal.group("otp")
                print("otp 码：", otpcode)
                self.printDelimiter()
                return otpcode
                '''
                data = [
                    ("flag", "otp_v"),
                    ("flag", "jingdong_qiu"),
                    ("otp1", otpcode)
                ]
                html = self.spr_post(url="https://certsign.realtek.com/SMSOTP.jsp", data=data)
                print(html.decode("utf-8"))
                self.printDelimiter()
                print("Uploading file Win720210604.zip")
                html = self.putFileToCertSign(url="https://certsign.realtek.com/advanceConvert", path="D:\\test", file_name="Win720210604.zip", timeout=60)
                #print(html.decode("utf-8"))
                '''
        

        self.printDelimiter()
        return None
        
'''
if __name__ == "__main__":
    imp.reload(sys)
    #sys.setdefaultencoding('utf8')
    iSpider = Spider()
    #s = duanziSpider.get_urlcode_text()
    #duanziSpider.getcityList()
    iSpider.dl_mail()
'''
