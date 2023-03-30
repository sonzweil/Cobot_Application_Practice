import telnetlib


def check_query(self):
    o1 = self.sendARCLcommands("outputQuery o1")
    if "o1 on" in o1:
        print("o1 on")

    o2 = self.sendARCLcommands("outputQuery o2")

    if "o2 on" in o2:
        print("o2 on")

def sendARCLcommands(self, commands):
    commands_encoded = commands.encode('ascii') + b"\n"
    self.tn.write(commands_encoded)
    line = self.tn.read_until(b'\n')
    return line.decode('ascii').strip('\n')

def gotoGoal(self, pos):
    print("client - goto Goal" + str(pos))
    commands_str = "goto Goal{}".format(str(pos))
    self.sendARCLcommands(commands_str)


if __name__ == '__main__':
    try:
        password = input("Enter your password: ")
        tn = telnetlib.Telnet("192.168.212.220", 7171, 10)
        tn.read_until(b"\n")
        tn.write(password.encode('ascii') + b"\n")
        line = tn.read_until(b"End of commands")
        print(line.decode('ascii'))
        tn.read_until(b'\n')
    except:
        print("connection failed")

