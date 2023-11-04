import socket
import time
import os
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
#from qt_material import apply_stylesheet
import sys
import gui
running = False
opname = ""
flag = True
ip = "127.0.0.1"
port = 10000
username = ""
codemd = False
version = "2.0.5"  # 版本号

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
        ui = gui.GUI(self.c, self.guimainwindow, version)
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
