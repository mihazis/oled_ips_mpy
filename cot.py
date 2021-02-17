import time
import machine
import network
import utime
import ntptime
import wifi
import st7789
import ftext
import uos
import random

from ssd1309 import Display
from xglcd_font import XglcdFont

DISPLAY_WIDTH = const(128)
#wi-fi decloration
wifissid1 = 'Tomato24'
wifipassword1 = '77777777'
wifissid2 = ''
wifipassword2 = ''
tcounter = 0
formatted_time = "0"

#display decloration
spi = machine.SPI(
    2,
    baudrate=30000000,
    polarity=1,
    phase=1,
    sck=machine.Pin(18),
    mosi=machine.Pin(19))
display = st7789.ST7789(
    spi, 135, 240,
    reset=machine.Pin(23, machine.Pin.OUT),
    cs=machine.Pin(5, machine.Pin.OUT),
    dc=machine.Pin(16, machine.Pin.OUT))
display.init()
spi2 = machine.SPI(1, baudrate=10000000, sck=machine.Pin(27), mosi=machine.Pin(21))
oled = Display(spi2, dc=machine.Pin(13), cs=machine.Pin(26), rst=machine.Pin(22))
fonts = ["astrol.fnt", "cyrilc.fnt", "gotheng.fnt", "greeks.fnt",
         "italicc.fnt", "italiccs.fnt", "meteo.fnt", "music.fnt",
         "romanc.fnt", "romancs.fnt", "romand.fnt", "romanp.fnt",
         "romans.fnt", "romant.fnt", "scriptc.fnt", "scripts.fnt"]
perfect_big = XglcdFont('PerfectPixel_23x32.c', 23, 32)
perfect_small = XglcdFont('PerfectPixel_18x25.c', 18, 25)
# turn on the backlight on IPS
p = machine.Pin(4, machine.Pin.OUT)
p.value(1)

utc_shift = 3

def sync_time():        #пробуем синхронизировать время
    try:
        ntptime.settime()
        time.sleep(1)
    except Exception as ex:
        time.sleep(15)
    else:
        time.sleep(1)
    finally:
        time.sleep(1)
    
    tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    rtc.datetime(tm)

def log(logs):
    print(logs)
    time.sleep(1)
def tcb(timer):         #функция, выполняющаяся по коллбэку таймера
    update_oled()
    
def display_name_max(name, x, y):
    """Display name on LCD and maximize font size."

    Args:
        name (string):  name to display on LCD
        x, y (int): coordinates to draw text
    """
    if perfect_big.measure_text(name) < DISPLAY_WIDTH:
        oled.draw_text(x, y, name, perfect_big)
    else:
        oled.draw_text(x, y, name, perfect_small)
        
        
def get_time():
    tim = rtc.datetime()
    year = str(tim[0])
    mon0 = str(tim[1])
    day0 = str(tim[2])
    hour0 = str(tim[4])
    min0 = str(tim[5])
    if int(hour0) < 10: #добавляем ноль, если меньше 10
        hour1 = str("0" + hour0)
    else:
        hour1 = hour0

    if int(min0) < 10: #добавляем ноль, если меньше 10
        min1 = str("0" + min0)
    else:
        min1 = min0
    return str(hour1 + ":" + min1)    


def update_oled():      #выводим информацию на экран 1306 с обновлением часов
    oled.clear()
    print(get_time())
    oled.draw_text(15, 15, get_time(), perfect_big)
    oled.present()
    time.sleep(1)
    

#===================основное тело скрипта============================
'''ip = str(connect(wifissid1, wifipassword1))
if ip == '127.0.0.1':
    log('test')
    ip = str(connect(wifissid2, wifipassword2))
    log('test2')

display.fill(st7789.BLACK)
rtc = machine.RTC()

oled.clear()
oled.draw_text8x8(0, 0, "Please wait,")
oled.draw_text8x8(0, 16, "Loading fonts...")
oled.present()
perfect_big = XglcdFont('PerfectPixel_23x32.c', 23, 32)
perfect_small = XglcdFont('PerfectPixel_18x25.c', 18, 25)
oled.clear()
display_name_max('21:59', 20, 20)
oled.present()


startTime = time.ticks_ms()

ntptime.settime()
print(rtc.datetime())
#display_name_max(rtc.datetime(), 20, 20)
oled.present()

update_oled()
'''

#===================основное тело скрипта2============================

display.fill(st7789.BLACK)
ip = str(wifi.connect(wifissid1, wifipassword1)) # тут получим ip, если в офисе
if ip == '127.0.0.1':
    ip = str(connect(wifissid2, wifipassword2)) # или тут, если дома

oled.draw_text8x8(0, 0, ip)
oled.present()

rtc = machine.RTC()
sync_time()

t1 = machine.Timer(2)
t1.init(period=1000, mode=t1.PERIODIC, callback=tcb)
