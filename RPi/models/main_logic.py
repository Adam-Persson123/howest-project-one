import RPi.GPIO as GPIO
from hardware.lcd import LCD
from hardware.ultrasonic import DistanceSensor
from inputs.usb_camera import get_usb_frame
from time import sleep
from ultralytics import YOLO
from datetime import datetime
from services.api_connect import create_new_session, create_new_detection, create_new_log
from hardware.network import wait_for_host_interface_ips
from ui.operating_page import update_image
from services.bin_manager import get_color_for_class, get_bin_for_class
import cv2

ds = DistanceSensor()
lcd = LCD("LCD")
model = YOLO("ai/best.pt")

session_start = None

COOLDOWN = 2
DISTANCE = 50
UPDATE_INTERVAL = 0.1
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def hex_color_to_rgb(color):
    return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

def standby(rgb):
    rgb.set_color(0, 0, 0)

    lcd.send_string(wait_for_host_interface_ips()[0], 1)
    lcd.send_string(wait_for_host_interface_ips()[1], 2)

    create_new_log("info", "Standby", datetime.now().strftime(TIME_FORMAT))

    if session_start is not None:
        session_end = datetime.now().strftime(TIME_FORMAT)
        create_new_session(session_start, session_end)

def welcome(rgb):
    rgb.set_color(255, 255, 255)
    lcd.send_string("Welcome!", 1)
    lcd.send_string("Ready for trash", 2)

    create_new_log("info", "Ready", datetime.now().strftime(TIME_FORMAT))

    global session_start
    session_start = datetime.now().strftime(TIME_FORMAT)

def active(rgb):

    frame = get_usb_frame()
    if frame is not None:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        results = model(frame_bgr)
        result = None
        if results is not None:
            result = results[0]

        # Send image to gradio
        annotated = result.plot()
        annotated_rgb = annotated[:, :, ::-1]
        update_image(annotated_rgb)

        boxes = result.boxes  # Bounding box outputs
        for box in boxes:
            conf = box.conf[0]            # Confidence score
            cls = box.cls[0]              # Class ID

            class_name = model.names[int(cls)]

            bin_name = get_bin_for_class(class_name)
            bin_name = bin_name.capitalize()
            color = get_color_for_class(class_name)

            lcd.send_string(f"{class_name}", 1)
            lcd.send_string(f"{bin_name}", 2)

            rgb_color = hex_color_to_rgb(color)
            rgb.set_color(rgb_color[0], rgb_color[1], rgb_color[2])

            create_new_detection(int(cls) + 1, int(conf * 100), datetime.now().strftime(TIME_FORMAT))

            # if there are more than one object detected, wait
            if len(boxes) > 1:
                sleep(0.5)
                print("More than one object detected. Waiting 0.5 seconds before next update...")
    

def main_loop(rgb):

    cooldown = 0

    standby_flag = False
    welcome_flag = False

    last_distance = 1000

    try:
        while True:

            distance = ds.getDistance()

            if distance is None:
                distance = 1000

            if distance > DISTANCE:
                if cooldown > 0:
                    cooldown = cooldown - 1
                if cooldown == 0:
                    if standby_flag == False:
                        standby_flag = True
                        welcome_flag = False
                        standby(rgb)
            else:
                if last_distance < DISTANCE:
                    cooldown = COOLDOWN / UPDATE_INTERVAL
                    standby_flag = False

                    if welcome_flag == False:
                        welcome(rgb)
                        welcome_flag = True

            if cooldown != 0:
                active(rgb)

            last_distance = distance

            sleep(UPDATE_INTERVAL)


    except Exception as e:
        print(f"Main loop error: {e}")
        create_new_log("error", f"Main loop error: {e}", datetime.now().strftime(TIME_FORMAT))
    finally:
        GPIO.cleanup()