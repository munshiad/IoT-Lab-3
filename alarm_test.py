#import machine, I2C
from machine import Pin, I2C, RTC, ADC
#import ssd1306_old as ssd1306
import ssd1306
from time import sleep

#alarm reached
def alarmReached(alarmTime, curTime):
    if curTime[2] >= alarmTime[2] and curTime[4] >= alarmTime[4] \
    and curTime[5] >= alarmTime[5] and curTime[6] >= alarmTime[6]:
        return True
    
    
alarm_ringing = False

# ESP8266 Pin assignment
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

#setup oled
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)


#set rtc
rtc = RTC()
initial_time = (2014, 5, 1, 4, 12, 0, 0, 0)
rtc.datetime(initial_time)  #initial_time) #year, month, day
alarmTime = (2014, 5, 1, 2, 12, 0, 5, 0)


while True:
    if alarmReached(alarmTime, rtc.datetime()):
        oled.fill(1)
        oled.show()
