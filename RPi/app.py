import gradio as gr
import RPi.GPIO as GPIO
from ui.dashboard import build_dashboard
from models.main_logic import main_loop
from hardware.rgb import RGB
import threading

rgb = RGB()

if __name__ == "__main__":
    worker = threading.Thread(target=main_loop, args=(rgb,), daemon=True)
    worker.start()  # Starting main loop in its own thread

    app = build_dashboard(rgb)

    try:
        app.launch(server_name="0.0.0.0", server_port=7860, show_error=True, theme=gr.themes.Soft(primary_hue="green", font=[gr.themes.GoogleFont("Inter")], text_size="lg"))
    finally:
        GPIO.cleanup()