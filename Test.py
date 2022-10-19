# # -*- encoding: utf-8 -*-
#
import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import time

currentTime = time.strftime("%H:%M %p")  # 当前时间(时：分 AM/PM)


class Toast(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('toast')
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)  # 去掉标题栏
        self.setStyleSheet("background-color:#3A4659;\n")
        self.gridLayout_3 = QtWidgets.QGridLayout(self)
        self.gridLayout_3.setContentsMargins(0, 0, 0,
                                             0)  # 布局，frame布局在gridLayout_3里，gridLayout_3在窗体里，与窗体的四周的距离为（0，0，0，0）
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.frame = QtWidgets.QFrame(self)
        # self.frame.setStyleSheet("background-color:#3A4659;\n" )
        self.frame.setObjectName("frame")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.passLabel = QtWidgets.QLabel(self.frame)
        self.passLabel.setMinimumSize(QtCore.QSize(41, 41))
        self.passLabel.setMaximumSize(QtCore.QSize(41, 41))
        # 显示图片（对/错）的文本框，由调用此py文件传入需显示的图片
        # self.passLabel.setPixmap(QtGui.QPixmap("images/pass.png"))
        self.passLabel.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.passLabel)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        # 消息通知的文本框
        self.alertsLabel = QtWidgets.QLabel(self.frame)
        self.alertsLabel.setMinimumSize(QtCore.QSize(200, 0))  # 设置文本框最小尺寸
        self.alertsLabel.setStyleSheet("font: 20px\"微软雅黑\";color:white")
        self.alertsLabel.setText("消息通知")
        self.alertsLabel.setObjectName("label")
        self.gridLayout.addWidget(self.alertsLabel, 0, 0, 1, 1)
        # 显示时间的文本框
        self.timeLabel = QtWidgets.QLabel(self.frame)
        self.timeLabel.setStyleSheet("font: 15px\"微软雅黑\";color:white")
        self.timeLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.timeLabel.setText(currentTime)  # 将“currentTime”即当前时间，显示在文本框内
        self.timeLabel.setObjectName("label_3")
        self.gridLayout.addWidget(self.timeLabel, 0, 1, 1, 1)
        # 显示消息内容的文本框，由调用此py文件传入需显示的消息内容
        self.toastLabel = QtWidgets.QLabel(self.frame)
        self.toastLabel.setStyleSheet("font: 15px\"微软雅黑\";color:white")
        #self.toastLabel.setText("保存成功")
        self.toastLabel.setObjectName("label")
        self.gridLayout.addWidget(self.toastLabel, 1, 0, 1, 1)

        self.horizontalLayout.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)


class WinForm(QWidget):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.setGeometry(300, 300, 350, 350)  # 确定窗口位置大小
        self.resize(350, 350)
        self.setWindowTitle('点击按钮开启弹窗')  # 设置窗口标题
        quit = QPushButton('开启弹窗', self)  # button 对象
        quit.setGeometry(10, 10, 100, 35)  # 设置按钮的位置 和 大小
        quit.setStyleSheet("background-color: red")  # 设置按钮的风格和颜色
        quit.clicked.connect(self.toast)

    def toast(self):
        self.ui = Toast()
        self.ui.show()
        QtCore.QTimer().singleShot(2000, self.ui.close)
        self.ui.toastLabel.setText('保存成功')
        self.ui.passLabel.setPixmap(QtGui.QPixmap("images/pass.png"))
        screen = QDesktopWidget().screenGeometry()
        size = self.ui.geometry()
        self.ui.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WinForm()  # 实体化 类
    win.show()
    sys.exit(app.exec_())
