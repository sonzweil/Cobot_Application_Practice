import telnetlib
import threading
import time
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

class URDash(QDialog):
    def __init__(self):
        self.previous_position = -1
        self.current_position = 0
        self.selected_position = 0

        try:
            password = input("Enter your password: ")
            self.tn = telnetlib.Telnet("192.168.212.220", 7171, 10)
            self.tn.read_until(b"\n")
            self.tn.write(password.encode('ascii') + b"\n")
            line = self.tn.read_until(b"End of commands")
            print(line.decode('ascii'))
            self.tn.read_until(b'\n')
        except:
            print("connection failed")


        self.check_query()

        QDialog.__init__(self)
        self.ui = uic.loadUi('URDash.ui', self)
        for i in range(1,5):
            self.update_color(i, "red")

        self.Button1.clicked.connect(lambda: self.button_clicked(1))
        self.Button2.clicked.connect(lambda: self.button_clicked(2))
        self.Button3.clicked.connect(lambda: self.button_clicked(3))
        self.Button4.clicked.connect(lambda: self.button_clicked(4))

    def check_query(self):
        o1 = self.sendARCLcommands("outputQuery o1")
        if "o1 on" in o1:
            print("o1 on")

        o2 = self.sendARCLcommands("outputQuery o2")

        if "o2 on" in o2:
            print("o2 on")


    def checkCurPos(self, commands_str):
        print("client - send" + str(commands_str))
        if self.selected_position == self.current_position:
            self.update_color(self.previous_position, "red")
            self.update_color(self.selected_position, "green")
            self.previous_position = self.current_position

    def sendARCLcommands(self, commands):
        commands_encoded = commands.encode('ascii') + b"\n"
        self.tn.write(commands_encoded)
        line = self.tn.read_until(b'\n')
        return line.decode('ascii').strip('\n')

    def gotoGoal(self, pos):
        print("client - goto Goal" + str(pos))
        commands_str = "goto Goal{}".format(str(pos))
        self.sendARCLcommands(commands_str)

    # def getRegister(self, n):
    #     while True:
    #         results = self.client.read_holding_registers(n, 1)
    #         self.current_position = results.registers[0]
    #
    #         if self.selected_position == self.current_position:
    #             self.update_color(self.previous_position, "red")
    #             self.update_color(self.selected_position, "green")
    #             self.previous_position = self.current_position
    #
    #         time.sleep(0.05)

    def button_clicked(self, n):
        if 1 <= n <= 4:
            self.selected_position = n
        self.gotoGoal(self.selected_position)


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