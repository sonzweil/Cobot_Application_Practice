from pymodbus.client import ModbusTcpClient
import threading
import time
import sys



if __name__ == '__main__':
    client = ModbusTcpClient('192.168.213.80')
    while True:
        pos_dx = input("input posdx range 0 to 65535\n")
        pos_dy = input("input posdy range 0 to 65535\n")
        pos_dz = input("input posdz range 0 to 65535\n")

        client.write_register(128, int(pos_dx))
        client.write_register(129, int(pos_dy))
        client.write_register(130, int(pos_dz))