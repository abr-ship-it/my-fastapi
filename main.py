from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
import io

app = FastAPI()


def filter_colors(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # ---------------- ORANGE (ELEMENTS) ----------------
    lower_orange = np.array([8, 120, 120])
    upper_orange = np.array([25, 255, 255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # ---------------- MAGENTA (GRID) -------------------
    lower_magenta = np.array([125, 50, 50])
    upper_magenta = np.array([175, 255, 255])
    mask_magenta = cv2.inRange(hsv, lower_magenta, upper_magenta)

    # White canvas
    result = np.ones_like(image) * 255

    # Orange → Black
    result[mask_orange > 0] = [0, 0, 0]

    # Magenta → Gray
    result[mask_magenta > 0] = [140, 140, 140]

    return result


@app.post("/filter-orange/")
async def filter_orange(file: UploadFile = File(...)):

    contents = await file.read()

    np_array = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    filtered = filter_colors(image)

    _, buffer = cv2.imencode(".png", filtered)
    io_buf = io.BytesIO(buffer)

    return StreamingResponse(io_buf, media_type="image/png")
