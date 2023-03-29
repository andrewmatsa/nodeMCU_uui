# esptool --port COM5 -c esp8266 --baud 115200 write_flash --flash_size=detect -fm dout 0 esp8266-20220618-v1.19.1.bin

# list of files:
# import os
# os.listdir()

import machine
from machine import Pin, PWM
from time import sleep
import dht
import usocket as socket
import network

def do_connect():
    print('-- Connecting to network')
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Andre Archer Connect', '1234567890abb')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def webpage():
    file = open("data/index.html", "r")
    page = file.read().format(temp='goodbye')
    file.close()
    return page

class Main:
    first_header = 'World!'

def webserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    temp = str(measure_temp())
    while True:
        conn, addre = s.accept()
        request = conn.recv(1024)
        request = str(request)
        if "GET /?temp=on" in request:
            temp = 0
        temp_status = ("ON")[temp==0]
        print(request)
        # get_data = request.find('/')
        # a = str(measure_temp().get('temp'))
        # print(f'mesured {a}')
        # print(webpage())
        response = webpage()

        # response = webpage() % measure_temp().get('temp')

        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-type: text/html\n")

        conn.send("Connection: close\n\n")

        conn.sendall(response)

        conn.close()

def led():
    led = machine.Pin(2, machine.Pin.OUT)
    led.on()
    sleep(0.1)
    led.off()
    sleep(0.1)


def measure_temp():
    # D7
    sensor = dht.DHT11(Pin(13))
    try:
        sensor.measure()
    except OSError:
        print('got error sleep 3 sec')
        sleep(3)
        sensor.measure()
    print(f"TEMPER: {sensor.temperature()} C")
    print(f"HUMIDITY: {sensor.humidity()} %")
    return {"temp": sensor.temperature(), "hum": sensor.humidity()}


if __name__ == '__main__':
    do_connect()
    for i in range(5):
        led()
    # measure_temp()
    try:
        do_connect()
        webserver()
    except OSError:
        print('os error')
        do_connect()
        webserver()
