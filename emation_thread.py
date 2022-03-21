
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import json
import httpx
import lxml.html
from lxml import etree
import os
import re
import math
from configparser import ConfigParser
from shopping_cart_dlg import CartItem
from shopping_cart_dlg import Cart
from spider import Spider 
from enum import Enum, auto
from tmessage import MessageNode
from tmessage import Looper

class   MSG(Enum):
    LOGIN = 0
    SEARCH = auto()
    SEARCH_PAGE = auto()
    CONDITION_SEARCH = auto()
    ADDCART = auto()
    DISPLAYCART = auto()
    GREEN   = auto()
    PINK    = auto()

class ProdItem():
    idx =0
    productname = ""
    productCode = ""
    numberprices = ""
    stockNumber = ""
    theRatio = 1
    productPriceList=[]
    purchasedNumber = 0
    purchaseUnitPrice = 0
    purchasedAmount = 0
    productId = ""
    def __init__(self):
        pass

class EmationThread(QThread):  # 继承QThread
    updateSignal = QtCore.pyqtSignal(str)  # 注册一个信号
    updateViewSignal = QtCore.pyqtSignal(list)
    updateCart = QtCore.pyqtSignal(Cart)
    updateResultSignal = QtCore.pyqtSignal(str)
    updateRecordCnt = QtCore.pyqtSignal(int, int) 
    goods_in_stock = False
    pageCount = 0
    def __init__(self, looper, parent= None): # 从前端界面中传递参数到这个任务后台
        self.looper = looper 
        super(EmationThread, self).__init__(parent)
        self.spider = Spider()

    def run(self):  # 重写run  比较耗时的后台任务可以在这里运行    
        spider = self.spider
        #msg = self.queue.get(block = False)
        numbers = {
            MSG.LOGIN : self.loginLCSC,
            MSG.SEARCH : self.crawlingLCSC,
            MSG.SEARCH_PAGE: self.searchEntry,
            MSG.CONDITION_SEARCH : self.conditionSearch1,
            MSG.ADDCART : self.addCartAjax,
            MSG.DISPLAYCART: self.displayCart
        }
        while True:
            msg = self.looper.obtainMessage()
            method = numbers.get(msg.msg_id, "")
            if method:
                method(msg.wparam, msg.lparam)

    def displayCart(self, wparam, lparam):
        spider = self.spider
        print("*"*80)

        url = "https://cart.szlcsc.com/cart/display?isInit=true&isOrderBack=false"
        html = spider.spr_get_html(url, http2=True)
        self.writeToFile("foo_cart.json", html)
        try:
            jo1=json.loads(html)
        except json.decoder.JSONDecodeError as e:
            print("catch error: ", e)
            return
        shoppingCartVO = jo1["result"]["shoppingCartVO"]
        cartTotalSize = shoppingCartVO["cartTotalSize"]
        rmbCnShoppingCart = shoppingCartVO["rmbCnShoppingCart"]
        productSize = rmbCnShoppingCart["productSize"]
        productList = rmbCnShoppingCart["currentlyProductList"]
        cart = Cart()
        cart.cartTypeCount = rmbCnShoppingCart["cartTypeCount"]
        cart.cartTypeGdCount = rmbCnShoppingCart["cartTypeGdCount"]
        cart.cartOnlineMoney = rmbCnShoppingCart["cartOnlineMoney"]

        cartProductList =[]
        for i, product in enumerate(productList):
            cartItem = CartItem()
            cartItem.productId = product["productId"]
            cartItem.productCode = product["productCode"]
            cartItem.productName=product["productName"]
            cartItem.productModel=product["productModel"]
            cartItem.shopCarMapKey=product["shopCarMapKey"]
            cartItem.shopCarId=product["shopCarId"]
            cartItem.productNumber=product["productNumber"] #购买数量
            cartItem.convesionRatio = product["convesionRatio"]
            cartItem.productConsultPrice = product["productConsultPrice"]
            cartItem.productType=product["productType"]
            cartItem.productGradePlateName=product["productGradePlateName"] #品牌
            cartItem.encapsulationModel=product["encapsulationModel"] #封装
            cartItem.remark = product["remark"] #材质
            cartItem.bigImageUrl = product["bigImageUrl"]
            cartItem.hasAnnexPDF = product["hasAnnexPDF"]
            cartItem.gdDeliveryNum=product["gdDeliveryNum"]
            cartItem.gdDivideSplitDeliveryNum=product["gdDivideSplitDeliveryNum"]
            cartItem.isAllowUseCoupon=product["isAllowUseCoupon"] #是否允许使用优惠券
            cartItem.jsValidStockNumber = product["jsValidStockNumber"] #江苏库存
            cartItem.szValidStockNumber = product["szValidStockNumber"] #广东库存
            cartItem.stockNumber = product["stockNumber"] #总库存
            cartItem.lineMoney = product["lineMoney"] #价格
            cartItem.overseaProductTotalMoney = product["overseaProductTotalMoney"] #价格
            cartItem.productCycle =product["productCycle"]
            cartProductList.append(cartItem)
        savedir = os.getcwd() + "/cache"
        if(not os.path.exists(savedir)):
            os.makedirs(savedir)    
        for i, product in enumerate(cartProductList):
            product.localImg = spider.extractFileName(product.bigImageUrl, savedir)
            if(product.localImg == None):
                continue
            print("%s -- > %s"%(product.bigImageUrl, product.localImg))
            spider.spr_get_file(product.bigImageUrl, product.localImg)
        cart.cartProductList = cartProductList
        self.updateCart.emit(cart)
        print("*"*80)
        #print(html)

    def addCartAjax(sel, wparam, lparam):
        spider = self.spider
        print("*"*80)
        url = "https://cart.szlcsc.com/jsonp/add?cartKeyStr=0~257230~RMB~CN~3~3~0&entryType=product_choose_buy"
        #header = {"Referer" : "https://so.szlcsc.com/"}
        #html = spider.spr_get_html(url, header=header, http2=True)
        html = spider.spr_get_html(url, http2=True)
        self.writeToFile("foo_addcart.html", html)
        print("*"*80)
        print(html)

    def setSearchCriteria(self, goods_in_stock):
        self.goods_in_stock = goods_in_stock
    
    def execJS(self, js_plain):
        #data=open('sjtest.js','r',encoding= 'utf8').read()
        data = js_plain
        print(type(data))
        data=js2py.eval_js(data)

    def singlePageSearch(self, page):
        spider = self.spider 
        url = "https://so.szlcsc.com/search"
        data ={
            #os : "1", #  0有现货， 1无
            "sb"    : "0",
            "pn"    : str(page), #页号
            "k" : "10nf+0402",
            "tc"    : "0",
            "pds" : "0",
            "pa"    : "0",
            "pt"    : "0",
            "gp"    : "0",
            "sk"    : "10nf+0402",
            "stock" : "sz",
        }
        if (self.goods_in_stock):
            data.update({"os":  "0"})
        html = spider.spr_post_gethtml(url, data=data, http2=True)
        self.writeToFile("searchResult.html", html)
        for i in range(1, 15):
            try:
                jo1=json.loads(html)
                break
            except json.decoder.JSONDecodeError as e:
                print("catch error: ", e)
                doc = etree.HTML(html)
                scr_node = doc.xpath('//script')
                print(src_node)
                return []
        return jo1["result"]
        #print(jo1["result"]['productRecordList'][0])

    def SearchPage(self, page):
        self.printLog("Processing  "+str(page) +" page !")
        jo1 = self.singlePageSearch(page)
        if(not jo1):
            return;
            #print(jo1["result"]['productRecordList'][0])
        self.parseItems(jo1['productRecordList'])
        self.updateViewSignal.emit(self.itemList)
        self.printLog("Complete!")

    def conditionSearch(self):
        spider = self.spider 
        if(self.pageCount == 0):
            self.printLog("没有先搜一下就设定条件!")
            return
        totalCount = 0
        jo_resulut =self.singlePageSearch(1)
        if(not jo_resulut):
            return;
        totalCount = jo_resulut["totalCount"]
        
        pageCount = math.ceil(totalCount/20.0)
        self.pageCount = pageCount
        self.updateResultSignal.emit("符合条件商品，共" + str(totalCount) + "件, " 
            + str(pageCount) + " 页")
        self.itemList =[]
        self.parseItems(jo_resulut['productRecordList'])
        #print(self.get_inner_html(nodes))
        self.updateViewSignal.emit(self.itemList)
        self.printLog("Complete!")

    def searchAllPage(self):
        for page in range(2, self.pageCount+1):
            self.printLog("Processing  "+str(page) +" page !")
            jo1 = self.singlePageSearch(page)
            if(not jo1):
                return;
            #print(jo1["result"]['productRecordList'][0])
            self.parseItems(jo1['productRecordList'])
        self.updateViewSignal.emit(self.itemList)
        self.printLog("Complete!")

    def conditionSearch1(self, wparam, lparam):
        spider = self.spider 
        if(self.pageCount == 0):
            self.printLog("没有先搜一下就设定条件!")
            return
        totalCount = 0
        jo_resulut =self.singlePageSearch(1)
        if(not jo_resulut):
            return;
        totalCount = jo_resulut["totalCount"]
        
        pageCount = math.ceil(totalCount/20.0)
        self.pageCount = pageCount
        self.updateResultSignal.emit("符合条件商品，共" + str(totalCount) + "件, " 
            + str(pageCount) + " 页")
        self.updateRecordCnt.emit(totalCount, pageCount)
        self.itemList =[]
        self.parseItems(jo_resulut['productRecordList'])

        self.updateViewSignal.emit(self.itemList)
        self.printLog("Complete!")

    def searchEntry(self, wparam, lparam):
        page = wparam
        if(page > 0):
            self.SearchPage(page)
            return
        self.searchAllPage()

    def crawlingLCSC(self, wparam, lparam):
        spider = self.spider
        
        url ="https://so.szlcsc.com/global.html?k=10nf%25200402&hot-key=TJA1043T%2F1J"      
        html = spider.spr_get_html(url, http2=True)
        #print(html.decode("utf-8"))
        self.writeToFile("foo.html", html)
        doc = etree.HTML(html)
        nodes = doc.xpath('//div[@id=\'by-channel-total\']//b')
        print("nodes = ", nodes)
        if(not nodes):
            print("未获取到数据")
            self.printLog("未获取到数据!") 
            return
        for href in nodes:
            print(href.text)
        totalCount = int(nodes[0].text)
        pageCount = math.ceil( totalCount/20 )  
        print("page count: ", pageCount)
        self.pageCount = pageCount
        self.updateResultSignal.emit("符合条件商品，共" + str(totalCount) + "件, "
            + str(pageCount) + " 页")
        self.conditionSearch()
    
    def parseItems(self, productRecordList):
        
        for i, product in enumerate(productRecordList):

            productname = product["productName"] +"\n" \
                        + "封装： " + product["encapsulationModel"] + "\n" \
                        + "品牌： " + product["lightBrandName"] + "\n" \
                        + "型号： " + product["productModel"] + "\n" \
                        + "描述： " + product["remarkPrefix"] + "\n" 
            productCode = product["productCode"] + "\n" \
                        + product["productId"] #加入购物车时有用
            productId = product["productId"] 
            #numberprices = product["numberprices"]+ "\n"
            #temp = numberprices.split(',', -1)
            #coeff =int(temp[1])
            coeff = product["theRatio"]
            numberprices =""
            '''
            j=5
            while j <= len(temp)-2:
                numberprices +=str(int(temp[j])*coeff) + "+: " + temp[j+2]+ "\n"
                j+=3 
            '''
            #for k, priitem in enumerate(product["priceDiscount"]["priceList"]):
            #    numberprices +=str(priitem["spNumber"]* coeff) + "+: " + str(priitem["price"]) + "\n"
            
            for k, priitem in enumerate(product["productPriceList"]):
                numberprices += str(priitem["startPurchasedNumber"]* coeff) + "+: " + str(priitem["productPrice"]) + "\n"
            #numberprices= str(int(temp[5])* coeff) + ": " + temp[5+2]
            stockNumber = "广东仓： " + str(product["gdWarehouseStockNumber"]) +"\n" \
                        "江苏仓： "+str(product["jsWarehouseStockNumber"]) 
            xitem = ProdItem()
            xitem.productname = productname
            xitem.productCode = productCode
            xitem.productId = productId
            xitem.numberprices = numberprices
            xitem.stockNumber = stockNumber
            xitem.productPriceList = product["productPriceList"]
            xitem.theRatio = product["theRatio"]
            self.itemList.append(xitem)

    def getHello(self):
        spider = self.spider


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

    def loginLCSC(self, wparam=None, lparam=None):
        self.printLog("登录中...")
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
        response = spider.spr_post(url="https://passport.szlcsc.com/login", data=data1, http2=True);
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
        try:
            jo1=json.loads(html)
        except json.decoder.JSONDecodeError as e:
            print("catch error: ", e)
            
        self.printLog(jo1["result"]["customerCode"] + " 登录完成")