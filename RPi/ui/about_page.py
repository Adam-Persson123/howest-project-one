import gradio as gr

def build_about_page():
    gr.Markdown("## About")

    with gr.Row():
        gr.Markdown("""
            ### What is it?
            Welcome to the Self-sorting Bin project!  
            This device consists of a Raspberry Pi and a bunch of sensors and actuators.  
            It hosts an AI model that has been trained to recognize different kinds of trash.  
            In this graphical user interface you will also find the following pages:  
            - Data: For viewing data from sensors and the AI model.
            - Operating: For controlling the device (eg. power off).
            - Debug: For debugging hardware components.
        """)

    with gr.Row():
        gr.Markdown("""
            ### How does it work?
            1. Walk up to the device (the ultrasonic sensor will detect that someone is near).
            2. Place your trash on the flat surface on the device.
            3. The device will detect what kind of trash it is.
            4. The RGB LED light will light up in a specific color, indicating where you should throw it.
        """)

    with gr.Row():
        gr.Markdown("""
            ### Trash colors:
            - Yellow = Cardboard / paper
            - Blue = Plastic packaging
            - Cyan = Plastic bottles
            - Purple = Glass
            - Green = Organic
            - Red = Metal can
            """)