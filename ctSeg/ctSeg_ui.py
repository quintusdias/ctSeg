# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctSeg.ui'
#
# Created: Tue Nov 26 08:11:54 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("CtSeg")
        Dialog.resize(817, 542)

        self.selectionWidget = QtGui.QWidget(Dialog)
        self.selectionWidget.setGeometry(QtCore.QRect(50, 60, 288, 371))
        self.selectionWidget.setObjectName("selectionWidget")

        self.selectionLayout = QtGui.QVBoxLayout(self.selectionWidget)
        self.selectionLayout.setMargin(0)
        self.selectionLayout.setObjectName("selectionLayout")

        self.collectionTreeWidget = QtGui.QTreeWidget(self.selectionWidget)
        self.collectionTreeWidget.setObjectName("collectionTreeWidget")
        self.collectionTreeWidget.headerItem().setText(0, "1")
        self.selectionLayout.addWidget(self.collectionTreeWidget)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.selectionLayout.addItem(spacerItem)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.team1ComboBox = QtGui.QComboBox(self.selectionWidget)
        self.team1ComboBox.setObjectName("team1ComboBox")
        self.horizontalLayout.addWidget(self.team1ComboBox)

        self.team2ComboBox = QtGui.QComboBox(self.selectionWidget)
        self.team2ComboBox.setObjectName("team2ComboBox")
        self.horizontalLayout.addWidget(self.team2ComboBox)
        self.selectionLayout.addLayout(self.horizontalLayout)

        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.selectionLayout.addItem(spacerItem1)
        self.executeButton = QtGui.QPushButton(self.selectionWidget)
        self.executeButton.setObjectName("executeButton")
        self.executeButton.setText("")
        self.selectionLayout.addWidget(self.executeButton)

        self.displayWidget = QtGui.QWidget(Dialog)
        self.displayWidget.setGeometry(QtCore.QRect(380, 60, 401, 371))
        self.displayWidget.setObjectName("displayWidget")

        self.displayLayout = QtGui.QVBoxLayout(self.displayWidget)
        self.displayLayout.setMargin(0)
        self.displayLayout.setObjectName("displayLayout")

        self.graphicsView = QtGui.QGraphicsView(self.displayWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.displayLayout.addWidget(self.graphicsView)

        self.diceLabel = QtGui.QLabel(self.displayWidget)
        self.diceLabel.setObjectName("diceLabel")
        self.diceLabel.setText("")
        self.displayLayout.addWidget(self.diceLabel)

        self.imageSliceSlider = QtGui.QSlider(self.displayWidget)
        self.imageSliceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.imageSliceSlider.setObjectName("imageSliceSlider")
        self.displayLayout.addWidget(self.imageSliceSlider)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
