# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cmpp.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Nima(object):
    def setupUi(self, Nima):
        Nima.setObjectName("Nima")
        Nima.resize(1004, 628)
        self.centralwidget = QtWidgets.QWidget(Nima)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 851, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(890, 30, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(10, 580, 731, 16))
        self.statusLabel.setObjectName("statusLabel")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 90, 961, 451))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        Nima.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Nima)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1004, 26))
        self.menubar.setObjectName("menubar")
        Nima.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Nima)
        self.statusbar.setObjectName("statusbar")
        Nima.setStatusBar(self.statusbar)

        self.retranslateUi(Nima)
        QtCore.QMetaObject.connectSlotsByName(Nima)

    def retranslateUi(self, Nima):
        _translate = QtCore.QCoreApplication.translate
        Nima.setWindowTitle(_translate("Nima", "Nima"))
        self.pushButton.setText(_translate("Nima", "PushButton"))
        self.statusLabel.setText(_translate("Nima", "TextLabel"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Nima", "商品"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Nima", "编号"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Nima", "价格"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Nima", "库存"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Nima", "购价"))
