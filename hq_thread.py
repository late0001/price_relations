
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import json
import httpx
import lxml.html
from lxml import etree
import common
from enum import Enum, auto
from spider import Spider 
from configparser import ConfigParser
from product import ProdItem

class   HQMSG(Enum):
    LOGIN = 0
    SEARCH = auto()
    SEARCH_PAGE = auto()
    CONDITION_SEARCH = auto()
    ADDCART = auto()
    DISPLAYCART = auto()



class HqThread(QThread):  # 继承QThread
    updateSignal = QtCore.pyqtSignal(str)  # 注册一个信号
    updateViewSignal = QtCore.pyqtSignal(list)
    #updateCart = QtCore.pyqtSignal(Cart)
    updateResultSignal = QtCore.pyqtSignal(str)
    updateRecordCnt = QtCore.pyqtSignal(int, int) 
    goods_in_stock = False
    pageCount = 0
    def __init__(self, looper, parent= None): # 从前端界面中传递参数到这个任务后台
        self.looper = looper 
        super(HqThread, self).__init__(parent)
        self.spider = Spider()

    def run(self):  # 重写run  比较耗时的后台任务可以在这里运行    
        spider = self.spider
        #msg = self.queue.get(block = False)
        numbers = {
            HQMSG.LOGIN : self.loginHqChip,
            HQMSG.SEARCH : self.search,
            #HQMSG.SEARCH_PAGE: self.searchEntry,
            #HQMSG.CONDITION_SEARCH : self.conditionSearch1,
            #HQMSG.ADDCART : self.addCartAjax,
            #HQMSG.DISPLAYCART: self.displayCart
        }
        while True:
            msg = self.looper.obtainMessage()
            method = numbers.get(msg.msg_id, "")
            if method:
                method(msg.wparam, msg.lparam)

    def printLog(self,text):
        self.updateSignal.emit(text)  # 任务完成后，发送信号

    def parseItems(self, productRecordList):
        
        for i, product in enumerate(productRecordList):

            productname = \
                          "封装： " + product["encap"] + "\n" \
                        + "品牌： " + product["SelfBrand"]["brand_name"] +"("+ product["SelfBrand"]["brand_cn"]+")" + "\n" \
                        + "型号： " + product["ModelName"] + "\n" \
                        + "描述： " + product["Desc"] + "\n" 
            productCode = "GoodsId: " + str(product["GoodsId"]) + "\n" \
                        + "GoodsSn: " + product["GoodsSn"] #加入购物车时有用
            productId = product["GoodsSn"] 

            #coeff = product["theRatio"]
            numberprices =""
            
            for k, priitem in enumerate(product["Tiered"]):
                numberprices += str(priitem[0]) + "+: " + str(priitem[1]) + "\n"
            #numberprices= str(int(temp[5])* coeff) + ": " + temp[5+2]
            stockNumber=""
            for k, priitem in enumerate(product["Stocks"]):
                stockNumber += str(priitem[0]) + "+: " + str(priitem[1]) + "\n"
            xitem = ProdItem()
            xitem.productname = productname
            xitem.productCode = productCode
            xitem.productId = productId
            xitem.numberprices = numberprices
            xitem.stockNumber = stockNumber
            xitem.productPriceList = product["Tiered"]
            #xitem.theRatio = product["theRatio"]
            self.itemList.append(xitem)

    def search(self, wparam, lparam):
        spider = self.spider
        #url = "https://ss.hqchip.com/?keyword=10NF+0402&es_keyword=10nf+0402&supp=42,22,29,27,34,44,38,41,24,36,19,43,45,48&limit=100"
        url = "https://s13.hqchip.com/?k=13&keyword=100NF+0402&es_keyword=100nf+0402&limit=100&match_model_name=0"
        html = spider.spr_get_html(url)
        try:
            jo1=json.loads(html)
        except json.decoder.JSONDecodeError as e:
            print("catch error: ", e)
        self.itemList =[]
        #self.parseItems(jo1["PA"][0]["PD"])
        self.parseItems(jo1["PD"])
        self.updateViewSignal.emit(self.itemList)
        self.printLog("Complete!")

    def loginHqChip(self, wparam, lparam):
        spider = self.spider

        cfg = ConfigParser()
        cfg.read('config.ini')
        self.hq_username = cfg.get('hqchip', 'username')
        self.hq_password = cfg.get('hqchip', 'password')

        url = "https://www.hqchip.com/ajax/getcustomerinfo?v=pc"
        html = spider.spr_get_html(url, http2=True)
        common.writeToFile("getcustomerinfo.html", html)

        data1 = {
            "referer": "https://www.hqchip.com",
            "siteid" :	"12",
            "account": self.hq_username,
            "password":	self.hq_password,
            "csessionid": "",
            "sig":	"",
            "token":	"",
            "aliscene":	""
        }
        url="https://passport.elecfans.com/login/dologin.html"
        response = spider.spr_post(url=url, json=data1, http2=True)
        print("encoding : ", response.encoding)
        #print("text : ", response.text)
        #print("location", response.headers['location'])
        respHtml = response.text
        #print(respHtml)
        #print("location is : ", response.info())
        print("*"*80)
       # print("getheaders() =>", response.getheaders())
        common.writeToFile("login_hq.html", respHtml)
        #jo1={}
        try:
            jo1=json.loads(respHtml)
        except json.decoder.JSONDecodeError as e:
            print("catch error: ", e)

        print(spider.cookie)
        if(jo1["msg"]):
            self.printLog(jo1["msg"])

