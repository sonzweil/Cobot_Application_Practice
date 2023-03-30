
# #방식1
# import time
# from pymodbus.client import ModbusTcpClient
# client = ModbusTcpClient(host='192.168.123.14', port=502)
#
# a = 1
# while True:
#     client.write_register(129, a)
#     a += 1
#     time.sleep(1)

# #방식2
import time
from pyModbusTCP.client import ModbusClient
c = ModbusClient(host='192.168.123.7', port=502)

a = 1
while True:
    c.write_single_register(129, a)
    a += 1
    time.sleep(1)
