import base64
import io
import cv2
import numpy as np
from flask import (Flask, Response, jsonify, json, make_response, render_template,
                   request, send_file, send_from_directory)
from PIL import Image
import joblib
from torchvision.transforms import transforms
import torch



app = Flask(__name__)
app.config['CORS_HEADER'] = 'Content-Type'


# OpenCV.imread() is BGR color
# Pillow is RGB color

# cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
EMOTION = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'] # old
# {0: 'Anger', 1: 'Disgust', 2: 'Fear', 3: 'Happiness', 4: 'Neutral', 5: 'Sadness', 6: 'Surprise'}
EMOTION_TORCH = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise'] # new

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

def minmax_scale(image):
    if image[6] > 0.15:
        image[6] -= 0.15
        for i in range(6):
            image[i] += 0.025
    eps = 1e-2
    image = (image - image.min()) / (image.max() - image.min())
    image = (image + eps) / (image.sum() + 7 * eps)
    return image

def predict_emotion_torch(image, model_path='enet_b2_7.pt'):
    model = torch.load(model_path, map_location='cpu')  
    convert = transforms.Compose([
        transforms.Resize((260,260)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
    ])
    img = Image.fromarray(image)
    with torch.no_grad():
        predict = model((convert(img)).unsqueeze(0).to(torch.device('cpu')))
        result_prob = predict.cpu().numpy()[0]
        result_prob = minmax_scale(result_prob).tolist()
        prob_json = {EMOTION_TORCH[i]: result_prob[i] for i in range(7)}
        result = EMOTION_TORCH[np.array(result_prob).argmax()]
        return prob_json, result

def faces_detect_emotion(image):
    '''Detect emotion of the face in picture. Cropping is expected to be done at client side'''
    # # predict_emotion
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cropped = cv2.resize(gray, (48, 48), interpolation=cv2.INTER_LINEAR)
    # prob_json, result = predict_emotion(cropped)

    # predict_emotion_torch
    prob_json, result = predict_emotion_torch(toRGB(image))
    return prob_json
    
def detect_face(image):
    '''Detect faces in a picture. Returns the vertexes of the border surrounding the faces'''

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # print("Run face detect")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_list = {"faces": []}
    for face in faces:
        (x,y,w,h) = face
        location = {
            "top": int(y),
            "bottom": int(y+h),
            "left": int(x),
            "right": int(x+w)
        }
        face_list["faces"].append(location)
    return face_list
    

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

@app.route('/api/v1/face-detect/', methods=['POST'])
def classiyEmotionApi():
    data = request.get_json(force=True)
    b64Img = data.get("image")
    img = b64_to_image(b64Img)
    result = detect_face(img)
    return jsonify(result)

@app.route('/api/v1/emotion/', methods=["POST"])
def detectFacesApi():
    data = request.get_json(force=True)
    b64ImgList = data.get("images")
    emotionList = []
    for b64Img in b64ImgList:
        img = b64_to_image(b64Img)
        result = faces_detect_emotion(img)
        emotionList.append(result)
    return jsonify(emotionList)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)