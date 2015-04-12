# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctSeg.ui'
#
# Created: Tue Nov 26 08:11:54 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(817, 542)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 60, 288, 371))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.collectionTreeWidget = QtGui.QTreeWidget(self.layoutWidget)
        self.collectionTreeWidget.setObjectName(_fromUtf8("collectionTreeWidget"))
        self.collectionTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.collectionTreeWidget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.team1ComboBox = QtGui.QComboBox(self.layoutWidget)
        self.team1ComboBox.setObjectName(_fromUtf8("team1ComboBox"))
        self.horizontalLayout.addWidget(self.team1ComboBox)
        self.team2ComboBox = QtGui.QComboBox(self.layoutWidget)
        self.team2ComboBox.setObjectName(_fromUtf8("team2ComboBox"))
        self.horizontalLayout.addWidget(self.team2ComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.executeButton = QtGui.QPushButton(self.layoutWidget)
        self.executeButton.setObjectName(_fromUtf8("executeButton"))
        self.verticalLayout.addWidget(self.executeButton)
        self.layoutWidget1 = QtGui.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(380, 60, 401, 371))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graphicsView = QtGui.QGraphicsView(self.layoutWidget1)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.diceLabel = QtGui.QLabel(self.layoutWidget1)
        self.diceLabel.setObjectName(_fromUtf8("diceLabel"))
        self.verticalLayout_2.addWidget(self.diceLabel)
        self.imageSliceSlider = QtGui.QSlider(self.layoutWidget1)
        self.imageSliceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.imageSliceSlider.setObjectName(_fromUtf8("imageSliceSlider"))
        self.verticalLayout_2.addWidget(self.imageSliceSlider)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.executeButton.setText(_translate("Dialog", "Execute!", None))
        self.diceLabel.setText(_translate("Dialog", "TextLabel", None))
