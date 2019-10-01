# import machine, I2C
from machine import Pin, I2C, RTC
# import ssd1306_old as ssd1306
import ssd1306
from time import sleep

mode = 0  # 0 == "regular mode", 1 = "set year", 2 = "set month", etc.

button_A = Pin(0, Pin.IN)
button_B = Pin(16, Pin.IN)
button_C = Pin(2, Pin.IN)

last_mode = 3


def callback(pin):
    global mode

    global interrupt_pin
    interrupt_pin = pin

    sleep(0.05)  # DEBOUNCE

    #increment: will use mod to get the mode
    mode += 1

#attach interrupt to button a
button_A.irq(trigger=Pin.IRQ_RISING, handler=callback)  # when there is a change

def main():
    # ESP8266 Pin assignment
    i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

    #setup oled
    oled_width = 128
    oled_height = 32
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)

    #set rtc
    rtc = RTC()
    initial_time = (2014, 5, 1, 4, 13, 0, 0, 0)
    rtc.datetime(initial_time)  #initial_time) #year, month, day

    #main loop
    while True:
        if (mode % last_mode) != 0:  # not in regular mode
            # oled.text(str(mode), 100, 25)
            #
            # if mode == 1:  # change the year
            #     oled.fill(0)
            #     oled.text('Year: ' + year, 0, 0)
            #     oled.show()
            # elif mode == 2:  # change the month
            #     oled.fill(0)
            #     oled.text('Month: ' + month, 0, 0)
            #     oled.show()
            # else:
            #     oled.fill(1)
            #     oled.show()
            oled.fill(1)
            oled.show()
        
        else:
            #get current time
            cur_time = rtc.datetime()
            year = str(cur_time[0])
            month = str(cur_time[1])
            day = str(cur_time[2])
            hour = str(cur_time[4])
            minute = str(cur_time[5])
            second = str(cur_time[6])

            #create strings for displaying time
            first_line = month + " " + day + ", " + year
            second_line = hour + ":" + minute + ":" + second
            
            #clear previous screen and display current time
            oled.fill(0)
            oled.text(first_line, 0, 0)
            oled.text(second_line, 0, 10)

            oled.text(str(mode), 100, 25)
            oled.show()

if __name__ == "__main__" :
    main()


