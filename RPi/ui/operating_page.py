import gradio as gr
from hardware.network import request_sudo_poweroff
from services.api_connect import delete_all_sessions, delete_all_detections

def poweroff():
    request_sudo_poweroff()
    gr.Info("Powering off device...")

_current_image = None

def update_image(image):
    global _current_image
    _current_image = image

def _get_current_image():
    return _current_image

def reset_data():
    delete_all_sessions()
    delete_all_detections()
    gr.Info("Sessions and detections have been reset.")

def build_operating_page():
    gr.Markdown("## Operating")

    with gr.Row():
        with gr.Column():
            with gr.Row():
                gr.Markdown("### Camera")
            with gr.Row():
                output_img = gr.Image(label="Image", streaming=False)

        with gr.Column():
            with gr.Row():
                gr.Markdown("### Sessions")

    with gr.Row():
        poweroff_button = gr.Button("Poweroff device", variant="stop")
        poweroff_button.click(fn=poweroff, outputs=None)
        reset_button = gr.Button("Reset sessions and detections", variant="stop")
        reset_button.click(fn=reset_data, outputs=None)

    # Timer fires every 1 second
    timer = gr.Timer(1)
    timer.tick(fn=_get_current_image, inputs=None, outputs=output_img)