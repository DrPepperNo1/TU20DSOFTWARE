from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QMessageBox,QGraphicsView,QGraphicsScene
from UI_version1 import Ui_MainWindow
from UI_ProcessingNotification import Ui_Processing
from UI_Succeed import Ui_Succeed
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.Qt import QThread
from PyQt5.QtGui import QPixmap, QImage
from UI_Fail import Ui_Fail
import sys
import cv2
import serial
import datetime
import time
import re

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui=Ui_MainWindow()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面
        self.ProcessingWindow = ProcessingWindow()
        self.SucceedWindow = SucceedWindow()
        self.FailWindow = FailWindow()
        self.timer_delay = QTimer()

        self.scene = QGraphicsScene()  # 创建画布
        self.ui.graphicsView_avatar.setScene(self.scene)  # 把画布添加到窗口
        self.ui.graphicsView_avatar.show()
        self.Setimage()

        self.ser = serial.Serial('COM3', 9600, timeout=1)  # connecting to COM3
        self.TimerforReadingT()    # Timer initialization

        self.ui.pushButton_SetT.clicked.connect(self.SetT)
        self.ui.pushButton_instruction.clicked.connect(self.Sendinstruction)
    def Setimage(self):
        self.scene.clear()  # 先清空上次的残留
        self.pix = QPixmap(r'icon\icons8-chicken.png')
        #self.pix = QPixmap.fromImage(frame)
        self.scene.addPixmap(self.pix)

    def TimerforReadingT(self):# Timer initialization
        self.timer_measure = QTimer()
        self.thread5 = thread_readT(self.timer_measure,self.ser)
        self.thread5.signal_readT.connect(self.TextBrowserPrintT)
        self.thread5.setTerminationEnabled(True)
    def TextBrowserPrintT(self,currentT):    #Getting temperature and display
        if currentT == 'clear':
            self.ui.textBrowser.clear()
        else:
            self.ui.textBrowser.append('%s--------%s' % (currentT[2:],str(datetime.datetime.strftime(datetime.datetime.now(),'%m-%d %H:%M:%S'))))
    def SetT(self): #Setting Temperature Control Function
        self.thread5.terminate()
        self.timer_measure.stop()
        self.ui.pushButton_SetT.setEnabled(False)
        self.ui.pushButton_instruction.setEnabled(False)
        self.input_t = self.ui.lineEdit_InputT.text()
        rejudge = re.match("[+-][0-9][0-9][0-9][0-9][.][0-9][0-9]", self.input_t)
        if rejudge:
            self.thread1 = thread_processingwindow(self.ProcessingWindow)  # Thread1: display inprocessing window
            self.thread1.setTerminationEnabled(True)
            self.thread2 = thread_reallysettingT(self.input_t,self.ser)  # Thread2: really setting T
            self.thread2.start()
            self.thread2.signal_closeTh1_en.connect(self.kill_thread1)
        else:
            QMessageBox.critical(self, "Sorry",
                                 "The format of T you input seems wrong:(")  # 最后的Yes表示弹框的按钮显示为Yes，默认按钮显示为OK,不填QMessageBox.Yes即为默认
            self.ui.pushButton_SetT.setEnabled(True)
            self.ui.pushButton_instruction.setEnabled(True)
            self.thread5 = thread_readT(self.timer_measure, self.ser)
            self.thread5.signal_readT.connect(self.TextBrowserPrintT)
            self.thread5.setTerminationEnabled(True)
        '''
        self.ui.pushButton_SetT.setEnabled(True)
        self.ui.pushButton_instruction.setEnabled(True)
        self.thread5 = thread_readT(self.timer_measure,self.ser)
        self.timer_measure.start(3000)
        '''
    def Sendinstruction(self):
        self.thread5.terminate()
        self.timer_measure.stop()
        self.ui.pushButton_instruction.setEnabled(False)
        self.ui.pushButton_SetT.setEnabled(False)
        self.input_ins = self.ui.lineEdit_instruction.text()
        self.ui.textBrowser_2.setText(self.RS232communication(self.input_ins))
        self.ui.pushButton_instruction.setEnabled(True)
        self.ui.pushButton_SetT.setEnabled(True)
        self.thread5 = thread_readT(self.timer_measure, self.ser)
        self.thread5.signal_readT.connect(self.TextBrowserPrintT)
        self.thread5.setTerminationEnabled(True)
    def RS232communication(self, instruction):  #Sending Str to Hearter%
        var = instruction;
        self.ser.write(var.encode())  # str to bitstream
        data_from_Heater = self.ser.read(64)
        # 获取指令的返回值，并且进行类型转换，转换为字符串后便可以进行字符串对比，因而便可以根据返回值进行判断是否执行特定功能
        data_from_Heater = str(data_from_Heater, encoding="utf-8")
        return data_from_Heater
    '''
    def start_measure(self):
        self.timer_measure.start(20)
        self.ui.start_measure.setEnabled(False)
        self.ui.stop_measure.setEnabled(True)

    def stop_measure(self):
        self.timer_measure.stop()
        self.ui.start_measure.setEnabled(True)
        self.ui.stop_measure.setEnabled(False)
    '''
    def kill_thread1(self, judge):
        print(judge)
        self.thread1.stop()  # close processing window
        if(judge == 'succeed2set'):
            self.thread3 = thread_succeedwindow(self.SucceedWindow, self.input_t,self.timer_delay)
            self.thread3.setTerminationEnabled(True)
        if (judge == 'fail2set'):
            self.thread4 = thread_failwindow(self.FailWindow, self.timer_delay)
            self.thread4.setTerminationEnabled(True)
        self.ui.pushButton_SetT.setEnabled(True)
        self.ui.pushButton_instruction.setEnabled(True)
        self.thread5 = thread_readT(self.timer_measure, self.ser)
        self.thread5.signal_readT.connect(self.TextBrowserPrintT)
        self.thread5.setTerminationEnabled(True)
        #self.timer_measure.start(3000)
        #self.ui.pushButton_SetT.setEnabled(True)
class ProcessingWindow(QMainWindow): #子窗口构造类1
    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui=Ui_Processing()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面

class SucceedWindow(QMainWindow): #子窗口构造类2
    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui=Ui_Succeed()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面

class FailWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui=Ui_Fail()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面

class thread_processingwindow(QThread):  #线程函数1在这里📌
    def __init__(self,ProcessingWindow):
        super(thread_processingwindow,self).__init__()
        self.ProcessingWindow = ProcessingWindow
        self.ProcessingWindow.show()

    def stop(self):
        self.ProcessingWindow.close()
        self.terminate()

class thread_reallysettingT(QThread): #线程函数2在这里📌 Setting-T Control Thread
    signal_closeTh1_en = pyqtSignal(str)
    def __init__(self,input_t,ser):
        super(thread_reallysettingT,self).__init__()#线程一定要有构造函数！📌
        self.ser = ser
        self.input_t = input_t
        self.countfail = 0
    def run(self):
        if 'S' + self.input_t != self.RS232communication('S'+self.input_t):
            self.signal_closeTh1_en.emit('fail2set')  # 设置失败
        elif '\r\nError\r\n' == self.RS232communication('S'):
            self.signal_closeTh1_en.emit('succeed2set')# 设置成功
        else:
            self.signal_closeTh1_en.emit('fail2set')# 设置成功# 设置失败
    def RS232communication(self, instruction):  #Sending Str to Hearter
        var = instruction;
        self.ser.write(var.encode())  # str to bitstream
        data_from_Heater = self.ser.read(64)
        # 获取指令的返回值，并且进行类型转换，转换为字符串后便可以进行字符串对比，因而便可以根据返回值进行判断是否执行特定功能
        data_from_Heater = str(data_from_Heater, encoding="utf-8")
        return data_from_Heater
class thread_succeedwindow(QThread):  #线程函数3在这里📌
    def __init__(self, SucceedWindow, input_t, timer_delay):
        super(thread_succeedwindow,self).__init__()
        self.SucceedWindow = SucceedWindow
        self.SucceedWindow.ui.textBrowser.setText(input_t+'℃')
        self.SucceedWindow.show()
        self.timer_delay = timer_delay
        self.timer_delay.start(1000) #Successfully set window
        self.timer_delay.timeout.connect(self.stop)
    def stop(self):
        self.timer_delay.stop()
        self.SucceedWindow.close()
        self.terminate()
class thread_failwindow(QThread):  #线程函数4在这里📌
    def __init__(self, FailWindow, timer_delay):
        super(thread_failwindow,self).__init__()
        self.FailWindow = FailWindow
        self.FailWindow.show()
        self.timer_delay = timer_delay
        self.timer_delay.start(1000) #Fail to set window
        self.timer_delay.timeout.connect(self.stop)
    def stop(self):
        self.timer_delay.stop()
        self.FailWindow.close()
        self.terminate()
class thread_readT(QThread):  #线程函数5在这里📌
    signal_readT = pyqtSignal(str)
    def __init__(self, timer_measure, ser):
        super(thread_readT,self).__init__()
        self.counter = 0
        self.timer_measure = timer_measure
        self.ser = ser
        self.timer_measure.start(3000)
        self.timer_measure.timeout.connect(self.printt)
    def printt(self):
        self.counter = self.counter + 1
        if self.counter >= 12:
            self.signal_readT.emit('clear')
            self.counter = 0
        else:
            self.signal_readT.emit(self.RS232communication('T'))
    def RS232communication(self, instruction):  #Sending Str to Hearter
        var = instruction
        self.ser.write(var.encode())  # str to bitstream
        data_from_Heater = self.ser.read(64)
        # 获取指令的返回值，并且进行类型转换，转换为字符串后便可以进行字符串对比，因而便可以根据返回值进行判断是否执行特定功能
        data_from_Heater = str(data_from_Heater, encoding="utf-8")
        return data_from_Heater
if __name__ == '__main__':
    '''
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)  # connecting to COM3
    except:
        print('Seems No Communication...')
        print('① Please ensure your computer is connected to the Heater via RS-232')
        print('② Start the software')
        sys.exit()
    del ser
    '''
    app = QApplication(sys.argv)
    mainwindow = MyWindow()
    mainwindow.show()
    ProcessingWindow()
    sys.exit(app.exec_())

'''
‘T’: Temperature
'D': Device
'W': W
'E': E
'''