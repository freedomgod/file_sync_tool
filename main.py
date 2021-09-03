from GUI import tool_window, add_rule_window
import os
import sys
import json
import shutil
from util.file_operate import file_handle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

app = QApplication(sys.argv)


class add_rule_dialog(QtWidgets.QDialog):
    new_rule_signal = QtCore.pyqtSignal(dict)  # 添加规则返回的字典信号

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.add_dialog = add_rule_window.Ui_Dialog()
        self.add_dialog.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.setWindowIcon(QtGui.QIcon('resources/文件-同步.png'))
        self.add_dialog.folder1_toolButton.setIcon(QtGui.QIcon('resources/文件夹.png'))
        self.add_dialog.folder2_toolButton.setIcon(QtGui.QIcon('resources/文件夹.png'))
        self.add_dialog.file1_toolButton.setIcon(QtGui.QIcon('resources/文件.png'))
        self.add_dialog.file2_toolButton.setIcon(QtGui.QIcon('resources/文件.png'))

        self.add_dialog.folder1_toolButton.clicked.connect(self.select_path)
        self.add_dialog.folder2_toolButton.clicked.connect(self.select_path)
        self.add_dialog.file1_toolButton.clicked.connect(self.select_path)
        self.add_dialog.file2_toolButton.clicked.connect(self.select_path)
        self.add_dialog.file_path_lineEdit.textChanged.connect(self.show_path)
        self.add_dialog.sync_path_lineEdit.textChanged.connect(self.show_path)

    def show_path(self):
        """
        对选择好的路径，显示文件夹内容
        :return:
        """
        if self.sender() == self.add_dialog.file_path_lineEdit:
            self.tree_model1 = QtWidgets.QFileSystemModel()
            self.tree_model1.setRootPath(self.add_dialog.file_path_lineEdit.text())
            self.add_dialog.file_treeView.setModel(self.tree_model1)
            self.add_dialog.file_treeView.setRootIndex(self.tree_model1.index(self.add_dialog.file_path_lineEdit.text()))
        else:
            self.tree_model2 = QtWidgets.QFileSystemModel()
            self.tree_model2.setRootPath(self.add_dialog.sync_path_lineEdit.text())
            self.add_dialog.sync_treeView.setModel(self.tree_model2)
            self.add_dialog.sync_treeView.setRootIndex(self.tree_model2.index(self.add_dialog.sync_path_lineEdit.text()))

    def select_path(self):
        """
        打开文件路径选择窗口，选择路径
        :return:
        """
        file_dig = QFileDialog()
        button_name = self.sender().objectName()
        if button_name.find('file') == -1:
            file_dig.setFileMode(QFileDialog.Directory)
            if file_dig.exec_():
                file_path = file_dig.selectedFiles()[0]
                if self.sender() == self.add_dialog.folder1_toolButton:
                    self.add_dialog.file_path_lineEdit.setText(file_path)
                else:
                    self.add_dialog.sync_path_lineEdit.setText(file_path)
        else:
            file_dig.setFileMode(QFileDialog.ExistingFiles)
            if file_dig.exec_():
                file_path = file_dig.selectedFiles()[0]
                if self.sender() == self.add_dialog.file1_toolButton:
                    self.add_dialog.file_path_lineEdit.setText(file_path)
                else:
                    self.add_dialog.sync_path_lineEdit.setText(file_path)

    def check_rule(self) -> bool:
        """
        检查规则的合法性
        :return:
        """
        rule_name = self.add_dialog.rulename_lineEdit.text()
        file_path = self.add_dialog.file_path_lineEdit.text()
        sync_path = self.add_dialog.sync_path_lineEdit.text()
        if rule_name.isspace() or (not rule_name):  # 规则名称合法性检查
            return False
        if not (os.path.exists(file_path) and os.path.exists(sync_path)):  # 路径有效性检查
            return False
        elif os.path.isdir(file_path) == os.path.isfile(sync_path):
            return False
        return True

    def accept(self) -> None:
        """
        保存规则的操作，会检查规则的合法性
        :return:
        """
        if self.check_rule():
            self.new_rule_signal.emit({
                "rule_name": self.add_dialog.rulename_lineEdit.text(),
                "file_path": self.add_dialog.file_path_lineEdit.text(),
                "sync_path": self.add_dialog.sync_path_lineEdit.text()
            })
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, '警告', '请检查规则的合法性！\n1.规则名称不能为空;\n2.路径使用正斜杠;'
                                                      '\n3.两个路径须同为目录或文件',
                                          QtWidgets.QMessageBox.Yes)


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.createmenu()

    def createmenu(self):
        self.menu = QtWidgets.QMenu()
        self.showAction1 = QtWidgets.QAction("主界面", self, triggered=self.show_window)
        self.showAction2 = QtWidgets.QAction("显示通知", self, triggered=self.showMsg)
        self.quitAction = QtWidgets.QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # 设置图标
        self.setIcon(QtGui.QIcon("resources/文件-同步.png"))
        self.icon = self.MessageIcon()

        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.oniconclicked)

    def showMsg(self):
        self.showMessage("Message", "skr at here", self.icon)

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        QtWidgets.qApp.quit()

    def oniconclicked(self, reason):
        """
        鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        :param reason: 
        :return: 
        """
        if reason == 2 or reason == 3:
            # self.showMessage("Message", "skr at here", self.icon)
            if self.ui.isMinimized() or not self.ui.isVisible():
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.setWindowFlags(QtCore.Qt.Window)
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()
                self.ui.setWindowFlags(QtCore.Qt.SplashScreen)
                self.ui.show()
                # self.ui.show()


class main_window(tool_window.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.setupUi(self)

        self.rule_tableWidget.cellClicked.connect(self.show_rule_slot)
        self.exit_pushButton.clicked.connect(self.totray_slot)
        self.sync_pushButton.clicked.connect(self.sync_file_slot)
        self.undo_toolButton.clicked.connect(self.undo_slot)

        self.setWindowIcon(QtGui.QIcon('resources/文件-同步.png'))
        self.undo_toolButton.setIcon(QtGui.QIcon('resources/撤销.png'))

        self.init_rule()

    def init_rule(self):
        """
        初始化规则的内容
        :return:
        """
        with open('rule.json', 'r') as fp:
            res = json.load(fp)
        n_rule = len(res)

        n_col = 3
        self.rule_tableWidget.clear()
        self.rule_tableWidget.clearSpans()
        self.rule_tableWidget.setRowCount(n_rule + 1)
        self.rule_tableWidget.setColumnCount(n_col + 1)
        self.rule_tableWidget.setSpan(n_rule, 0, 1, n_col + 1)
        self.add_pushButton = QtWidgets.QPushButton()
        self.add_pushButton.setIcon(QtGui.QIcon('resources/添加.png'))
        self.rule_tableWidget.setCellWidget(n_rule, 0, self.add_pushButton)
        self.add_pushButton.clicked.connect(self.add_rule_slot)  # 添加规则的按钮连接槽函数

        item = QtWidgets.QTableWidgetItem('rule_name')
        self.rule_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('file_path')
        self.rule_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem('sync_path')
        self.rule_tableWidget.setHorizontalHeaderItem(2, item)
        for i, rule in zip(range(n_rule), res):
            for j, v in zip(range(n_col), rule.values()):
                item = QtWidgets.QTableWidgetItem(v)
                self.rule_tableWidget.setItem(i, j, item)
                if j == n_col - 1:
                    names = self.__dict__
                    names[f'delete_rule{i}'] = QtWidgets.QPushButton()
                    names[f'delete_rule{i}'].setIcon(QtGui.QIcon('resources/删除筛选项.png'))
                    names[f'delete_rule{i}'].setObjectName(f"delete_rule{i}")
                    names[f'delete_rule{i}'].clicked.connect(self.delete_rule_slot)
                    self.rule_tableWidget.setCellWidget(i, j + 1, names[f'delete_rule{i}'])

    def delete_rule_slot(self):
        """
        删除一条规则
        :return:
        """
        rule_idx = int(self.sender().objectName()[11:])
        with open('rule.json', 'r') as fp:
            rule_list = json.load(fp)
        rule_list.pop(rule_idx)
        with open('rule.json', 'w') as fp:
            json.dump(rule_list, fp, ensure_ascii=False, indent=2)
        self.init_rule()

    def add_rule_slot(self):
        """
        弹出添加规则的窗口
        :return:
        """
        self.add_rule_gui = add_rule_dialog()
        self.add_rule_gui.show()
        self.add_rule_gui.new_rule_signal.connect(self.save_rule_slot)

    def save_rule_slot(self, rule_dict: dict):
        """
        保存添加的规则
        :param rule_dict: 传递的字典信号
        :return:
        """
        with open('rule.json', 'r') as fp:
            rule_list = json.load(fp)
        rule_list.append(rule_dict)
        with open('rule.json', 'w') as fp:
            json.dump(rule_list, fp, ensure_ascii=False, indent=2)
        self.init_rule()

    def show_rule_slot(self):
        """
        显示选中的规则的文件视图
        :return:
        """
        file_path = self.rule_tableWidget.selectedItems()[1].text()
        sync_path = self.rule_tableWidget.selectedItems()[2].text()
        self.tree_model1 = QtWidgets.QFileSystemModel()
        self.tree_model1.setRootPath(file_path)
        self.file1_treeView.setModel(self.tree_model1)
        self.file1_treeView.setRootIndex(self.tree_model1.index(file_path))

        self.tree_model2 = QtWidgets.QFileSystemModel()
        self.tree_model2.setRootPath(sync_path)
        self.file2_treeView.setModel(self.tree_model2)
        self.file2_treeView.setRootIndex(self.tree_model2.index(sync_path))

    def sync_file_slot(self):
        """
        同步文件
        :return:
        """
        fh = file_handle()
        res = fh.sync_file()
        print(res)
        QtWidgets.QMessageBox.information(self, '提示', '文件同步完成!', QtWidgets.QMessageBox.Ok)

    def undo_slot(self):
        """
        撤销同步操作，还原文件
        :return:
        """
        file_handle().undo()
        QtWidgets.QMessageBox.information(self, '提示', '撤销文件同步!', QtWidgets.QMessageBox.Ok)

    def totray_slot(self):
        """
        退出程序
        :return:
        """
        self.close()

    def closeEvent(self, event):
        """
        重写关闭事件
        :param event: 点击关闭的信号
        :return: None
        """
        reply = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, self.tr("提示"),
                                      self.tr("你确定要退出吗？"), QtWidgets.QMessageBox.NoButton, self)
        yr_btn = reply.addButton(self.tr("退出"), QtWidgets.QMessageBox.YesRole)
        reply.addButton(self.tr("隐藏至托盘"), QtWidgets.QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton() == yr_btn:
            event.accept()
            QtWidgets.qApp.quit()
        else:
            event.ignore()
            self.hide()
            self.tray_app = TrayIcon(self)
            self.tray_app.show()
            # event.ignore()
            # # 最小化到托盘
            # MainWindow.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)
            # MainWindow.showMinimized()


if __name__ == '__main__':
    a = main_window()
    a.show()
    sys.exit(app.exec_())
