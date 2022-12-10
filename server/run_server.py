import base64
import io
import cv2
import numpy as np
from flask import (Flask, Response, jsonify, json, make_response, render_template,
                   request, send_file, send_from_directory)
from PIL import Image


app = Flask(__name__)
app.config['CORS_HEADER'] = 'Content-Type'


# OpenCV.imread() is BGR color
# Pillow is RGB color

# cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Crop whole face
def face_detect(image):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    print("Run face detect")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if(len(faces) == 0):
        return None, None
    (x,y,w,h) = faces[0]
    print("Return sth")
    cropped = image[y:y+h, x:x+w]
    cv2.resize(cropped, (40, 40), interpolation=cv2.INTER_LINEAR)
    print("Return sth")
    return cropped, (y,y+h,x,x+w)

def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# readb64
def b64_to_image(base64_string): # decode("utf-8") ->  return np.array
    imgdata = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(imgdata))
    imgArray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) # opencv need BGR
    print(imgArray.shape)
    return imgArray

# image path -> base64 encoded
def image_to_b64(image_path: str): # return base64 string
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        print(encoded_string)
        return encoded_string


# body: string
@app.route('/api/v1/predict/', methods=['POST'])
def predictImage():
    data = request.data
    img = b64_to_image(data)
    x = face_detect(img)
    print(x)
    # print(cropped)
    # print(bounding_box)
    # (y,y+h,x,x+w)

    response = make_response("Hello World")
    response.headers.set('Content-Type', 'application/json')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)