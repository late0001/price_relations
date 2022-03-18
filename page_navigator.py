from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIntValidator
from page_nav_ui import Ui_PageNavigator

def qMax(a, b):
	return a if a >= b else b

def qMin(a, b):
	return a if a <= b else b

class PageNavigator(QWidget):
	m_maxPage = 0
	m_blockSize = 0
	m_pageLabels = []
	currentPageChanged = QtCore.pyqtSignal(int)
	def __init__(self, blockSize = 3, parent= None):
		super(PageNavigator, self).__init__(parent)
		self.ui = Ui_PageNavigator()
		self.ui.setupUi(self)
		self.setBlockSize(blockSize)
		self.initialize();

		self.m_maxPage = 0
		self.setMaxPage(1)
		qss = """
.QLabel[page="true"] 
{ padding: 6px; }
.QLabel[currentPage="true"] 
{ color: rgb(190, 0, 0);}
.QLabel[page="true"]:hover { 
		color: white; border-radius: 4px; 
		background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:1, 
			stop:0 rgba(53, 121, 238, 255), 
			stop:1 rgba(0, 202, 237, 255)
		);
}
"""
		self.setStyleSheet(qss)

	def eventFilter(self, watched, event):
		if(event.type() == QEvent.MouseButtonRelease):
			page = -1
			if(watched == self.ui.previousPageLabel):
				page = self.getCurrentPage() - 1

			if(watched == self.ui.nextPageLabel):
				page = self.getCurrentPage() + 1

			if(watched == self.m_pageHead):
				page = 1
			if(watched == self.m_pageTail):
				page = int(self.m_pageTail.text())
			for i in range(0, len(self.m_pageLabels)):
				if( watched == self.m_pageLabels[i]):
					page = int(self.m_pageLabels[i].text())
					break
			if( -1 != page):
				if(self.ui.pageLineEdit.text().strip()):
					self.ui.pageLineEdit.clear()
				print("page = ", page)
				self.setCurrentPage(page, True)
				return True	

		if(watched == self.ui.pageLineEdit and event.type() == QEvent.KeyRelease):
			ke= event
			if(ke.key() == Qt.Key_Enter or ke.key() == Qt.Key_Return):
				self.setCurrentPage(int(self.ui.pageLineEdit.text()), True)
				return True;
		return super().eventFilter(watched, event)

	def getBlockSize(self):
		return self.m_blockSize

	def getMaxPage(self):
		return self.m_maxPage

	def getCurrentPage(self):
		return self.m_currentPage

	def setMaxPage(self, page):
		page = qMax(page, 1)
		if(self.m_maxPage != page):
			self.m_maxPage = page
			self.m_currentPage = 1
			self.updatePageLabels()

	def setCurrentPage(self, page, signalEmitted = False):
		page = qMax(page, 1)
		page = qMin(page, self.m_maxPage)
		if(page != self.m_currentPage):
			self.m_currentPage = page
			self.updatePageLabels()
			if(signalEmitted):
				self.currentPageChanged.emit(page)

	def setBlockSize(self, blockSize):
		blockSize = qMax(blockSize, 3)
		if(blockSize % 2 == 0):
			blockSize +=1
		self.m_blockSize = blockSize


	def addNewLabel(self, page):
		label = QtWidgets.QLabel(str(page), self)
		label.setProperty("page", "true")
		label.installEventFilter(self)	
		return label

	def initialize(self):
		self.ui.pageLineEdit.installEventFilter(self)
		self.ui.pageLineEdit.setValidator(QIntValidator(1, 10000000, self))
		self.ui.nextPageLabel.setProperty("page", "true")
		self.ui.previousPageLabel.setProperty("page", "true")
		self.ui.nextPageLabel.installEventFilter(self)
		self.ui.previousPageLabel.installEventFilter(self)

		self.m_pageLabels = []

		leftLayout = QtWidgets.QHBoxLayout()
		self.centerLayout = QtWidgets.QHBoxLayout()
		rightLayout = QtWidgets.QHBoxLayout()
		leftLayout.setContentsMargins(0, 0, 0, 0)
		leftLayout.setSpacing(0)
		self.centerLayout.setContentsMargins(0, 0, 0, 0)
		self.centerLayout.setSpacing(0)
		rightLayout.setContentsMargins(0, 0, 0, 0)
		rightLayout.setSpacing(0)

		self.m_pageHead = self.addNewLabel(1)
		leftLayout.addWidget(self.m_pageHead)

		self.m_pageTail = self.addNewLabel(5)
		rightLayout.addWidget(self.m_pageTail)

		for i in range(0, 5):
			label= self.addNewLabel(i+2)		
			self.m_pageLabels.append(label)
			self.centerLayout.addWidget(label)

		self.ui.getLeftPagesWidget().setLayout(leftLayout)
		self.ui.centerPagesWidget.setLayout(self.centerLayout)
		self.ui.rightPagesWidget.setLayout(rightLayout)

	def setSelectStyleSheet(self, page, label):
		if (page ==self.m_currentPage):
			label.setProperty("currentPage", "true")
		else:
			label.setProperty("currentPage", "false")

		label.setStyleSheet("/**/")

	def updatePageLabels(self):
		print("updatePageLabels")
		self.ui.leftSeparateLabel.hide()
		self.ui.rightSeparateLabel.hide()

		if(self.m_maxPage < 5):
			for i in range(0, len(self.m_pageLabels) ):
				label = self.m_pageLabels[i]
				page = i +2
				if(page < self.m_maxPage):
					label.setText(str(i + 2))
					label.show()
				else:
					label.hide()
				if(self.m_currentPage  == page):
					label.setProperty("currentPage", "true")
				else:
					label.setProperty("currentPage", "false")
				label.setStyleSheet("/**/")
			return
			
		c = self.m_currentPage
		n = self.m_blockSize
		m = self.m_maxPage
		centerStartPage = 0
		if( c >= 1 and c < m - 2):
			centerStartPage = c - 2
			self.ui.rightSeparateLabel.show()
		elif ( c >= 4):
			centerStartPage = c - 2
			self.ui.leftSeparateLabel.show()

		self.m_pageTail.setText(str(m))
		if(c -2 >= 2 ):
			if(c + 2 < m ):
				centerStartPage = c -2;
			elif( c + 2 >= m):
				centerStartPage = m - 3 - 2  
			self.ui.leftSeparateLabel.show()
			
		else:
		#if( c - 2 < 2 ):
			centerStartPage = 2;
		
		self.setSelectStyleSheet(1, self.m_pageHead)
		self.setSelectStyleSheet(self.m_maxPage, self.m_pageTail)
		for i in range(0, len(self.m_pageLabels)):
			label = self.m_pageLabels[i]
			label.setText(str(centerStartPage + i))
			page = centerStartPage + i
			#page = int(self.m_pageLabels[i].text())
			if(page > c + 2):
				#print("page > ", str(c + 2), ", m_pageLabels["+ str(i) + "] need hide()" )
				label.hide()
			elif(page < c -2 ):
				#print("page < ", str(c - 2), ", m_pageLabels["+ str(i) + "] need hide()" )
				label.hide()
			else:
				self.setSelectStyleSheet(page, label)
				label.show();
			
			
		for i in range(0, len(self.m_pageLabels)):
			label = self.m_pageLabels[i]
			print("----------- ", label.text())


	
