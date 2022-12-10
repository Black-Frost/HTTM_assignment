import base64
import io
import cv2
import numpy as np
from flask import (Flask, Response, jsonify, json, make_response, render_template,
                   request, send_file, send_from_directory)
from PIL import Image
import joblib


app = Flask(__name__)
app.config['CORS_HEADER'] = 'Content-Type'


# OpenCV.imread() is BGR color
# Pillow is RGB color

# cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
EMOTION = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# FER predict
def predict_emotion(image, model_path='svm_model.sav', pca_path='pca_model.sav'):
    loaded_model = joblib.load(model_path)
    image_flat = image.reshape(1,-1)
    loaded_pca = joblib.load(pca_path)
    pca_image = loaded_pca.transform(image_flat) #1, 28
    # predict_proba, predict
    result_prob = loaded_model.predict_proba(pca_image)[0]
    prob_json = {EMOTION[i]: result_prob[i] for i in range(7)}
    result = EMOTION[np.array(result_prob).argmax()]
    return prob_json, result


def faces_detect_emotion(image):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # print("Run face detect")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    final_result = {}
    for face in faces:
        (x,y,w,h) = face
        cropped = gray[y:y+h, x:x+w]
        # print(y, y+h, x, x+w)
        # [int(y), int(y+h), int(x), int(x+w)]
        location = {
            "top": int(y),
            "bottom": int(y+h),
            "left": int(x),
            "right": int(x+w)
        }
        cropped = cv2.resize(cropped, (48, 48), interpolation=cv2.INTER_LINEAR)
        prob_json, result = predict_emotion(cropped)
        tmp = {
            "location": location,
            "emotion": result,
            "prob": prob_json
        }
        final_result["face_" + str(len(final_result) + 1)] = tmp
    
    return final_result

def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# readb64
def b64_to_image(base64_string): # decode("utf-8") ->  return np.array
    imgdata = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(imgdata))
    imgArray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) # opencv need BGR
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
    result = faces_detect_emotion(img)
    print(result)

    response = make_response("Hello World")
    # response.headers.set('Content-Type', 'application/json')
    return result
    # return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)