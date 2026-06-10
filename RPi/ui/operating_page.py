import gradio as gr
from hardware.network import request_sudo_poweroff

def poweroff():
    request_sudo_poweroff()

_current_image = None

def update_image(image):
    global _current_image
    _current_image = image

def _get_current_image():
    return _current_image

def build_operating_page():
    gr.Markdown("## Operating")

    with gr.Row():
        gr.Markdown("### Camera")
    with gr.Row():
        output_img = gr.Image(label="Image", streaming=False)
        
    # Timer fires every 1 second
    timer = gr.Timer(1)
    timer.tick(fn=_get_current_image, inputs=None, outputs=output_img)

    with gr.Row():
        poweroff_button = gr.Button("Poweroff")
        poweroff_button.click(fn=poweroff, outputs=None)