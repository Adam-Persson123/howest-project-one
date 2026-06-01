import RPi.GPIO as GPIO
from hardware.lcd import LCD
from hardware.ultrasonic import DistanceSensor
from inputs.usb_camera import get_usb_frame
from time import sleep
from ultralytics import YOLO

ds = DistanceSensor()
lcd = LCD("LCD")
model = YOLO("../ai/best.pt")

def standby(rgb):
    rgb.set_color(0, 0, 0)
    lcd.send_string(" ", 1)
    lcd.send_string(" ", 2)

def active(rgb):
    rgb.set_color(255, 255, 255)
    lcd.send_string("Welcome!", 1)
    lcd.send_string("Distance: " + str(ds.getDistance()), 2)

    frame = get_usb_frame()
    if frame is not None:
        results = model(frame)
        for result in results:
            classes = result.names
            for c in classes:
                lcd.send_string(c, 1)

        

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