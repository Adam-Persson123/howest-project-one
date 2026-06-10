import gradio as gr
from hardware.lcd import LCD
import pandas as pd
from services.api_connect import load_logs
from inputs.usb_camera import get_usb_frame
import hardware.ultrasonic as ultrasonic

sensor = ultrasonic.DistanceSensor()
lcd = LCD("LCD")
rgb = None

def get_distance() -> str:
    return str(sensor.getDistance())

def send_message(text, line):
    lcd.send_string(text, line)

def set_color(r, g, b):
    rgb.set_color(r, g, b)

def get_logs():
    return load_logs()

def shoot_picture():
    return get_usb_frame()

def build_debug_page(led):
    global rgb
    rgb = led
    gr.Markdown("## Debug")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Distance Sensor")
            value = gr.Textbox(label="Ultrasonic value", value=get_distance())
            gr.Markdown("### LCD")
            text = gr.Textbox(label="Text")
            line = gr.Radio(label="Line", choices=[1, 2], value=1)
            button = gr.Button("Send to LCD Display")
            button.click(fn=send_message, inputs=[text, line], outputs=None)

        with gr.Column():
            gr.Markdown("### RGB")
            r = gr.Slider(minimum=0, maximum=255, step=1, label="R")
            g = gr.Slider(minimum=0, maximum=255, step=1, label="G")
            b = gr.Slider(minimum=0, maximum=255, step=1, label="B")
            button = gr.Button("Set color of RGB LED")
            button.click(fn=set_color, inputs=[r, g, b], outputs=None)

    with gr.Row():
        with gr.Column():
            refresh_btn = gr.Button("Refresh Logs")
            logs = gr.DataFrame(label="Logs")
            refresh_btn.click(fn=get_logs, inputs=None, outputs=logs)

        with gr.Column():
            gr.Markdown("### Camera")

            # Timer fires every 0.1 second
            timer = gr.Timer(0.1)
            gr.Markdown("# Raspberry Pi 5 Camera")
            output_img = gr.Image(label="Image", streaming=False)
            timer.tick(fn=shoot_picture, outputs=output_img)
            timer.tick(fn=get_distance, inputs=None, outputs=value)
