# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shopping_cart.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CartDlg(object):
    def setupUi(self, CartDlg):
        CartDlg.setObjectName("CartDlg")
        CartDlg.resize(1132, 572)
        self.buttonBox = QtWidgets.QDialogButtonBox(CartDlg)
        self.buttonBox.setGeometry(QtCore.QRect(920, 530, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(CartDlg)
        self.tableWidget.setGeometry(QtCore.QRect(10, 30, 1111, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        self.label = QtWidgets.QLabel(CartDlg)
        self.label.setGeometry(QtCore.QRect(430, 530, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(CartDlg)
        self.label_2.setGeometry(QtCore.QRect(510, 530, 321, 16))
        self.label_2.setObjectName("label_2")
        self.label_cartTypeCount = QtWidgets.QLabel(CartDlg)
        self.label_cartTypeCount.setGeometry(QtCore.QRect(480, 530, 21, 21))
        self.label_cartTypeCount.setObjectName("label_cartTypeCount")
        self.label_cartTotalMoney = QtWidgets.QLabel(CartDlg)
        self.label_cartTotalMoney.setGeometry(QtCore.QRect(840, 530, 81, 21))
        self.label_cartTotalMoney.setObjectName("label_cartTotalMoney")

        self.retranslateUi(CartDlg)
        self.buttonBox.accepted.connect(CartDlg.accept)
        self.buttonBox.rejected.connect(CartDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(CartDlg)

    def retranslateUi(self, CartDlg):
        _translate = QtCore.QCoreApplication.translate
        CartDlg.setWindowTitle(_translate("CartDlg", "购物车"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("CartDlg", "新建列"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("CartDlg", "图"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("CartDlg", "商品编号"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("CartDlg", "商品信息"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("CartDlg", "单价"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("CartDlg", "数量"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("CartDlg", "发货仓库"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("CartDlg", "金额"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("CartDlg", "操作"))
        self.label.setText(_translate("CartDlg", "已选中"))
        self.label_2.setText(_translate("CartDlg", "种商品（广东发货4种） 总价（不含运费）：￥"))
        self.label_cartTypeCount.setText(_translate("CartDlg", "1"))
        self.label_cartTotalMoney.setText(_translate("CartDlg", "0"))
