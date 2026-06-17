import gradio as gr
from services.bin_manager import get_color_for_class


cardboard_color = get_color_for_class("Cardboard")
organic_color = get_color_for_class("Organic")
plastic_color = get_color_for_class("Plastic packaging")
metal_color = get_color_for_class("Metal can")
glass_color = get_color_for_class("Glass jar")
plastic_bottle_color = get_color_for_class("Plastic bottle")

def update_colors():
    cardboard_color = get_color_for_class("Cardboard")
    organic_color = get_color_for_class("Organic")
    plastic_color = get_color_for_class("Plastic packaging")
    metal_color = get_color_for_class("Metal can")
    glass_color = get_color_for_class("Glass jar")
    plastic_bottle_color = get_color_for_class("Plastic bottle")

    return gr.update(value=f"""
        ## Trash colors:
        <span style='color: {cardboard_color}'>⏺</span> Cardboard / paper  
        <span style='color: {organic_color}'>⏺</span> Organic  
        <span style='color: {plastic_color}'>⏺</span> Plastic packaging  
        <span style='color: {metal_color}'>⏺</span> Metal can  
        <span style='color: {glass_color}'>⏺</span> Glass jar  
        <span style='color: {plastic_bottle_color}'>⏺</span> Plastic bottle
    """)

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
                <div style='overflow: hidden; height: 60px'>
                    <span style='font-size: 40px; vertical-align: middle; color: #22C55E;'>⓵</span>
                    <span style='vertical-align: middle;'> Walk up to the device (the ultrasonic sensor will detect that someone is near).</span>
                </div>
                """)
            
            gr.Markdown("""
                <div style='overflow: hidden; height: 60px'>
                    <span style='font-size: 40px; vertical-align: middle; color: #22C55E'>⓶</span>
                    <span style='vertical-align: middle;'> Place your trash on the flat surface on the device.</span>
                </div>
                """)

            gr.Markdown("""
                <div style='overflow: hidden; height: 60px'>
                    <span style='font-size: 40px; vertical-align: middle; color: #22C55E'>⓷</span>
                    <span style='vertical-align: middle;'> The device will detect what kind of trash it is.</span>
                </div>
                """)

            gr.Markdown("""
                <div style='overflow: hidden; height: 60px'>
                    <span style='font-size: 40px; vertical-align: middle; color: #22C55E'>⓸</span>
                    <span style='vertical-align: middle;'> The RGB LED light will light up in a specific color, indicating where you should throw it.</span>
                </div>
                """)

        with gr.Column():
            trash_colors = gr.Markdown(f"""
                ## Trash colors:
                <span style='color: {cardboard_color}'>⏺</span> Cardboard / paper  
                <span style='color: {organic_color}'>⏺</span> Organic  
                <span style='color: {plastic_color}'>⏺</span> Plastic packaging  
                <span style='color: {metal_color}'>⏺</span> Metal can  
                <span style='color: {glass_color}'>⏺</span> Glass jar  
                <span style='color: {plastic_bottle_color}'>⏺</span> Plastic bottle
                """)

        timer = gr.Timer(2)
        timer.tick(fn=update_colors, inputs=[], outputs=[trash_colors])