from pymodbus.client import ModbusTcpClient
import threading
import time
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

class URDash(QDialog):
    def __init__(self):
        self.previous_position = 1
        self.current_position = 1
        self.selected_position = 0

        try:
            self.client = ModbusTcpClient('192.168.213.80')
        except:
            print("connection failed")

        try:
            self.thread = threading.Thread(target=self.getRegister, args=(255, ))
            self.thread.start()
        except:
            print("thread failed")

        QDialog.__init__(self)
        self.ui = uic.loadUi('URDash.ui', self)
        self.update_color(1, "green")
        self.update_color(2, "red")
        self.update_color(3, "red")
        self.update_color(4, "red")

        self.Button1.clicked.connect(lambda: self.button_clicked(1))
        self.Button2.clicked.connect(lambda: self.button_clicked(2))
        self.Button3.clicked.connect(lambda: self.button_clicked(3))
        self.Button4.clicked.connect(lambda: self.button_clicked(4))

    def getRegister(self, n):
        while True:
            results = self.client.read_holding_registers(n, 1)
            self.current_position = results.registers[0]

            if self.selected_position == self.current_position:
                self.update_color(self.previous_position, "red")
                self.update_color(self.selected_position, "green")
                self.previous_position = self.current_position

            time.sleep(0.05)

    def button_clicked(self, n):
        if n == 1:
            self.selected_position = 1
        elif n == 2:
            self.selected_position = 2
        elif n == 3:
            self.selected_position = 3
        elif n == 4:
            self.selected_position = 4

        self.client.write_register(129, self.selected_position)

        if self.previous_position != self.selected_position:
            self.update_color(self.selected_position, "blue")

    def update_color(self, selected_position, color):
        if selected_position == 1:
            self.P1.setStyleSheet("QCheckBox::indicator{background-color : "+ color + ";}")
        elif selected_position == 2:
            self.P2.setStyleSheet("QCheckBox::indicator{background-color : "+ color + ";}")
        elif selected_position == 3:
            self.P3.setStyleSheet("QCheckBox::indicator{background-color : "+ color + ";}")
        elif selected_position == 4:
            self.P4.setStyleSheet("QCheckBox::indicator{background-color : "+ color + ";}")


if __name__ == '__main__':
    app = QApplication([])
    URDash().show()
    sys.exit(app.exec_())