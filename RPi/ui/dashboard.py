import gradio as gr
import ui.about_page as about_page
import ui.data_page as data_page
import ui.operating_page as operating_page
import ui.debug_page as debug_page
import ui.config_page as config_page
import RPi.GPIO as GPIO

def build_dashboard(rgb):
    with gr.Blocks() as app:
        gr.Markdown("# Self-sorting Bin")
        with gr.Tab("About"):
            about_page.build_about_page()
        with gr.Tab("Data"):
            data_page.build_data_page()
        with gr.Tab("Operating"):
            operating_page.build_operating_page()
        with gr.Tab("Debug"):
            debug_page.build_debug_page(rgb)
        with gr.Tab("Config"):
            config_page.build_config()
    return app