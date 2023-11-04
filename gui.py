from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet

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

