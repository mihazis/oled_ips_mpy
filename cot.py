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
from machine import Pin
from ssd1309 import Display
from xglcd_font import XglcdFont

DISPLAY_WIDTH = const(128)
#wi-fi decloration
wifissid1 = 'Tomato24'
wifipassword1 = '77777777'
wifissid2 = ''
wifipassword2 = ''

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

spi2 = machine.SPI(1, baudrate=10000000, sck=Pin(27), mosi=Pin(21))
oled = Display(spi2, dc=Pin(13), cs=Pin(26), rst=Pin(22))


fonts = ["astrol.fnt", "cyrilc.fnt", "gotheng.fnt", "greeks.fnt",
         "italicc.fnt", "italiccs.fnt", "meteo.fnt", "music.fnt",
         "romanc.fnt", "romancs.fnt", "romand.fnt", "romanp.fnt",
         "romans.fnt", "romant.fnt", "scriptc.fnt", "scripts.fnt"]

def disconnect():
    station = network.WLAN(network.STA_IF)
    if station.active():
        station.disconnect()
        station.active(False)
        oled.text('disconnected!', 0, 30)
        time.sleep(1)
        oled.fill(0)
        time.sleep(1)
def log(logs):
    print(logs)
    time.sleep(1)
def connect(ssid, password):
    log('connect start')
    station = network.WLAN(network.STA_IF) 
 
    if not station.active():
        station.active(True) 
  
    if station.isconnected():
        tuple1 = station.ifconfig()
        ipold = tuple1[0]
        return ipold
  
    try:
        station.connect(ssid, password)
        time.sleep(3)
        while station.isconnected() == False:
            if time.ticks_diff(time.ticks_ms(), startTime) > 15000:
                log("raise")
                raise PasswordError('Неверный пароль')
            log(str(time.ticks_diff(time.ticks_ms(), startTime)))
            #time.sleep_ms(1000)
        tuple1 = station.ifconfig()
        ipold = tuple1[0]
        return ipold
          
    except PasswordError:
        time.sleep_ms(1000)
        return '127.0.0.1' 
p = Pin(4, Pin.OUT)
p.value(1)

ip = str(connect(wifissid1, wifipassword1))
if ip == '127.0.0.1':
    log('test')
    ip = str(connect(wifissid2, wifipassword2))
    log('test2')

display.fill(st7789.BLACK)
'''font_file = "/fonts/romanc.fnt"
font_file2 = "/fonts/romancs.fnt"
font_file3 = "/fonts/scripts.fnt"
color1 = st7789.color565(250,0,0)
color2 = st7789.color565(250,250,0)
color3 = st7789.color565(0,255,255)
#ftext.text(display, font_file, "AAAAAAA", 0, 0, color1)
#ftext.text(display, font_file, "Radio", 50, 5, color1)
#ftext.text(display, font_file2, ip, 80, 50, color3)
#ftext.text(display, font_file2, "Volume:0-255", 120, 20, color2)
#ftext.text(display, font_file2, "stream:", 160, 50, color3)
#ftext.text(display, font_file3, "Nashe Radio", 190, 20, color3)'''
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

oled.clear()
oled.draw_text8x8(0, 0, "Please wait,")
oled.draw_text8x8(0, 16, "Loading fonts...")
oled.present()
perfect_big = XglcdFont('PerfectPixel_23x32.c', 23, 32)
perfect_small = XglcdFont('PerfectPixel_18x25.c', 18, 25)
oled.clear()
display_name_max('21:59', 20, 20)
oled.present()