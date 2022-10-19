from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Processing(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(436, 46)
        Form.setStyleSheet("color: rgb(102, 102, 153);\n"
"background-color: rgb(255, 255, 255);")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 421, 41))
        self.label.setStyleSheet("font: 75 14pt \"Fixedsys\" rgb(0, 0, 255);")
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Now setting temperature, please wait...😾"))