import gradio as gr
from hardware.lcd import LCD

lcd = LCD("LCD")

def send_message(text, line):
    lcd.send_string(text, line)

def set_color(r, g, b):
    pass

def build_debug_page():
    gr.Markdown("## Debug")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### LCD")
            text = gr.Textbox(label="Text")
            line = gr.Radio(label="Line", choices=[1, 2], value=1)
            button = gr.Button("Send")
            button.click(fn=send_message, inputs=[text, line], outputs=None)

        with gr.Column():
            gr.Markdown("### RGB")
            r = gr.Slider(minimum=0, maximum=255, step=1, label="R")
            g = gr.Slider(minimum=0, maximum=255, step=1, label="G")
            b = gr.Slider(minimum=0, maximum=255, step=1, label="B")
            button = gr.Button("Set")
            button.click(fn=set_color, inputs=[r, g, b], outputs=None)