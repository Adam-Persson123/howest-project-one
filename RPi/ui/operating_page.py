import gradio as gr

_current_image = None

def update_image(image):
    global _current_image
    _current_image = image

def _get_current_image():
    return _current_image

def build_operating_page():
    gr.Markdown("## Operating")

    with gr.Row():
        with gr.Column():
            with gr.Row():
                output_img = gr.Image(label="Camera", streaming=False)

    # Timer fires every 1 second
    timer = gr.Timer(1)
    timer.tick(fn=_get_current_image, inputs=None, outputs=output_img)