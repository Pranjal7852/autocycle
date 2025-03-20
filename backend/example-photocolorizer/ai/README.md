# Old Photo Colorizer📸🌈

Welcome to the Old Photo Colorizer, a user-friendly Gradio app and an api built with FastApi that utilizes [modelscope's](https://huggingface.co/modelscope) colorizer to breathe new life into old black and white photos. 🚀

## About the model 🤖:

ModelScope is a platform that allows users to easily deploy and use machine learning models in their applications. It provides a simple API for users to interact with the models, and a dashboard for users to manage their models. ModelScope also provides a marketplace for users to share their models with the community.

To use models in ModelScope, you can pip install modelscope or refer to their github repo https://github.com/modelscope/modelscope

## Pre-requisites:

- Python 3.10+

## Project Setup 🚀

`Step 1:` Clone the repository

```bash
git clone <repo-url>
```

`Step 2:` Navigate to the project directory

```bash
cd ai
```

`Step 3:` Install the dependencies

```bash
pip install -r requirements.txt
```

`Step 4:` Start the gradio app server

```bash
python gradio_app.py
```

Now you can access the Gradio app at http://localhost:7860/ 🎉

`Step 5:` Start the FastApi server

```bash
python fast_api.py
```

**Note:** _This step is crucial as it starts the FastAPI server, allowing you to make api calls from frontend react application._

Now you can access the FastAPI docs at http://localhost:8000/docs/ 🎉

## How to Use 🎨

1. Simply upload your old black and white photo.
2. Witness the magic as the colorizer brings your photo to life!
3. Use the convenient slider-view to adjust the colorization intensity.

## Acknowledgments 🙏

Special thanks to the [colorizer](https://huggingface.co/modelscope) model from ModelScope that makes this app possible.

Now, go ahead, upload those vintage photos, and let the Old Photo Colorizer work its magic! ✨
