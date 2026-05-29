import gradio as gr
import ui.about_page as about_page
import ui.data_page as data_page
import ui.operating_page as operating_page
import ui.debug_page as debug_page

import RPi.GPIO as GPIO
from time import sleep

"""RPi UI Dashboard — entry point."""

with gr.Blocks() as app:
    gr.Markdown(
        "# Self-sorting Bin"
    )
    with gr.Tab("About"):
        about_page.build_about_page()
    with gr.Tab("Data"):
        data_page.build_data_page()
    with gr.Tab("Operating"):
        operating_page.build_operating_page()
    with gr.Tab("Debug"):
        debug_page.build_debug_page()

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft(primary_hue="green"))

try:
    while True:
        pass

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

