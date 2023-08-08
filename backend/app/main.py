import base64
import io
import os
import sys

import joblib
from PIL import Image
import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classes import Model
import uvicorn
import torchvision.transforms as T


path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Imagestr(BaseModel):
    image: str

@app.post("/predict")
def predict(imgstr:Imagestr):
    imgbytes:str = imgstr.dict()["image"].split(",")[-1]
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(imgbytes,"utf-8"))))
    tensortransforms = T.Compose([
        T.Resize((28,28)),
        T.ToTensor()
    ])
    x_test:torch.Tensor = tensortransforms(img)
    x_test = x_test[-1,:,:]
    mod = Model()
    checkpoint = torch.load("model2.ckpt")
    modw = checkpoint["state_dict"]
    for k in list(modw):
        modw[k.replace("model.","")] = modw.pop(k)
    mod.load_state_dict(checkpoint["state_dict"])
    mod.eval()

    with torch.no_grad():
        y_hat = torch.nn.functional.softmax(mod(x_test),dim=1)
        print(y_hat)
        prediction = torch.argmax(y_hat).item()
        print(prediction)
    lb = joblib.load("labelencoder.joblib")
    predclass = lb.inverse_transform([prediction])
    return {"pred":predclass[0]}


if __name__ == "__main__":
    uvicorn.run("main:app")
