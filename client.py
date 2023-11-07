import socket
import time
import os
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
#from qt_material import apply_stylesheet
import sys
running = False
opname = ""
flag = True
ip = "127.0.0.1"
port = 10000
username = ""
codemd = False
version = "2.0.6"  # 版本号

class GUI(object):
    def __init__(self, c, Form, version):
        self.version = version
        self.c = c
        self.Form = Form
        self.setupUi(Form)
        self.textEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.codeclick)
        self.pushButton_3.clicked.connect(self.fileclick)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.textEdit.setFontFamily("Consolas")
    def codeclick(self):
        codeewindow = QtWidgets.QWidget()
        self.ui = codewindow(self.c, codeewindow, self.version)
    def click(self):
        data = self.lineEdit.text()
        self.c.send(data.encode("utf-8"))
        self.lineEdit.setText("")
    def send(self, data):
        self.textEdit.append(data)
    def sendwarning(self, data):
        self.textEdit.append("<font color=\"#FF0000\">" + data + "</font>")
    def fileclick(self):
        fileewindow = QtWidgets.QWidget()
        self.ui = filewindow(self.c, fileewindow, self.version)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(506, 405)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 50, 481, 291))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 350, 361, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 350, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 10, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 10, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "发送"))
        self.pushButton_2.setText(_translate("Form", "代码模式"))
        self.pushButton_3.setText(_translate("Form", "发送文件"))


class codewindow(object):
    def __init__(self, c, Form, version):
        self.version = version
        self.Form = Form
        self.c = c
        super().__init__()
        self.setupUi(Form)
        self.pushButton.clicked.connect(self.click)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.Form.show()
    def click(self):
        data = self.TextEdit.toPlainText()
        data = "发送了代码：" + "\n" + data + "\n"
        self.c.send(data.encode("utf-8"))
        self.TextEdit.setText("")
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(483, 434)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName("label")
        self.TextEdit = QtWidgets.QTextEdit(Form)
        self.TextEdit.setGeometry(QtCore.QRect(10, 50, 461, 371))
        self.TextEdit.setObjectName("TextEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "发送"))

class filewindow(object):
    def __init__(self, c, Form, version):
        self.version = version
        self.c = c
        self.Form = Form
        self.setupUi(Form)
        self.pushButton.clicked.connect(self.get_path)
        self.pushButton_2.clicked.connect(self.click)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.Form.show()
    def get_path(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(None, "请选择文件路径", "", "All files (*.*)")
        self.lineEdit.setText(filename)
    def click(self):
        global ui
        data = self.lineEdit.text()
        if data == "":
            return
        try:
            f = open(data, "rb")
            ui.send("正在发送文件...")
            self.c.send("!!!file".encode("utf-8"))
            data = os.path.basename(data)
            self.c.send(data.encode("utf-8"))
            print(data)
            self.c.sendall(f.read())
            time.sleep(5)
            self.c.send(b"!!!endfile")
            f.close()
        except:
            ui.send("发送文件失败！")
        finally:
            self.lineEdit.setText("")
            self.Form.close()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(483, 156)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(80, 50, 271, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 81, 31))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(370, 50, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 100, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">路径：</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "选择"))
        self.pushButton_2.setText(_translate("Form", "发送"))


class namewindow(object):
    def click(self):
        global username
        username = self.lineEdit.text()
        self.window.close()
    def setupUi(self, Form, version):
        self.version = version
        self.window = Form
        Form.setObjectName("Form")
        Form.resize(295, 116)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 161, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(122, 40, 151, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 171, 21))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(100, 70, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.click)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        reg = QtCore.QRegExp("[a-zA-Z0-9]+$")
        regVal = QtGui.QRegExpValidator()
        regVal.setRegExp(reg)
        self.lineEdit.setValidator(regVal)
        self.lineEdit.setMaxLength(16)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.lineEdit.setToolTip(_translate("Form", "<html><head/><body><p>输入服务器 IP</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">输入用户名：</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "确定"))

class ipportwindow(object):
    def click(self):
        # pass
        global ip
        global port
        ip = self.lineEdit.text()
        port = int(self.lineEdit_2.text())
        self.window.close()
    def setupUi(self, Form, version):
        self.version = version
        self.window = Form
        Form.setObjectName("Form")
        Form.resize(295, 185)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 161, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 60, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 171, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 171, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(90, 130, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.click)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.lineEdit.setToolTip(_translate("Form", "<html><head/><body><p>输入服务器 IP</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">输入服务器 IP :</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">输入服务器端口:</span></p></body></html>"))
        self.lineEdit_2.setToolTip(_translate("Form", "<html><head/><body><p>输入服务器 IP</p></body></html>"))
        self.pushButton.setText(_translate("Form", "确定"))

class showgui():
    def __init__(self, c):
        self.c = c
        self.setup()
    def setup(self):
        app = QtWidgets.QApplication(sys.argv)
        # apply_stylesheet(app, theme='default_light.xml')
        global ui
        self.guimainwindow = QtWidgets.QWidget()
        ui = GUI(self.c, self.guimainwindow, version)
        self.guimainwindow.show()
        app.exec_()
        del app
        self.c.close()
    
class Chatter:
    def recv(c, showguit):
        while True:
            app = QtWidgets.QApplication(sys.argv)
            # apply_stylesheet(app, theme='default_light.xml')
            widget = QtWidgets.QWidget()
            name = namewindow()
            name.setupUi(widget, version)
            widget.show()
            app.exec_()
            del app
            if len(username) < 4:
                continue
            break
        c.send((username + " " + version).encode("utf-8"))
        showguit.start()
        time.sleep(1)
        ui.send("GitHub 仓库地址：https://github.com/yuhaodi22222/OIChat")
        while running:
            try:
                data = c.recv(102400).decode("utf-8")
                if not data:
                    break
                if data[0:3] == "!!!":
                    tmp = data[3:].split(" ")
                    le = len(tmp)
                    if tmp[0] == "warning":
                        ui.sendwarning(data[11:])
                        continue
                    if tmp[0] == "password":
                        ui.send("请在下方输入框输入密码")
                        continue
                    if tmp[0] == "file":
                        filename = tmp[1]
                        if not os.path.exists("download"):
                            os.makedirs("download")
                        filename = os.path.basename(filename)
                        #print(filename)
                        try:
                            fileaddr = os.path.join("download", filename)
                            filesss = open(fileaddr, "wb")
                            while True:
                                filesssdata = c.recv(100)
                                #print(filesssdata)
                                if filesssdata == b"!!!endfile":
                                    break
                                filesss.write(filesssdata)
                            filesss.close()
                        except:
                            print("报错")
                        continue
                    if le == 1:
                        if tmp[0] == "kick":
                            ui.send("你被管理员踢出了服务器")
                            c.send("被管理员踢出了服务器！".encode("utf-8"))
                            flag = False
                            continue
                        if tmp[0] == "ban":
                            ui.send("你被管理员封禁了")
                            c.send("被管理员封禁！".encode("utf-8"))
                            flag = False
                            continue
                ui.send(data)
                print(data)
            except:
                break
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # apply_stylesheet(app, theme='default_light.xml')
    widget = QtWidgets.QWidget()
    ipport = ipportwindow()
    ipport.setupUi(widget, version)
    widget.show()
    app.exec_()
    del app
    ipad = (ip, port)
    addrs = socket.getaddrinfo(socket.gethostname(), None)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ipad)
        running = True
        showguit = Thread(target=showgui, args=(client, ))
        t = Thread(target=Chatter.recv, args=(client, showguit, ))
        t.start()
        t.join()
        showguit.join()
    except:
        pass
    finally:
        print("连接已被关闭")
        client.close()
        exit()
