import sys
from PyQt5.QtWidgets import QMainWindow,QWidget,QLayout,QApplication,QMessageBox
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt,QSettings
import Sieral_UI


class Myform(QMainWindow):
	def __init__(self):
		super().__init__()
		# self.setupUi(self)

		self.settings = QSettings('config.ini',QSettings.IniFormat)
		self.com = self.settings.value('SETUP/COM_VALUE')
		self.baud = self.settings.value('SETUP/BAUD_VALUE')
		self.databit = self.settings.value('SETUP/DATABIT_VALUE')
		self.polarity = self.settings.value('SETUP/POLARITY_VALUE')
		self.stopbit = self.settings.value('SETUP/STOPBIT_VALUE')

		if self.polarity == 'Odd':
			self.polarity = '奇校验'
		elif self.polarity == 'Even':
			self.polarity = '偶校验'
		elif self.polarity == 'None':
			self.polarity = '无'

	# 	self.comboBox_port.addItem(self.com)
	# 	self.comboBox_baud.setCurrentText(self.baud)
	# 	self.comboBox_databit.setCurrentText(self.databit)
	# 	self.comboBox_polarity.setCurrentText(self.polarity)
	# 	self.comboBox_stopbit.setCurrentText(self.stopbit)

	# 	self.statusbar.showMessage('status:ok')
	# 	self.comboBox_baud.currentIndexChanged.connect(self.comBox_baud_cb)
	# 	self.btn_send.clicked.connect(self.btn_send_cb)

	# def comBox_baud_cb(self):
	# 	self.baud = self.comboBox_baud.currentText()

	# def btn_send_cb(self):
	# 	self.settings.setValue('SETUP/BAUD_VALUE',self.baud)
	# 	QMessageBox.information(self,'提示','QSettings保存成功')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Myform()
    w1.show()
    app.exec_()