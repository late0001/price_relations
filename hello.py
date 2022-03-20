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



if __name__== "__main__":
    
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    ui.loginToLCSC()
    sys.exit(app.exec_())
