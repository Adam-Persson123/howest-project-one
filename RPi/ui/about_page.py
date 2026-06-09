import gradio as gr

def build_about_page():
    gr.Markdown("## About")

    with gr.Row():
        with gr.Column():
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

        with gr.Column():
            gr.Markdown("### How does it work?")
            with gr.Walkthrough(selected=1) as walkthrough:
                with gr.Step("Step 1", id=1):
                    gr.Markdown("Walk up to the device (the ultrasonic sensor will detect that someone is near).")
                    with gr.Row():
                        with gr.Column():
                            btn_prev_1 = gr.Button("Previous")
                        with gr.Column():
                            btn_next_1 = gr.Button("Next")
                            btn_next_1.click(lambda: gr.Walkthrough(selected=2), outputs=walkthrough)

                with gr.Step("Step 2", id=2):
                    gr.Markdown("Place your trash on the flat surface on the device.")
                    with gr.Row():
                        with gr.Column():
                            btn_prev_2 = gr.Button("Previous")
                            btn_prev_2.click(lambda: gr.Walkthrough(selected=1), outputs=walkthrough)
                        with gr.Column():
                            btn_next_2 = gr.Button("Next")
                            btn_next_2.click(lambda: gr.Walkthrough(selected=3), outputs=walkthrough)

                with gr.Step("Step 3", id=3):
                    gr.Markdown("The device will detect what kind of trash it is.")
                    with gr.Row():
                        with gr.Column():
                            btn_prev_3 = gr.Button("Previous")
                            btn_prev_3.click(lambda: gr.Walkthrough(selected=2), outputs=walkthrough)
                        with gr.Column():
                            btn_next_3 = gr.Button("Next")
                            btn_next_3.click(lambda: gr.Walkthrough(selected=4), outputs=walkthrough)

                with gr.Step("Step 4", id=4):
                    gr.Markdown("The RGB LED light will light up in a specific color, indicating where you should throw it.")
                    with gr.Row():
                        with gr.Column():
                            btn_prev_4 = gr.Button("Previous")
                            btn_prev_4.click(lambda: gr.Walkthrough(selected=3), outputs=walkthrough)
                        with gr.Column():
                            pass
                
            gr.Markdown("# Test")
            gr.Textbox(show_label=False, interactive=False, value="Test")
                



    with gr.Row():
        with gr.Column():
            gr.Markdown("""
                ### Trash colors:
                - Yellow = Cardboard / paper
                - Blue = Plastic packaging
                - Cyan = Plastic bottles
                - Purple = Glass
                - Green = Organic
                - Red = Metal can
                """)

        with gr.Column():
            gr.Markdown("""
                ### About me
                Hi! I am Adam, a student from Sweden studying Creative Technologies and AI at Howest in Kortrijk, Belgium.

                """)