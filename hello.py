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
from page_navigator import PageNavigator
from queue import Queue
import sys
from emation_thread import EmationThread
from emation_thread import MSG
from tmessage import MessageNode
from tmessage import Looper
from hq_thread import HqThread
from hq_thread import HQMSG


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
        self.pageNavigator.currentPageChanged.connect(self.pageChanged)
        self.btnSearch.clicked.connect(self.searchBtnClicked)
        self.btn_Addcart.clicked.connect(self.addCart)
        self.ckb_spot.stateChanged.connect(self.changeCkbSpot)
        self.btn_Calc.clicked.connect(self.calc)
        self.btn_AllPage.clicked.connect(self.resultAllPage)
        self.cartBtn.clicked.connect(self.openCart)
        self.tableWidget.setSortingEnabled(True);
        self.tableWidget.sortByColumn(4, Qt.AscendingOrder)
        self.looper = Looper()
        self.ThreadEmation = EmationThread(self.looper)
        self.ThreadEmation.updateSignal.connect(self.UpdateStatusText) 
        self.ThreadEmation.updateViewSignal.connect(self.UpdateTableWidget)
        self.ThreadEmation.updateResultSignal.connect(self.UpdateResultText)
        self.ThreadEmation.updateRecordCnt.connect(self.UpdateRecordCnt)
        self.productRecordList = []
        self.hqLooper = Looper()
        self.ThreadHq = HqThread(self.hqLooper)
        self.ThreadHq.updateSignal.connect(self.UpdateStatusText)
        self.ThreadHq.updateViewSignal.connect(self.UpdateTableWidget)
        self.radioLCSC.toggled.connect(lambda :self.radioBtnState(self.radioLCSC))
        self.radioHQ.toggled.connect(lambda :self.radioBtnState(self.radioHQ))
        self.radioLCSC.setChecked(True)
        self.fromsite = 1

    def radioBtnState(self, btn):
        if btn.text()=='????????????':
            if(btn.isChecked()):
                self.fromsite = 1
        if( btn.text()== '????????????'):
            if(btn.isChecked()):
                self.fromsite = 2

    def loginToLCSC(self):
        msg = MessageNode(MSG.LOGIN)
        self.looper.sendMessage(msg)
        self.ThreadEmation.start()
   
    def loginToHqChip(self):
        msg = MessageNode(HQMSG.LOGIN)
        self.hqLooper.sendMessage(msg)
        self.ThreadHq.start()

    def openDialog(self):
        filename, filetype =QFileDialog.getOpenFileName(self, "????????????", "C:/", "All Files(*);;Text Files(*.csv)")
        print(filename, filetype)
        self.lineEdit.setText(filename)
    
    def changeCkbSpot(self):
         if self.ckb_spot.checkState() == Qt.Checked:
            self.ThreadEmation.setSearchCriteria(True)
            msg = MessageNode(MSG.CONDITION_SEARCH)
            self.looper.sendMessage(msg)

    def pageChanged(self, page):
        msg = MessageNode(MSG.SEARCH_PAGE, page)
        self.looper.sendMessage(msg)

    def resultAllPage(self):
        msg = MessageNode(MSG.SEARCH_PAGE, 0)
        self.looper.sendMessage(msg)

    def searchBtnClicked(self):
        if(self.fromsite == 1):
            msg = MessageNode(MSG.SEARCH)
            self.looper.sendMessage(msg)
        if(self.fromsite == 2):
            msg = MessageNode(HQMSG.SEARCH)
            self.hqLooper.sendMessage(msg)

    def addCart(self):
        msg = MessageNode(MSG.ADDCART)
        self.looper.sendMessage(msg)
    
    def UpdateRecordCnt(self, recordCnt, pageCnt):
        print("UpdateRecordCnt =====>")
        self.pageNavigator.setMaxPage(pageCnt)

    def openCart(self):
        msg = MessageNode(MSG.DISPLAYCART)
        self.looper.sendMessage(msg)
        self.cartDlg = CartDlg()
        self.ThreadEmation.updateCart.connect(self.cartDlg.UpdateTableWidget)
        self.cartDlg.show()

    def calc(self):
        if self.edt_quantity.text() =="":
            QMessageBox.critical(self,"??????","Empty Value Not Allowed!???")        
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
            price_item = MyTableWidgetItem("{:.4f}".format(product.purchasedAmount), product.purchasedAmount)
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
            stockNumber_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

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
        self.tableWidget.setColumnWidth(2, 150)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)



if __name__== "__main__":
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    #ui.loginToLCSC()
    ui.loginToHqChip()
    sys.exit(app.exec_())
