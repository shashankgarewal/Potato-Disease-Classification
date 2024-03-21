from fastapi import FastAPI, File, UploadFile

from io import BytesIO
from PIL import Image
import uvicorn

import numpy as np
import tensorflow as tf
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)

app = FastAPI()
model = tf.keras.models.load_model("models/2") 
class_name = ["Early Blight", "Late Blight", "Healthy"]
#model = tf.saved_model.load("models/2")

@app.post("/predict")
async def predictor(
    file: UploadFile = File(...)
):
    byte_data = await file.read()
    img = np.array(Image.open(BytesIO(byte_data)))
    img_batch = np.expand_dims(img, 0)

    prediction = model.predict(img_batch)
    predict_class = class_name[np.argmax(prediction[0][0])]
    confidence = round(100*np.max(prediction[0]).astype("float"), 2)

    return {
        'class': predict_class, 
        'confidence': confidence
        }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)