from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from cmppui import Ui_Nima
from spider import Spider 
import sys
import re
import httpx
import lxml.html
from lxml import etree
import math
from configparser import ConfigParser

class mywindow(QtWidgets.QMainWindow, Ui_Nima):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_lcsc)
    def openDialog(self):
        filename, filetype =QFileDialog.getOpenFileName(self, "选取文件", "C:/", "All Files(*);;Text Files(*.csv)")
        print(filename, filetype)
        self.lineEdit.setText(filename)
        
    def get_lcsc(self):
        self.ThreadEmation = EmationThread()
        self.ThreadEmation.updateSignal.connect(self.UpdateStatusText) 
        self.ThreadEmation.start()
        
    def UpdateStatusText(self, res):
        self.statusLabel.setText(res)


class EmationThread(QtCore.QThread):  # 继承QThread
    updateSignal = QtCore.pyqtSignal(str)  # 注册一个信号
    def __init__(self, parent= None): # 从前端界面中传递参数到这个任务后台
        super(EmationThread, self).__init__(parent)
        self.spider = Spider()

    def run(self):  # 重写run  比较耗时的后台任务可以在这里运行    
        spider = self.spider
        self.crawlingLCSC()
        url ="https://so.szlcsc.com/global.html?k=10nf%25200402&hot-key=TJA1043T%2F1J"      
        html = spider.spr_get_html(url, http2=True)
        #print(html.decode("utf-8"))
        self.writeToFile("foo.html", html)
        doc = etree.HTML(html)
        nodes = doc.xpath('//div[@id=\'by-channel-total\']//b')
        for href in nodes:
            print(href.text)
        pageCount = math.ceil( int(nodes[0].text)/20 )  
        print("page count: ", pageCount)
        #print(self.get_inner_html(nodes))
        url = "https://so.szlcsc.com/search"
        data ={
            "sb"    : "0",
            "pn"    : "2", #页号
            "k" : "10nf+0402",
            "tc"    : "0",
            "pds" : "0",
            "pa"    : "0",
            "pt"    : "0",
            "gp"    : "0",
            "sk"    : "10nf+0402",
            "stock" : "sz",
        }
        html = spider.spr_post_gethtml(url, data=data, http2=True)
        self.writeToFile("searchResult.html", html)

        self.printLog("Complete!")
        

    def printLog(self,text):
        self.updateSignal.emit(text)  # 任务完成后，发送信号

    def writeToFile(self, filename, content):
        with open(filename, "w", encoding="utf-8") as fo:
            fo.write(content)

    def get_inner_html(self, node):
        html = node
        p_begin = html.find('>') +1
        p_end = html.rfind('<')
        return html[p_begin: p_end]

    def crawlingLCSC(self):
        spider = self.spider
        html = spider.spr_get_html(
            url="https://passport.szlcsc.com/login?service=https://member.szlcsc.com/member/login.html?s=&c=&f=shop", 
            http2 = True)
        respHtml = html
        #print(respHtml)
        self.writeToFile("foo2.html", respHtml)
        print(spider.cookie)
        foundTokenVal = re.search("<input type=\"hidden\" name=\"lt\" value=\"(?P<lt>LT-.*-cas.test.com)\" />", respHtml)
        flt = ""
        if(foundTokenVal):
            flt = foundTokenVal.group("lt")
            print ("=> ",flt)
        else:
            print("not found lt")
            self.printLog("not found lt")
            return
        
        foundTokenVal = re.search("<input type=\"hidden\" name=\"execution\" value=\"(?P<execution>[\w]+)\" />", respHtml)
        execution = ""
        if(foundTokenVal):
            execution = foundTokenVal.group("execution")
            print ("=> ",execution)
        else:
            print("not found execution")
            self.printLog("not found execution")
            return
        cfg = ConfigParser()
        cfg.read('config.ini')
        self.lc_username = cfg.get('szlcsc', 'username')
        self.lc_password = cfg.get('szlcsc', 'password')
        data1 = {
            #"lt" : "LT-1548862-ggo4fjByDKbZ6VAeB0Yv4oO5PuREXS-cas.test.com",
            "lt" : flt,
            "execution" : execution,
            "_eventId" : "submit",
            "loginUrl" :  "https://passport.szlcsc.com/login?service=https%3A%2F%2Fmember.szlcsc.com%2Fmember%2Flogin.html%3Fs%3D%26c%3D%26f%3Dshop",
            "afsId" : "",
            "sig" : "",
            "token"  : "",
            "scene"  : "login",
            "loginFromType" : "shop",
            "showCheckCodeVal" : "false",
            "pwdSource" :  "",
            "username" :  self.lc_username,
            "password" :  self.lc_password,
            "rememberPwd" : "yes"
        }
        response = spider.spr_post_getrsp(url="https://passport.szlcsc.com/login", data=data1, http2=True);
        print("encoding : ", response.encoding)
        print("text : ", response.text)
        print("location", response.headers['location'])
        respHtml = response.text
        #print(respHtml)
        #print("location is : ", response.info())
        print("*"*80)
       # print("getheaders() =>", response.getheaders())
        self.writeToFile("foo1.html", respHtml)
        print(spider.cookie)
        #https://member.szlcsc.com/member/login.html?s=&ticket=ST-321346-Xryqf1J6kcfl9f9ahVpd-cas.test.com
        url = response.headers['location']
        html = spider.spr_get_html(
            url=url, 
            http2 = True);
        self.writeToFile("foo2.html", html)
        print(spider.cookie)
        
        
        url = "https://member.szlcsc.com/member/login.html?s=&c=&f=shop"
        html = spider.spr_get_html(
            url=url, 
            http2 = True);
        self.writeToFile("foo3.html", html)
        print(spider.cookie)
        #html = spider.spr_get(url="https://www.szlcsc.com/async/page/home/order/customer/message")
        url="https://www.szlcsc.com/async/page/home/order/customer/message"
       
        html = spider.spr_get_html(
            url=url, 
            http2 = True);
        print(html)
        self.writeToFile("foo4.html", html)
        print(spider.cookie)


if __name__== "__main__":
    
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    sys.exit(app.exec_())
