from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from io import BytesIO
import cv2
import numpy as np
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import uuid
import os

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

img_colorization = pipeline(Tasks.image_colorization, model='iic/cv_ddcolor_image-colorization')

def colorize_image(image):
    # Run colorization model
    output = img_colorization(image[...,::-1])
    result = output[OutputKeys.OUTPUT_IMG].astype(np.uint8)

    # Convert the image to bytes
    _, img_bytes = cv2.imencode(".png", cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    return img_bytes.tobytes()

@app.post("/ai/restore_photo")
async def restore_photo(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    restored_image_bytes = colorize_image(image)

    if not restored_image_bytes:
        raise HTTPException(status_code=500, detail="Image processing failed.")

    return StreamingResponse(BytesIO(restored_image_bytes), media_type="image/png")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
