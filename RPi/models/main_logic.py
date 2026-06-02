import RPi.GPIO as GPIO
from hardware.lcd import LCD
from hardware.ultrasonic import DistanceSensor
from inputs.usb_camera import get_usb_frame
from time import sleep
from ultralytics import YOLO
from datetime import datetime

ds = DistanceSensor()
lcd = LCD("LCD")
model = YOLO("ai/best.pt")

session_start = None

def standby(rgb):
    rgb.set_color(0, 0, 0)
    lcd.send_string(" ", 1)
    lcd.send_string(" ", 2)

    if session_start is not None:
        session_end = datetime.now()
        # send to backend

def welcome(rgb):
    rgb.set_color(255, 255, 255)
    lcd.send_string("Welcome!", 1)
    lcd.send_string("Ready for trash", 2)

    global session_start
    session_start = datetime.now()

def active(rgb):

    frame = get_usb_frame()
    if frame is not None:
        results = model(frame)
        for result in results:
            boxes = result.boxes  # Bounding box outputs
            for box in boxes:
                # x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coordinates
                conf = box.conf[0]            # Confidence score
                cls = box.cls[0]              # Class ID
                class_name = model.names[int(cls)]
                lcd.send_string(f"Class: {class_name}", 1)
                lcd.send_string(f"Confidence: {conf}", 2)
                # print(f"Class: {cls}, Confidence: {conf}")
                match cls:
                    case 0:
                        rgb.set_color(255, 0, 0)
                    case 1:
                        rgb.set_color(0, 255, 0)
                    case 2:
                        rgb.set_color(0, 0, 255)
                    case 3:
                        rgb.set_color(255, 255, 255)
                    case 4:
                        rgb.set_color(255, 0, 255)
                    case 5:
                        rgb.set_color(0, 255, 255)

                # Send to backend

def main_loop(rgb):

    cooldown = 0

    standby_flag = False
    welcome_flag = False

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
                        welcome_flag = False
                        standby(rgb)
            else:
                cooldown = 5
                standby_flag = False

                if welcome_flag == False:
                    welcome(rgb)
                    welcome_flag = True

            if cooldown != 0:
                active(rgb)

            sleep(1)

    except Exception as e:
        print(f"Main loop error: {e}")
    finally:
        GPIO.cleanup()