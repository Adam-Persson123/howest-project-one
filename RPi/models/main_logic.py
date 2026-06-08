import RPi.GPIO as GPIO
from hardware.lcd import LCD
from hardware.ultrasonic import DistanceSensor
from inputs.usb_camera import get_usb_frame
from time import sleep
from ultralytics import YOLO
from datetime import datetime
from services.api_connect import create_new_session, create_new_detection
from hardware.network import wait_for_host_interface_ips

ds = DistanceSensor()
lcd = LCD("LCD")
model = YOLO("ai/best.pt")

session_start = None

def standby(rgb):
    rgb.set_color(0, 0, 0)

    lcd.send_string(wait_for_host_interface_ips()[0], 1)
    lcd.send_string(wait_for_host_interface_ips()[1], 2)

    if session_start is not None:
        session_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_new_session(session_start, session_end)

def welcome(rgb):
    rgb.set_color(255, 255, 255)
    lcd.send_string("Welcome!", 1)
    lcd.send_string("Ready for trash", 2)

    global session_start
    session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

                color = None
                match cls:
                    case 0:
                        rgb.set_color(255, 0, 0)
                        color = "Red"
                    case 1:
                        rgb.set_color(0, 255, 0)
                        color = "Green"
                    case 2:
                        rgb.set_color(0, 0, 255)
                        color = "Blue"
                    case 3:
                        rgb.set_color(255, 255, 0)
                        color = "Yellow"
                    case 4:
                        rgb.set_color(255, 0, 255)
                        color = "Purple"
                    case 5:
                        rgb.set_color(0, 255, 255)
                        color = "Cyan"

                class_name = model.names[int(cls)]
                lcd.send_string(f"{class_name}", 1)
                lcd.send_string(f"{color} bin", 2)

                create_new_detection(int(cls) + 1, int(conf * 100), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                sleep(1)
    

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