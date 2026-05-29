import RPi.GPIO as GPIO
from hardware.lcd import LCD
from hardware.ultrasonic import DistanceSensor
from time import sleep

ds = DistanceSensor()
lcd = LCD("LCD")

def standby(rgb):
    rgb.set_color(0, 0, 0)
    lcd.send_string(" ", 1)
    lcd.send_string(" ", 2)

def active(rgb):
    rgb.set_color(255, 255, 255)
    lcd.send_string("Welcome!", 1)
    lcd.send_string("Distance: " + str(ds.getDistance()), 2)

def main_loop(rgb):

    cooldown = 0

    standby_flag = False

    try:
        while True:

            distance = ds.getDistance()

            if distance is None:
                distance = 1000

            if distance > 50:
                if cooldown > 0:
                    cooldown = cooldown - 1
                if cooldown == 0:
                    if standby_flag == False:
                        standby_flag = True
                        standby(rgb)
            else:
                cooldown = 5
                standby_flag = False
                active(rgb)

            sleep(1)

    except Exception as e:
        print(f"Main loop error: {e}")
    finally:
        GPIO.cleanup()