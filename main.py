from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
import numpy as np
import cv2

app = FastAPI()

@app.post("/filter-orange/")
async def filter_orange(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    result = np.full_like(img, 255)
    result[mask > 0] = [0, 0, 0]

    _, buffer = cv2.imencode(".png", result)

    return Response(content=buffer.tobytes(), media_type="image/png")
