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

    if mode == last_mode:
        mode = 0
    else:  # if pushed is False or mode != 2
        mode += 1


button_A.irq(trigger=Pin.IRQ_RISING, handler=callback)  # when there is a change

def main():
    # ESP8266 Pin assignment
    i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

    oled_width = 128
    oled_height = 32

    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    oled.fill(0)

    rtc = RTC()
    initial_time = (2014, 5, 1, 4, 13, 0, 0, 0)
    rtc.datetime(initial_time)  #initial_time) #year, month, day

    while True:
        cur_time = rtc.datetime()
        year = str(cur_time[0])
        month = str(cur_time[1])
        day = str(cur_time[2])
        hour = str(cur_time[4])
        minute = str(cur_time[5])
        second = str(cur_time[6])

        first_line = month + " " + day + ", " + year
        second_line = hour + ":" + minute + ":" + second
        oled.text(first_line, 0, 0)
        oled.text(second_line, 0, 10)
        oled.show()
        oled.fill(0)

        oled.text(str(mode), 100, 25)
        oled.show()

        while mode != 0:  # not in regular mode
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






    # rtc = urtc.PCF8523(i2c)


    # d = RTC().datetime()
    # del RTC
    # res = "{}-{}-{} {}:{}:{}".format(str(d[0])[2 :], d[1], d[2], d[4], d[5], d[6])
    # oled.text(res, 0, 0)
    # oled.show()



    # rtc = machine.RTC()
    # default_time = (2019, 9, 28, 4, 28)
    # rtc.init(default_time)
    # rtc.init((2014, 5, 1, 4, 13, 0, 0, 0))
    # oled.text(rtc.now(), 0, 0)
    # datetime = rtc.datetime()
    # print(datetime)
    # # oled.fill(0)
    # hour = datetime.hour
    # ampm = "AM"
    # if (hour > 12) :
    #     hour = hour - 12
    #     if (hour == 0) :
    #         hour = 12
    #     ampm = "PM"
    # oled.text(("%d:%02d:%02d " + ampm) % (hour, datetime.minute, datetime.second), 30, 0)
    # oled.text("%d/%d/%d" % (datetime.month, datetime.day, datetime.year), 30, 8)
    # oled.text('MicroPython Time', 0, 24)
    # oled.show()


if __name__ == "__main__" :
    main()