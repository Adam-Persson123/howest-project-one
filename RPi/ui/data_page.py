import gradio as gr
import hardware.ultrasonic as ultrasonic

def build_data_page():
    gr.Markdown(
        """
        ### Data
        """
    )

def ultrasonic_value():
    return ultrasonic.getDistance