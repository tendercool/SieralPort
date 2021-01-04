
'''

       ┌─┐       ┌─┐ + +
    ┌──┘ ┴───────┘ ┴──┐++
    │                 │
    │       ───       │++ + + +
    ███████───███████ │+
    │                 │+
    │       ─┴─       │
    │                 │
    └───┐         ┌───┘
        │         │
        │         │   + +
        │         │
        │         └──────────────┐
        │                        │
        │                        ├─┐
        │                        ┌─┘
        │                        │
        └─┐  ┐  ┌───────┬──┐  ┌──┘  + + + +
          │ ─┤ ─┤       │ ─┤ ─┤
          └──┴──┘       └──┴──┘  + + + +
                 神兽保佑
                代码无BUG!


'''



import sys
from PyQt5.QtWidgets import QMainWindow,QWidget,QLayout,QApplication,QMessageBox,QAction
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt,QTimer,QDateTime
from PyQt5.Qt import QThread,QMutex
import Sieral_UI
import config
import serial
import serial.tools.list_ports


class Worker(QThread):
    def __init__(self):
        super().__init__()
    



class Serial_MainWindow(QMainWindow,Sieral_UI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.rec_selction()
        self.send_selction()
        self.timer = QTimer()
        self.timer1 = QTimer()
        # self.time_now = time.strftime('%H:%M:%S',time.localtime())
        self.timer1.timeout.connect(self.time_now)
        self.timer.timeout.connect(self.data_send)

        self.ser = serial.Serial()
        self.port_check()

        self.thread = Worker()
        self.qmut = QMutex()

        
        con = config.Myform()
        self.comboBox_port.addItem(con.com)
        self.comboBox_baud.setCurrentText(con.baud)
        self.comboBox_databit.setCurrentText(con.databit)
        self.comboBox_polarity.setCurrentText(con.polarity)
        self.comboBox_stopbit.setCurrentText(con.stopbit)

       


        self.comboBox_baud.currentIndexChanged.connect(self.combox_baud_cb)
        self.comboBox_databit.currentIndexChanged.connect(self.combox_databit_cb)
        self.comboBox_polarity.currentIndexChanged.connect(self.combox_polarity_cb)
        self.comboBox_stopbit.currentIndexChanged.connect(self.combox_stopbit_cb)
        self.btn_send.clicked.connect(self.btn_send_cb)

        self.action_start.setEnabled(True)
        self.action_Pause.setEnabled(False)
        self.action_Stop.setEnabled(False)

        self.action_start.triggered.connect(self.action_start_cb)
        self.action_Pause.triggered.connect(self.action_Pause_cb)
        self.action_Clear.triggered.connect(self.action_Clear_cb)
        self.action_Stop.triggered.connect(self.action_Stop_cb)

        self.Infor = QAction('串口信息',self)
        self.menu_2.addAction(self.Infor)
        self.Infor.triggered.connect(self.display_cb)

    def time_now(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('hh:mm:ss')
        self.timer1.start(1000)
        return timeDisplay


    def display_cb(self):
        self.port_information()
        



    def port_information(self):
        imf_s = self.comboBox_port.currentText()
        if imf_s != '':
            # self.textBrowser.append('当前串口为：' + imf_s)
            # self.textBrowser.append('当前波特率为：' + self.comboBox_baud.currentText())
            # self.textBrowser.append('当前数字位位：' + self.comboBox_databit.currentText())
            # self.textBrowser.append('当前校验位为：' + self.comboBox_polarity.currentText())
            # self.textBrowser.append('当前停止位为：' + self.comboBox_stopbit.currentText())
            self.textBrowser.append('*****************当前串口状态********************')
            self.textBrowser.append(str(self.ser.getSettingsDict()))
            self.textBrowser.append('*****************当前串口状态********************')
        else:
            QMessageBox.information(self,'Nothing','无串口信息!')



    def port_check(self):
        self.com_dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox_port.clear()
        for port in port_list:
            self.com_dict['%s' % port[0]] = '%s' % port[1]
            self.comboBox_port.addItem(port[0])

        if len(self.com_dict) == 0:
            QMessageBox.information(self,'提示','无可用串口')



    def port_open(self):
        self.ser.port = self.comboBox_port.currentText()
        self.ser.baudrate = int(self.comboBox_baud.currentText())
        self.ser.bytesize = int(self.comboBox_databit.currentText())
        self.ser.stopbits = int(self.comboBox_stopbit.currentText())

        if self.comboBox_polarity.currentText() == '无':
            self.ser.parity = 'N'
        elif self.comboBox_polarity.currentText() == '奇校验':
            self.ser.parity = 'O'
        elif self.comboBox_polarity.currentText() == '偶校验':
            self.ser.parity = 'E'

        try:
            self.ser.open()
        except:
            QMessageBox.critical(self,'错误','该端口不能被打开！')
            return None

        if self.ser.isOpen():
            self.action_start.setEnabled(False)
            self.action_Stop.setEnabled(True)
            self.action_Pause.setEnabled(True)


        # serial.timer.start(2)



    def port_close(self):
        self.timer.stop()
        try:
            self.ser.close()
        except:
            pass
        if self.ser.isOpen() == False:
            self.action_start.setEnabled(True)
            self.action_Stop.setEnabled(False)
            self.action_Pause.setEnabled(False)
            
    def send_time(self):
        if self.checkBox_4.isChecked():
            self.timer.start(self.spinBox.value())
        else:
            self.timer.stop()
            self.data_send()
    


    def data_send(self):
        
        if self.ser.isOpen():
            input_s = self.textEdit_get.toPlainText()
            if input_s != '':
                if self.radioButton_4.isChecked():
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2],16)
                        except ValueError:
                            QMessageBox.critical(self,'wrong data','请输入16进制数据，以空格分开！')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                   
                    input_s = bytes(send_list)
                    
                else:
                    input_s = (input_s +'\r\n').encode('utf-8')

                self.ser.write(input_s)
            if self.checkBox_2.isChecked():
                    if self.checkBox_3.isChecked():
                        self.textBrowser.append('Send: ' + self.textEdit_get.toPlainText() + ' ' +self.time_now())
                    else:
                        self.textBrowser.append('Send: ' + self.textEdit_get.toPlainText())
            else:
                pass

        else:
            pass






    def data_rec(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.ser.close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            if self.radioButton_2.checkState():
                out_s = ''
                for i in range(0,num):
                    out_s = out_s + '{:02X}'.format(data[i])
                    if self.checkBox_3.isChecked():
                        self.textBrowser.append('Receive: ' + out_s + ' ' + self.time_now())
                    else:
                        self.textBrowser.append('Receive: ' + out_s)
            else:
                self.textBrowser.insertPlainText(data.decode('utf-8'))

            textCursor = self.textBrowser.textCursor()
            textCursor.movePosition(textCursor.End)
            self.textBrowser.setTextCursor(textCursor)
        else:
            pass



    def rec_selction(self):
        self.radioButton_2.setChecked(True)
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(True)



    def send_selction(self):
        self.radioButton_4.setChecked(True)
        self.checkBox_4.setChecked(False)
        self.spinBox.setRange(1000,10000)
        self.spinBox.setSingleStep(100)




        # self.statusbar.showMessage('status:ok')
        # self.comboBox_baud.currentIndexChanged.connect(self.comBox_baud_cb)
        # self.btn_send.clicked.connect(self.btn_send_cb)




    def action_start_cb(self):
        self.port_open()
        if self.ser.isOpen():
            QMessageBox.information(self,'提示','串口已连接')
       
    def action_Pause_cb(self):
        self.port_close()
        self.action_start.setEnabled(True)
        self.action_Stop.setEnabled(True)
        self.action_Pause.setEnabled(False)

        QMessageBox.information(self,'提示','停止接收')
        
    def action_Clear_cb(self):
        QMessageBox.information(self,'提示','您点击了清除按钮')
        self.textBrowser.clear()
        # self.textEdit_get.clear()

    def action_Stop_cb(self):
        self.port_close()
        
        if self.ser.isOpen() == False:
       
            QMessageBox.information(self,'提示','串口关闭')

    def combox_baud_cb(self):
        data = self.comboBox_baud.currentText()
        QMessageBox.information(self,'提示','当前选择波特率为：'+data,QMessageBox.Ok | QMessageBox.Cancel)

    def combox_databit_cb(self):
        data = self.comboBox_databit.currentText()
        QMessageBox.information(self,'提示','当前选择数据位为：'+data,QMessageBox.Ok | QMessageBox.Cancel)

    def combox_polarity_cb(self):
        data = self.comboBox_polarity.currentText()
        QMessageBox.information(self, '提示', '当前选择校验位为：' + data, QMessageBox.Ok | QMessageBox.Cancel)

    def combox_stopbit_cb(self):
        data = self.comboBox_stopbit.currentText()
        QMessageBox.information(self, '提示', '当前选择停止位为：' + data, QMessageBox.Ok | QMessageBox.Cancel)

    def btn_send_cb(self):
        # str_send = self.textEdit_get.toPlainText()
        # print(str_send)
        # self.comboBox_port.addItem('COM4')
        
        self.send_time()
        # self.data_send()
        # self.textBrowser.append(str_send)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Serial_MainWindow()
    win.show()

    sys.exit(app.exec_())