#import machine, I2C
from machine import Pin, I2C, RTC, ADC
#import ssd1306_old as ssd1306
import ssd1306
from time import sleep

#globals that are modified by interrupts
mode = 0  # 0 == "regular mode", 1 = "set year", 2 = "set month", etc.
incPressed = False

#buttons
button_A = Pin(2, Pin.IN)
button_B = Pin(13, Pin.IN)
#button_C = Pin(2, Pin.IN)


#light sensor
lightSensor = ADC(0)

last_mode = 8


def mode_pressed_callback(pin):
    global mode
    global interrupt_pin
    interrupt_pin = pin

    sleep(0.05)  # DEBOUNCE

    #increment: will use mod to get the mode
    mode += 1
    
    
    
def inc_pressed_callback(pin):
    global interrupt_pin
    global incPressed
    interrupt_pin = pin
    sleep(0.05)
    print("pressed")
    incPressed = True
    
    

#attach interrupt to button a
button_A.irq(trigger=Pin.IRQ_RISING, handler=mode_pressed_callback)  # when there is a change

#attach interrupt to button b
button_B.irq(trigger=Pin.IRQ_RISING, handler=inc_pressed_callback)

def main():
    global mode
    global last_mode
    global incPressed
    
    
    
    haveTime = False

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

    #vars to track updated time
    yearNew = 0
    yearMax = 2020
    yearMin = 1990
    monthNew = 0

    #main loop
    while True:
        if (mode % last_mode) != 0:  # not in regular mode
            oled.text(str(mode), 100, 25)
            
            #if don't already have an updated time
            if not(haveTime):
                #get the current time and update temp vars
                cur_time = rtc.datetime()
                yearNew = cur_time[0]
                monthNew = cur_time[1]
                dayNew = cur_time[2]
                hourNew = cur_time[4]
                minuteNew = cur_time[5]
                secNew = cur_time[6]
                haveTime = True

            #update year
            if (mode % last_mode) == 1:
                #clear the screen
                oled.fill(0)
                
                #if button B is pushed
                if incPressed:
                    incPressed = False
                    yearNew += 1
                    
                    #make sure year is within bounds
                    if yearNew > yearMax:
                        yearNew = yearMin
                
                oled.text('Year: ' + str(yearNew), 0, 0)
                oled.show()
                
                
                
            # change the month
            elif (mode % last_mode) == 2:
                oled.fill(0)
                
                #if button B is pushed
                if incPressed:
                    incPressed = False
                    monthNew = monthNew % 12 + 1
                    
                oled.text('Month: ' + str(monthNew), 0, 0)
                oled.show()
            
            # change the day
            elif (mode % last_mode) == 3:
                oled.fill(0)
                
                #if button B is pushed
                if incPressed:
                    incPressed = False
                    dayNew = dayNew % 31 + 1
                    
                oled.text('Day: ' + str(dayNew), 0, 0)
                oled.show()
            
            # change the hour
            elif (mode % last_mode) == 4:
                oled.fill(0)
                
                #if button B is pushed
                if incPressed:
                    incPressed = False
                    hourNew = (hourNew + 1) % 24
                    
                oled.text('Hour: ' + str(hourNew), 0, 0)
                oled.show()
            
            # change the minute
            elif (mode % last_mode) == 5:
                oled.fill(0)
                
                #if button B is pushed
                if incPressed:
                    incPressed = False
                    minuteNew = (minuteNew + 1) % 60
                    
                oled.text('Minute: ' + str(minuteNew), 0, 0)
                oled.show()
            
            # change the sec
            elif (mode % last_mode) == 6:
                oled.fill(0)
                
                #if button B is pushed
                if incPressed:
                    incPressed = False
                    secNew = (secNew + 1) % 60
                    
                oled.text('Second: ' + str(secNew), 0, 0)
                oled.show()
            
            #else is being used as the update
            else:
                haveTime = False
                
                #update the time
                newTime = (yearNew, monthNew, dayNew, 2, hourNew, minuteNew, secNew) + cur_time[7:]
                rtc.datetime(newTime)
                
                oled.fill(0)
                oled.text('press A to', 0, 0)
                oled.text('update', 0, 10)
                oled.show()
        
        else:
            #set contrast
            oled.contrast(lightSensor.read())
            
            #get current time
            cur_time = rtc.datetime()
            year = str(cur_time[0])
            month = str(cur_time[1])
            day = str(cur_time[2])
            hour = str(cur_time[4])
            minute = str(cur_time[5])
            second = str(cur_time[6])

            #create strings for displaying time
            first_line = month + "-" + day + "-" + year
            second_line = hour + ":" + minute + ":" + second
            
            #clear previous screen and display current time
            oled.fill(0)
            oled.text(first_line, 0, 0)
            oled.text(second_line, 0, 10)

            oled.text(str(mode), 100, 25)
            oled.show()

if __name__ == "__main__" :
    main()


