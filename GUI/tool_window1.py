# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tool_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(928, 678)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rule_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.rule_tableWidget.setObjectName("rule_tableWidget")
        self.rule_tableWidget.setColumnCount(0)
        self.rule_tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.rule_tableWidget, 0, 0, 1, 3)
        self.file_frame = QtWidgets.QFrame(self.centralwidget)
        self.file_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.file_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.file_frame.setObjectName("file_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.file_frame)
        self.gridLayout.setObjectName("gridLayout")
        self.file2_treeView = QtWidgets.QTreeView(self.file_frame)
        self.file2_treeView.setObjectName("file2_treeView")
        self.gridLayout.addWidget(self.file2_treeView, 1, 1, 1, 1)
        self.file1_treeView = QtWidgets.QTreeView(self.file_frame)
        self.file1_treeView.setObjectName("file1_treeView")
        self.gridLayout.addWidget(self.file1_treeView, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.file_frame, 1, 0, 1, 3)
        self.undo_toolButton = QtWidgets.QToolButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.undo_toolButton.setFont(font)
        self.undo_toolButton.setObjectName("undo_toolButton")
        self.gridLayout_2.addWidget(self.undo_toolButton, 2, 0, 1, 1)
        self.sync_pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.sync_pushButton.setFont(font)
        self.sync_pushButton.setObjectName("sync_pushButton")
        self.gridLayout_2.addWidget(self.sync_pushButton, 2, 1, 1, 1)
        self.exit_pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.exit_pushButton.setFont(font)
        self.exit_pushButton.setObjectName("exit_pushButton")
        self.gridLayout_2.addWidget(self.exit_pushButton, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.undo_toolButton.setText(_translate("MainWindow", "..."))
        self.sync_pushButton.setText(_translate("MainWindow", "同步所有"))
        self.exit_pushButton.setText(_translate("MainWindow", "退出"))