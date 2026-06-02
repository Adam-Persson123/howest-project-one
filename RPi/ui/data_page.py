import gradio as gr
import hardware.ultrasonic as ultrasonic
from inputs.usb_camera import get_usb_frame

sensor = ultrasonic.DistanceSensor()

def get_distance() -> str:
    return str(sensor.getDistance())

def shoot_picture():
    return get_usb_frame()

def build_data_page():
    gr.Markdown("## Data")
    with gr.Row():
        value = gr.Textbox(label="Ultrasonic value", value=get_distance())

    # Timer fires every 0.1 second
    timer = gr.Timer(0.1)
    timer.tick(fn=get_distance, inputs=None, outputs=value)

    gr.Markdown("# Raspberry Pi 5 Camera")

    with gr.Row():
        output_img = gr.Image(label="Image", streaming=False)

    timer.tick(fn=shoot_picture, outputs=output_img)
