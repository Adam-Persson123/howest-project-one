import gradio as gr
from services.api_connect import get_latest_detection, fetch_detection_data, fetch_class_data, load_sessions
import pandas as pd
import plotly.express as px

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
    
    return counts

def get_bar_plot():
    counts = get_number_of_detections()
    if counts is None:
        return None
    return px.bar(counts, x="Class", y="Detections")

def get_pie_plot():
    counts = get_number_of_detections()
    if counts is None:
        return None
    return px.pie(counts, values="Detections", names="Class")

def get_number_of_sessions():
    df = load_sessions()
    if df is None or df.empty:
        return None
    return len(df)

def build_data_page():
    gr.Markdown("## Data")

    with gr.Row():
        with gr.Column():
            latest_detection = gr.DataFrame(label="Latest AI detection")
        with gr.Column():
            number_of_sessions = gr.Textbox(label="Number of sessions", value=get_number_of_sessions(), interactive=False)

    with gr.Row():
        with gr.Column():
            detections_plot = gr.Plot(label="Detections per Class")
                    
        with gr.Column():
            detections_pie = gr.Plot(label="Detections per Class")

    with gr.Row():
        refresh_btn = gr.Button("Refresh")
        refresh_btn.click(fn=get_bar_plot, inputs=None, outputs=detections_plot)
        refresh_btn.click(fn=get_pie_plot, inputs=None, outputs=detections_pie)
        
    # Timer fires every 1 second
    timer = gr.Timer(1)
    timer.tick(fn=get_detection, outputs=latest_detection)