# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'playlist.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Playlist(object):
    def setupUi(self, Playlist):
        Playlist.setObjectName("Playlist")
        Playlist.resize(629, 473)
        self.makeplaylist = QtWidgets.QPushButton(Playlist)
        self.makeplaylist.setGeometry(QtCore.QRect(390, 350, 93, 28))
        self.makeplaylist.setObjectName("makeplaylist")
        self.splitter = QtWidgets.QSplitter(Playlist)
        self.splitter.setGeometry(QtCore.QRect(320, 40, 221, 81))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.listnameedit = QtWidgets.QLineEdit(self.splitter)
        self.listnameedit.setObjectName("listnameedit")
        self.layoutWidget = QtWidgets.QWidget(Playlist)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 140, 521, 194))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.layoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.listWidget_2 = QtWidgets.QListWidget(self.layoutWidget)
        self.listWidget_2.setObjectName("listWidget_2")
        self.horizontalLayout.addWidget(self.listWidget_2)
        self.label_2 = QtWidgets.QLabel(Playlist)
        self.label_2.setGeometry(QtCore.QRect(50, 60, 201, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Playlist)
        QtCore.QMetaObject.connectSlotsByName(Playlist)

    def retranslateUi(self, Playlist):
        _translate = QtCore.QCoreApplication.translate
        Playlist.setWindowTitle(_translate("Playlist", "Dialog"))
        self.makeplaylist.setText(_translate("Playlist", "Oluştur"))
        self.label.setText(_translate("Playlist", "Çalma Listesine bir isim veriniz:"))
        self.label_2.setText(_translate("Playlist", "<html><head/><body><p align=\"center\">Eklemek istediğiniz</p><p align=\"center\">müzikleri seçiniz</p></body></html>"))

