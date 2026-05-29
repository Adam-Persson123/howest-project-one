import gradio as gr
from hardware.lcd import LCD

lcd = LCD("LCD")
rgb = None

def send_message(text, line):
    lcd.send_string(text, line)

def set_color(r, g, b):
    rgb.set_color(r, g, b)

def build_debug_page(led):
    global rgb
    rgb = led
    gr.Markdown("## Debug")

    with gr.Row():
        with gr.Column():
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