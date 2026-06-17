import gradio as gr
from hardware.network import request_sudo_poweroff
from services.api_connect import delete_all_sessions, delete_all_detections

def poweroff():
    request_sudo_poweroff()
    gr.Info("Powering off device...")

_current_image = None

def reset_data():
    delete_all_sessions()
    delete_all_detections()
    gr.Info("Sessions and detections have been reset.")

def build_admin_page():
    gr.Markdown("## Admin")
    poweroff_button = gr.Button("Poweroff device", variant="stop")
    poweroff_button.click(fn=poweroff, outputs=None)
    reset_button = gr.Button("Reset sessions and detections", variant="stop")
    reset_button.click(fn=reset_data, outputs=None)
