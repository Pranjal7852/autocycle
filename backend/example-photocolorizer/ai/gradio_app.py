import gradio as gr
import cv2
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import numpy as np
from gradio_imageslider import ImageSlider
import os


img_colorization = pipeline(Tasks.image_colorization, model='iic/cv_ddcolor_image-colorization')

def color(image):
    # Run colorization model
    output = img_colorization(image[...,::-1])
    result = output[OutputKeys.OUTPUT_IMG].astype(np.uint8)

    # You can choose not to save the image here

    print('Inference finished!')
    return (image, result)

title = "old_photo_restoration"
description = "Colorize old black and white photos."
examples = [[os.path.join('assets', 'tajmahal.jpeg'),], [os.path.join('assets', 'oldhouse.jpeg')]]

# Set up Gradio interface
demo = gr.Interface(
    fn=color,
    inputs="image",
    outputs=ImageSlider(position=0.5, label='Colored image with slider-view'),
    examples=examples,
    title=title,
    description=description,
    allow_flagging="never",
)

if __name__ == "__main__":
    # Launch the Gradio app on port 7860
    demo.launch(share=False, server_port=7860)
