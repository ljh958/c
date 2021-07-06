import threading
import uuid
import RPi.GPIO as GPIO
from time import sleep
import time
import re
import json
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.IN)

time.localtime(time.time())

RST = 24
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
width = disp.width
height = disp.height
disp.begin()
disp.clear()
disp.display()

b=0
e = 0
Fraction = 0
Mode=0

threads = []

threadLock1 = threading.Lock()
threadLock2 = threading.Lock()
threadLock2.acquire()


def main():
    thread1.start()
    thread6.start()
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)
    threads.append(thread5)
    threads.append(thread6)

def get_mac():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac


class myThread1(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        import serial
        global Mode
        while True:
            if threadLock1.acquire():
                get_mac()
            serial1 = serial.Serial('/dev/ttyACM0', 115200)
            date = '''{"flag":"Online","DeviceID":"''' + get_mac() + '''","Online":1}'''
            lon = len(date)
            if serial1.isOpen():
                print("open success")
            else:
                print("open failed")
            head = '''POST / HTTP/1.1\r\nContent-Type: application/json;charset=utf-8\r\nContent-Length: ''' + str(
                lon) + ''''\r\nHost: 39ns596068.wicp.vip\r\nConnection: Keep-Alive\r\nAccept-Encoding: gzip\r\nUser-Agent: okhttp/3.12.1\r\n\r\n'''
            send_data = head + date
            serial1.write(send_data.encode())
            data = serial1.read(1)
            sleep(0.1)
            data = (data + serial1.read(serial1.inWaiting())).decode()
            print(data)
            s = data
            data = re.search('(.\{)(.*)', s)
            ju = json.loads(data  .group())
            Mode = ju['Mode']
            time.sleep(10)
            threadLock2.release()


class myThread2(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter


    def run(self):
        global Fraction
        import serial
        while True:
            if GPIO.input(13) == 1:
                if threadLock2.acquire():
                    get_mac()
                serial1 = serial.Serial('/dev/ttyACM0', 115200)
                date = '''{"flag":"Totalscore","DeviceID":"''' + get_mac() + '''"}'''
                lot = len(date)
                head = '''POST / HTTP/1.1\r\nContent-Type: application/json;charset=utf-8\r\nContent-Length: ''' + str(
                    lot) + ''''\r\nHost: 39ns596068.wicp.vip\r\nConnection: Keep-Alive\r\nAccept-Encoding: gzip\r\nUser-Agent: okhttp/3.12.1\r\n\r\n'''
                send_data = head + date + '\r\n'
                serial1.write(send_data.encode())
                data = serial1.read(1)
                sleep(0.1)
                data = (data + serial1.read(serial1.inWaiting())).decode()
                print(data)
                s = data
                data = re.search('(\{)(.*)', s)
                ja = json.loads(data.group())
                Fraction = ja['Fraction']
                if Fraction == b:
                    GPIO.output(16, 1)
                sleep(3)
                threadLock1.release()


class myThread3(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        a = 0
        global b
        b = 1
        while True:
            if GPIO.input(13) == 1:
                GPIO.output(16, 0)
                a += 1
                if a == 60:
                    b += 1
                    a = 0
            else:
                GPIO.output(16, 1)
            time.sleep(1)


class myThread4(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global b
        d=0
        import serial
        while True:
            if GPIO.input(13) == 0:
                d+=1
            else:
                d=0
            if d==1:
                if threadLock2.acquire():
                    serial1 = serial.Serial('/dev/ttyACM0', 115200)
                datb = '''{"flag":"Fraction","Fraction":"''' + str(
                    b) + '''","DeviceID":"''' + get_mac() + '''"}'''
                lob = len(datb)
                heat = '''POST / HTTP/1.1\r\nContent-Type: application/json;charset=utf-8\r\nContent-Length: ''' + str(
                    lob) + ''''\r\nHost: 39ns596068.wicp.vip\r\nConnection: Keep-Alive\r\nAccept-Encoding: gzip\r\nUser-Agent: okhttp/3.12.1\r\n\r\n'''
                send_data = heat + datb + '\r\n'
                serial1.write(send_data.encode())
                data = serial1.read(1)
                sleep(0.1)
                data = (data + serial1.read(serial1.inWaiting())).decode()
                print(data)
                sleep(3)
                b = 0
                threadLock1.release()



class myThread5(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global b
        global Fraction
        while True:
            if GPIO.input(13) == 1:
                image1 = Image.new('1', (width, height))
                draw = ImageDraw.Draw(image1)
                font = ImageFont.truetype('/home/pi/hx711py/cxcy/fanzxt.ttf', 15)
                font2 = ImageFont.truetype('/home/pi/hx711py/cxcy/fanzxt.ttf', 15)
                draw.text((20, 18), '运行时间:' + str(b) + '分钟', font=font, fill=255)
                draw.text((20, 0), '总分:' + str(Fraction), font=font2, fill=255)
                disp.image(image1)
                disp.display()
            else:
                image = Image.new('1', (width, height))
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype('/home/pi/hx711py/cxcy/fanzxt.ttf', 13)
                font2 = ImageFont.truetype('/home/pi/hx711py/cxcy/fanzxt.ttf', 15)
                draw.text((20, 0), time.strftime('%Y-%m:%d:%S', time.localtime(time.time())), font=font2, fill=255)
                draw.text((20, 18), 'smell smell tree', font=font, fill=255)
                disp.image(image)
                disp.display()

class myThread6(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global Mode
        if threadLock2.acquire():
            print(Mode)
            if Mode==1:
                GPIO.output(16,1)
            elif Mode==0:
                thread3.start()
                thread2.start()
                thread5.start()
                thread4.start()
        threadLock1.release()



thread1 = myThread1(1, "Thread-1", 1)  # 获取在线情况
thread2 = myThread2(2, "Thread-2", 2)  # 获取总分
thread3 = myThread3(3, "Thread-3", 3)  # 计时开关继电器
thread4 = myThread4(4, "Thread-4", 4)  # 发送扣除的分数
thread5 = myThread5(5, "Thread-1", 5)
thread6 = myThread6(6, "Thread-1", 6)


if __name__ == '__main__':
    for t in threads:
        t.join()
    main()
