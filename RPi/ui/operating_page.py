import gradio as gr
from hardware.network import request_sudo_poweroff

def poweroff():
    request_sudo_poweroff()

def build_operating_page():
    gr.Markdown("## Operating")

    poweroff_button = gr.Button("Poweroff")
    poweroff_button.click(fn=poweroff, outputs=None)