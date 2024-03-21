from fastapi import FastAPI, File, UploadFile
import requests

from io import BytesIO
from PIL import Image
import uvicorn

import numpy as np
import tensorflow as tf
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)

app = FastAPI()
class_name = ["Early Blight", "Late Blight", "Healthy"]
endpoint = "http://localhost:8501/v1/models/potato_disease_classification:predict"

@app.post("/predict")
async def predictor(
    file: UploadFile = File(...)
):
    byte_data = await file.read()
    img = np.array(Image.open(BytesIO(byte_data)))
    img_batch = np.expand_dims(img, 0)

    json_image = {'instances': img_batch.tolist()}
    response = requests.post(endpoint, json=json_image)

    prediction = response.json()['predictions'][0]
    print(prediction)
    predict_class = class_name[np.argmax(prediction)]
    confidence = round(100*np.max(prediction).astype("float"), 4)

    return {
        'class': predict_class, 
        'confidence': confidence
        }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8001)