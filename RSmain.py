import serial

# 把字符串类型转换为bytes数据流进行发送，RS232命令发送函数
def serial_sent_utf(command):
    # 从字典里获取对应的RS232命令
    var = command
    # encode()函数是编码，把字符串数据转换成bytes数据流
    ser.write(var.encode())
    #var = bytes.fromhex(RS232_Command["%s" % command])
    #ser.write(var)
    data = ser.read(64)
    # 获取指令的返回值，并且进行类型转换，转换为字符串后便可以进行字符串对比，因而便可以根据返回值进行判断是否执行特定功能
    data = str(data, encoding="utf-8")
    return data


if __name__ == '__main__':
    # 实现串口的连接
    ser = serial.Serial('COM3', 9600, timeout=1)
    command1_utf8 = serial_sent_utf('S')
    print(command1_utf8)
'''
‘T’: Temperature
'D': Device
'W': W interrupt
'E': E
'S,O': Set
'''

