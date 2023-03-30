import telnetlib
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
            password = input("Enter your password: ")
            self.tn = telnetlib.Telnet("192.168.212.220", 7171, 10)
            self.tn.read_until(b"\n")
            self.tn.write(password.encode('ascii') + b"\n")
            line = self.tn.read_until(b"End of commands")
            print(line.decode('ascii'))

        except:
            print("connection failed")
        try:
            self.thread = threading.Thread(target=self.check_query)
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

    def check_query(self):
        while True:
            time.sleep(0.5)

            sum = 0
            status = self.check_status()
            print("status : " + status)
            if "Teleop driving" in status:
                print("ready")
            elif "Going" in status:
                print("Going")
            elif "Arrived" in status:
                if "at Goal1" in status:
                    self.current_position = 1
                elif "at Goal2" in status:
                    self.current_position = 2
                elif "at Goal3" in status:
                    self.current_position = 3
                elif "at Goal4" in status:
                    self.current_position = 4

            if self.selected_position == self.current_position:
                self.update_color(self.previous_position, "red")
                self.update_color(self.selected_position, "green")
                self.previous_position = self.current_position

            print("curpos : " + str(self.current_position))

    def check_status(self):
        self.tn.write("status".encode('ascii') + b'\n')
        line = self.tn.read_until(b"Status: ")
        line = self.tn.read_until(b'\n')
        return line.decode('ascii').strip('\n')

    def button_clicked(self, n):
        if 1 <= n <= 4:
            self.selected_position = n

        if self.previous_position != self.selected_position:
            self.update_color(self.selected_position, "blue")

        print("client - goto Goal" + str(self.selected_position))
        commands_str = "goto Goal{}".format(str(self.selected_position))
        commands_encoded = commands_str.encode('ascii') + b'\n'
        self.tn.write(commands_encoded)
        line = self.tn.read_until(b'\n')
        return line.decode('ascii').strip('\n')

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