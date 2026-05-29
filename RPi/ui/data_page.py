import gradio as gr
import hardware.ultrasonic as ultrasonic

sensor = ultrasonic.DistanceSensor()

def get_distance() -> str:
    return str(sensor.getDistance())

def build_data_page():
    gr.Markdown("## Data")
    with gr.Row():
        value = gr.Textbox(label="Ultrasonic value", value=get_distance())

    # Timer fires every 1 second, calls get_distance, pushes result into `value`
    timer = gr.Timer(1)
    timer.tick(fn=get_distance, inputs=None, outputs=value)