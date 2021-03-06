# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shopping_cart.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from shopping_cartui import Ui_CartDlg 
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QTableWidgetItem

class CartItem():
    productId = 0
    productCode=""
    productName=""
    productModel=""
    shopCarMapKey=""
    shopCarId=""
    productNumber=0 #购买数量
    convesionRatio = 1
    productConsultPrice = 0
    productType=""
    productGradePlateName="" #品牌
    encapsulationModel="" #封装
    remark = "" #材质
    bigImageUrl = ""
    localImg = ""
    hasAnnexPDF = "no"
    gdDeliveryNum=0
    gdDivideSplitDeliveryNum=0
    isAllowUseCoupon="no" #是否允许使用优惠券
    jsValidStockNumber = 0 #江苏库存
    szValidStockNumber = 0 #广东库存
    stockNumber = 0 #总库存
    lineMoney = 0 #价格
    overseaProductTotalMoney = 0 #价格
    productCycle ="on_sale"

class Cart():
    discountMoney=0 #优惠金额
    cartTypeCount=0 #货品种类
    cartTypeGdCount=0 #广东发货种类
    cartOnlineMoney=0 #总价
    cartProductList=[]

class CartDlg(QDialog,Ui_CartDlg):
    def  __init__ (self):
        super(CartDlg, self).__init__()
        self.setupUi(self)
        ft = QFont()
        ft.setBold(True)
        ft.setPointSize(14)
        self.label_cartTypeCount.setFont(ft)
        self.label_cartTotalMoney.setFont(ft)
        pa= QPalette()
        pa.setColor(QPalette.WindowText,QColor(0xff7800))
        self.label_cartTypeCount.setPalette(pa)
        self.label_cartTotalMoney.setPalette(pa)

    def UpdateTotalMoney(self, cart):
        self.label_cartTypeCount.setText(str(cart.cartTypeCount))
        self.label_cartTotalMoney.setText(str(cart.cartOnlineMoney))


    def initTable(self, cartProductList, table_rows):
        rowCnt = self.tableWidget.rowCount()
        # delete all lines
        for i in range(rowCnt -1, -1, -1):
            self.tableWidget.removeRow(i)
        self.cartProductList = cartProductList
        for i, product in enumerate(cartProductList):
            productname = product.productName
            productCode = product.productCode + "\n" \
                    + str(product.productId)
            productInfo = product.productType + "/"+ product.productName + "\n" \
                    + product.productModel + " " + product.encapsulationModel + "\n" \
                    + product.productGradePlateName

            productConsultPrice = "￥"+ str(product.productConsultPrice)
            
            productNumber = str(product.productNumber * product.convesionRatio)

            stockNumber = product.stockNumber

            totalMoney = "￥"+ str(product.overseaProductTotalMoney)

            self.tableWidget.insertRow(table_rows)

            check = QTableWidgetItem()   
            check.setTextAlignment(Qt.AlignHCenter )  
            check.setCheckState(Qt.Checked)
            pix = QPixmap(product.localImg)
            label1= QLabel()
            label1.setScaledContents(True);#设置图片适应label
            label1.setPixmap(pix)
            productname_item = QTableWidgetItem(productname)   
            productname_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)       
            

            productCode_item = QTableWidgetItem(productCode)
            productCode_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            productInfo_item = QTableWidgetItem(productInfo)
            productInfo_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

            productConsultPrice_item = QTableWidgetItem(productConsultPrice)
            productConsultPrice_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            productNumber_item = QTableWidgetItem(productNumber)
            productNumber_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            stockNumber_item = QTableWidgetItem(stockNumber)
            stockNumber_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            totalMoney_item = QTableWidgetItem(totalMoney)
            totalMoney_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            price_item = QTableWidgetItem("price")
            price_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.tableWidget.setItem(i, 0, check)
            self.tableWidget.setCellWidget(i, 1, label1)
            self.tableWidget.setItem(i, 2, productCode_item)
            self.tableWidget.setItem(i, 3, productInfo_item)
            self.tableWidget.setItem(i, 4, productConsultPrice_item)
            self.tableWidget.setItem(i, 5, productNumber_item)
            self.tableWidget.setItem(i, 6, stockNumber_item)
            self.tableWidget.setItem(i, 7, totalMoney_item)
            
            #self.tableWidget.setItem(i, 4, price_item)
            table_rows +=1
        #self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(3, 240)
        #self.tableWidget.setColumnWidth(2, 140)

    def UpdateTableWidget(self, res):
        self.UpdateTotalMoney(res)
        self.initTable( res.cartProductList, 0)
