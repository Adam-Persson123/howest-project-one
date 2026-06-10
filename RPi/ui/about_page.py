import gradio as gr

def build_about_page():

    with gr.Row():
        gr.Markdown(height=10)

    with gr.Row():
        with gr.Column():
            gr.Markdown("""
                ## What is it?
                Welcome to the Self-sorting Bin project!  
                This device consists of a Raspberry Pi and a bunch of sensors and actuators.  
                It hosts an AI model that has been trained to recognize different kinds of trash.  
                Show a piece of trash to the device and it will tell you where to throw it.  
                In this graphical user interface you will also find the following pages:  
                - Data: For viewing data from sensors and the AI model.
                - Operating: For controlling the device (eg. power off).
                - Debug: For debugging hardware components.
            """)
                
        with gr.Column():
            gr.Markdown("""
                ## About me
                Hi! I am Adam, a student from Sweden studying Creative Technologies and AI at Howest in Kortrijk, Belgium.

                """)        

    with gr.Row():
        gr.Markdown(height=10)

    with gr.Row():
        gr.Markdown("---")

    with gr.Row():
        gr.Markdown(height=10)

    with gr.Row():

        with gr.Column():
            gr.Markdown("## How does it work?")
            gr.Markdown("""
                <span style='font-size: 40px; vertical-align: middle; color: #22C55E'>⓵</span>
                <span style='vertical-align: middle;'> Walk up to the device (the ultrasonic sensor will detect that someone is near).</span>
                """)
            
            gr.Markdown("""
                <span style='font-size: 40px; vertical-align: middle; color: #22C55E'>⓶</span>
                <span style='vertical-align: middle;'> Place your trash on the flat surface on the device.</span>
                """)

            gr.Markdown("""
                <span style='font-size: 40px; vertical-align: middle; color: #22C55E'>⓷</span>
                <span style='vertical-align: middle;'> The device will detect what kind of trash it is.</span>
                """)

            gr.Markdown("""
                <span style='font-size: 40px; vertical-align: middle; color: #22C55E'>⓸</span>
                <span style='vertical-align: middle;'> The RGB LED light will light up in a specific color, indicating where you should throw it.</span>
                """)

        with gr.Column():
            gr.Markdown("""
                ## Trash colors:
                <span style='color: #FBBF24'>⏺</span> Yellow = Cardboard / paper  
                <span style='color: #1E90FF'>⏺</span> Blue = Plastic packaging  
                <span style='color: #00EEEE'>⏺</span> Cyan = Plastic bottles  
                <span style='color: #800080'>⏺</span> Purple = Glass  
                <span style='color: #008000'>⏺</span> Green = Organic  
                <span style='color: #FF0000'>⏺</span> Red = Metal can  
                """)