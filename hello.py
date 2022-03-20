from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from cmppui import Ui_Nima
from shopping_cart_dlg import CartDlg
from shopping_cart_dlg import CartItem
from page_navigator import PageNavigator
from spider import Spider 
from queue import Queue
import sys
import os
import re
import httpx
import lxml.html
from lxml import etree
import math
from configparser import ConfigParser
import json
from enum import Enum, auto


class   MSG(Enum):
    LOGIN = 0
    SEARCH = auto()
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
    


class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, text, sortKey):
        #call custom constructor with UserType item type
        QTableWidgetItem.__init__(self, text, QTableWidgetItem.UserType)
        self.sortKey = sortKey

    #Qt uses a simple < check for sorting items, override this to use the sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey    

class mywindow(QMainWindow, Ui_Nima):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pageNavigator = PageNavigator()
        self.horizontalLayout.addWidget(self.pageNavigator)
        self.pageNavigator.setMaxPage(15)
        self.pushButton.clicked.connect(self.get_lcsc)
        self.btn_Addcart.clicked.connect(self.addCart)
        self.ckb_spot.stateChanged.connect(self.changeCkbSpot)
        self.btn_Calc.clicked.connect(self.Calc)
        self.cartBtn.clicked.connect(self.openCart)
        self.tableWidget.setSortingEnabled(True);
        self.tableWidget.sortByColumn(4, Qt.AscendingOrder)
        self.queue = Queue()
        self.ThreadEmation = EmationThread(self.queue)
        self.ThreadEmation.updateSignal.connect(self.UpdateStatusText) 
        self.ThreadEmation.updateViewSignal.connect(self.UpdateTableWidget)
        self.ThreadEmation.updateResultSignal.connect(self.UpdateResultText)
        self.productRecordList = []

    def loginToLCSC(self):
        self.queue.put(MSG.LOGIN)
        self.ThreadEmation.start()
   
    def openDialog(self):
        filename, filetype =QFileDialog.getOpenFileName(self, "选取文件", "C:/", "All Files(*);;Text Files(*.csv)")
        print(filename, filetype)
        self.lineEdit.setText(filename)
    
    def changeCkbSpot(self):
         if self.ckb_spot.checkState() == Qt.Checked:
            self.ThreadEmation.setSearchCriteria(True)
            self.queue.put(MSG.CONDITION_SEARCH)

    def get_lcsc(self):  
        self.queue.put(MSG.SEARCH)
    
    def addCart(self):
        self.queue.put(MSG.ADDCART)
    
    def openCart(self):
        self.queue.put(MSG.DISPLAYCART)
        self.cartDlg = CartDlg()
        self.ThreadEmation.updateCart.connect(self.cartDlg.UpdateTableWidget)
        self.cartDlg.show()

    def Calc(self):
        if self.edt_quantity.text() =="":
            QMessageBox.critical(self,"错误","Empty Value Not Allowed!！")        
            self.edt_quantity.setFocus()
            return
        
        if(not self.productRecordList):
            return ;
        quantity_t = int(self.edt_quantity.text())

        for i, product in enumerate(self.productRecordList):
            quantity = quantity_t
            coeff = product.theRatio
            unitPrice=0
            if(quantity%coeff != 0):
                quantity = quantity/coeff + 1
            else:
                quantity = quantity/coeff
            product.purchasedNumber = quantity
            for k, priitem in enumerate(product.productPriceList):
                if( quantity >= priitem["startPurchasedNumber"] and  
                    quantity <= priitem["endPurchasedNumber"]): 
                    unitPrice = priitem["productPrice"]
            if(unitPrice == 0):
                print("can not found unit price")
            product.purchaseUnitPrice = unitPrice
            product.purchasedAmount = unitPrice * quantity * coeff

        for i, product in enumerate(self.productRecordList):
            price_item = MyTableWidgetItem(str(product.purchasedAmount), product.purchasedAmount)
            price_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 4, price_item)


    def UpdateStatusText(self, res):
        self.statusLabel.setText(res)
    
    def UpdateTableWidget(self, res):
        self.initTable( res, 0)

    def UpdateResultText(self, res):
        self.lbl_Result.setText(res)

    def initTable(self, productRecordList, table_rows):
        rowCnt = self.tableWidget.rowCount()
        # delete all lines
        for i in range(rowCnt -1, -1, -1):
            self.tableWidget.removeRow(i)
        self.productRecordList = productRecordList
        for i, product in enumerate(productRecordList):
            productname = product.productname
            productCode = product.productCode
            numberprices = product.numberprices
            stockNumber = product.stockNumber

            self.tableWidget.insertRow(table_rows)

            productname_item = QTableWidgetItem(productname)   
            productname_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)       
            

            productCode_item = QTableWidgetItem(productCode)
            productCode_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            numberprices_item = QTableWidgetItem(numberprices)
            numberprices_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

            stockNumber_item = QTableWidgetItem(stockNumber)
            stockNumber_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            price_item = QTableWidgetItem("price")
            price_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.tableWidget.setItem(i, 0, productname_item)
            self.tableWidget.setItem(i, 1, productCode_item)
            self.tableWidget.setItem(i, 2, numberprices_item)
            self.tableWidget.setItem(i, 3, stockNumber_item)
            #self.tableWidget.setItem(i, 4, price_item)
            table_rows +=1
        #self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(0, 240)
        self.tableWidget.setColumnWidth(2, 140)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)

class EmationThread(QtCore.QThread):  # 继承QThread
    updateSignal = QtCore.pyqtSignal(str)  # 注册一个信号
    updateViewSignal = QtCore.pyqtSignal(list)
    updateCart = QtCore.pyqtSignal(list)
    updateResultSignal = QtCore.pyqtSignal(str)
    goods_in_stock = False
    pageCount = 0
    def __init__(self, queue, parent= None): # 从前端界面中传递参数到这个任务后台
        self.queue = queue 
        super(EmationThread, self).__init__(parent)
        self.spider = Spider()

    def run(self):  # 重写run  比较耗时的后台任务可以在这里运行    
        spider = self.spider
        #msg = self.queue.get(block = False)
        numbers = {
            MSG.LOGIN : self.loginLCSC,
            MSG.SEARCH : self.crawlingLCSC,
            MSG.CONDITION_SEARCH : self.conditionSearch1,
            MSG.ADDCART : self.addCartAjax,
            MSG.DISPLAYCART: self.displayCart
        }
        while True:
            msg_id = self.queue.get()
            method = numbers.get(msg_id, "")
            if method:
                method()

    def displayCart(self):
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
        self.cartProductList =[]
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
            self.cartProductList.append(cartItem)
        savedir = os.getcwd() + "/cache"
        if(not os.path.exists(savedir)):
            os.makedirs(savedir)    
        for i, product in enumerate(self.cartProductList):
            product.localImg = spider.extractFileName(product.bigImageUrl, savedir)
            if(product.localImg == None):
                continue
            print("%s -- > %s"%(product.bigImageUrl, product.localImg))
            spider.spr_get_file(product.bigImageUrl, product.localImg)

        self.updateCart.emit(self.cartProductList)
        print("*"*80)
        #print(html)

    def addCartAjax(self):
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
        for page in range(2, pageCount):
            jo1 = self.singlePageSearch(page)
            if(not jo_resulut):
                return;
            #print(jo1["result"]['productRecordList'][0])
            self.parseItems(jo1['productRecordList'])
        self.updateViewSignal.emit(self.itemList)
        self.printLog("Complete!")

    def conditionSearch1(self):
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

        self.updateViewSignal.emit(self.itemList)
        self.printLog("Complete!")


    def crawlingLCSC(self):
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

    def loginLCSC(self):
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

if __name__== "__main__":
    
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    ui.loginToLCSC()
    sys.exit(app.exec_())
