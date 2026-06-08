import gradio as gr
import hardware.ultrasonic as ultrasonic
from services.api_connect import get_latest_detection, fetch_detection_data, fetch_class_data
import pandas as pd
import plotly.express as px

sensor = ultrasonic.DistanceSensor()

def get_distance() -> str:
    return str(sensor.getDistance())

def get_detection():
    result = get_latest_detection()
    if result is None:
        return pd.DataFrame()
    return pd.DataFrame([result])

def get_number_of_detections():
    df = fetch_detection_data()
    if df is None or df.empty:
        return None
    
    class_df = fetch_class_data()
    if class_df is None or class_df.empty:
        return None

    counts = df.groupby("class_id").size().reset_index(name="Detections")
    counts = counts.merge(class_df[["id", "name"]], left_on="class_id", right_on="id")
    counts = counts[["name", "Detections"]]
    counts.columns = ["Class", "Detections"]
    
    fig = px.bar(counts, x="Class", y="Detections")
    return fig

def build_data_page():
    gr.Markdown("## Data")
    with gr.Row():
        value = gr.Textbox(label="Ultrasonic value", value=get_distance())
        latest_detection = gr.DataFrame(label="Latest AI detection")

    with gr.Row():
        with gr.Column():
            detections_plot = gr.Plot(label="Detections per Class")
            refresh_btn = gr.Button("Refresh")
            refresh_btn.click(fn=get_number_of_detections, inputs=None, outputs=detections_plot)
                    
        with gr.Column():
            pass
        
    # Timer fires every 1 second
    timer = gr.Timer(1)
    timer.tick(fn=get_distance, inputs=None, outputs=value)
    timer.tick(fn=get_detection, outputs=latest_detection)