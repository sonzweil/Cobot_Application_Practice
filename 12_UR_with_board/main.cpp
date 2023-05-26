/* Sockets Example
 * Copyright (c) 2016-2020 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "mbed.h"
#include "wifi_helper.h"
#include <cstdint>

InterruptIn Echo(PA_0);
Timer timer;
Ticker ticker;
PwmOut Trig(PA_1);
uint8_t echo_flag = 0;
uint8_t sec_flag = 0;

void funcA(void) // rising
{
    timer.reset();
    timer.start();
}
void funcB(void) // falling
{
    timer.stop();
    echo_flag = 1;
}
void funcC(void) // Period 3sec
{
    sec_flag = 1;
}

class ModbusDemo {
    static constexpr size_t MAX_NUMBER_OF_ACCESS_POINTS = 10;

public:
    ModbusDemo()  : _net(NetworkInterface::get_default_instance())
    {
        
    }

    ~ModbusDemo()
    {
        if (_net) {
            _net->disconnect();
        }
    }

    void wifi_connection()
    {
        if (!_net) {
            printf("Error! No network interface found.\r\n");
            return;
        }

        /* if we're using a wifi interface run a quick scan */
        if (_net->wifiInterface()) {
            /* the scan is not required to connect and only serves to show visible access points */
            wifi_scan();

            /* in this example we use credentials configured at compile time which are used by
             * NetworkInterface::connect() but it's possible to do this at runtime by using the
             * WiFiInterface::connect() which takes these parameters as arguments */
        }

        /* connect will perform the action appropriate to the interface type to connect to the network */

        printf("Connecting to the network...\r\n");

        nsapi_size_or_error_t result = _net->connect();
        if (result != 0) {
            printf("Error! _net->connect() returned: %d\r\n", result);
            return;
        }

        print_network_info();

        result = _socket.open(_net);
        if (result != 0) {
            printf("Error! _socket.open() returned: %d\r\n", result);
            return;
        }  

        _a.set_ip_address("192.168.213.80");
        _a.set_port(502); //Modbus Socket Port      
        _socket.connect(_a);

    }


    uint8_t modbus_single_read(uint16_t address)
    {
       unsigned char recv_data[1024] = {0x00, };
       nsapi_size_t recv_length = 0;
       // unsigned char Tr = 0;  // Transaction ID
       // unsigned char Pr = 0; // Protocol ID
       // unsigned char Le = 6;  // Length
       // unsigned char ID = 1;  // Unit ID
       // unsigned char Code = 0x03;  //03 read, Read Holding Register
       // unsigned char Addr = 0;  // Satrting Address
       // unsigned char Data = 1;     //read Data #
       unsigned char buffer[12] = {00,01,00,00,00,06,01,03,00,00,00,01};
       buffer[0] = _seq_num;
       buffer[8] = (address >> 8) & 0xff;
       buffer[9] = address & 0xff;

       int scount = _socket.send(buffer, sizeof buffer);
       recv_length = _socket.recv(recv_data, 1024);

       printf("R[%04d]:",address);
       for(int i=0; i < recv_length; i++)
       {
           printf("%02x",recv_data[i]);
       }
       printf("\n\r"); 

       _seq_num++; 

       return 0;      

    }

    void modbus_single_write(uint16_t address,  uint16_t data)
    {
       unsigned char recv_data[1024] = {0x00, };
       nsapi_size_t recv_length = 0;        
       // unsigned char Tr = 0;  // Transaction ID
       // unsigned char Pr = 0; // Protocol ID
       // unsigned char Le = 6;  // Length
       // unsigned char ID = 1;  // Unit ID
       // unsigned char Code = 0x06;  //06 Write, Write Holding Register
       // unsigned char Addr = 0;  // Satrting Address
       // unsigned char Data = 25;     //read Data #

       unsigned char buffer[12] = {00,02,00,00,00,06,01,06,00,00,00,19};
       buffer[0] = _seq_num;            
       buffer[8] = (address >> 8) & 0xff;
       buffer[9] = address & 0xff;
       buffer[10] = (data >> 8) & 0xff;  
       buffer[11] = data & 0xff;  

       int scount = _socket.send(buffer, sizeof buffer);
       recv_length = _socket.recv(recv_data, 1024);

       printf("W[%04d]:",address);
       for(int i=0; i < recv_length; i++)
       {
           printf("%02x",recv_data[i]);
       }
       printf("\n\r");   

       _seq_num++; 
    }    

private:
    void wifi_scan()
    {
        WiFiInterface *wifi = _net->wifiInterface();

        WiFiAccessPoint ap[MAX_NUMBER_OF_ACCESS_POINTS];

        /* scan call returns number of access points found */
        int result = wifi->scan(ap, MAX_NUMBER_OF_ACCESS_POINTS);

        if (result <= 0) {
            printf("WiFiInterface::scan() failed with return value: %d\r\n", result);
            return;
        }

        printf("%d networks available:\r\n", result);

        for (int i = 0; i < result; i++) {
            printf("Network: %s secured: %s BSSID: %hhX:%hhX:%hhX:%hhx:%hhx:%hhx RSSI: %hhd Ch: %hhd\r\n",
                   ap[i].get_ssid(), get_security_string(ap[i].get_security()),
                   ap[i].get_bssid()[0], ap[i].get_bssid()[1], ap[i].get_bssid()[2],
                   ap[i].get_bssid()[3], ap[i].get_bssid()[4], ap[i].get_bssid()[5],
                   ap[i].get_rssi(), ap[i].get_channel());
        }
        printf("\r\n");
    }

    void print_network_info()
    {
        /* print the network info */
        SocketAddress a;
        _net->get_ip_address(&a);
        printf("IP address: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
        _net->get_netmask(&a);
        printf("Netmask: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
        _net->get_gateway(&a);
        printf("Gateway: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
    }

private:
    NetworkInterface *_net;
    TCPSocket _socket;
    SocketAddress _a;
    uint8_t _seq_num = 0;
};

int main() {
    uint8_t count = 0;
    

    printf("\r\nStarting socket Wifi Test\r\n\r\n");

    ModbusDemo *example = new ModbusDemo();
    MBED_ASSERT(example);
    example->wifi_connection();

    Trig.period_ms(200); 
    Trig.pulsewidth_us(20); 
    Echo.rise(funcA);
    Echo.fall(funcB);
    ticker.attach_us(&funcC, 1000000);


    while(1){
        if(echo_flag == 1){
            uint16_t distance = 0;  
            distance = (timer.read_us() / 58) * 10; 
            example->modbus_single_read(129);
            example->modbus_single_write(130,distance);
            printf("Distanced : %d\n\r", distance);
            count++;
            echo_flag = 0;
        }
    }
    return 0;
}
