import cv2
import numpy as np

# Detector one or more face
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# Crop whole face
def face_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detectMultiScale(
    #         gray,
    #         scaleFactor=1.1,
    #         minNeighbors=7,
    #         minSize=(100, 100),)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if(len(faces) == 0):
        return None
    (x,y,w,h) = faces[0]
    cropped = image[y:y+h, x:x+w]
    cv2.resize(cropped, (224, 224), interpolation=cv2.INTER_LINEAR)

    norm = np.zeros((224,224))
    cropped = cv2.normalize(cropped, norm, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite("image.png", cropped)
    return cropped

# # Use crop_faec() for face detection
# image = cv2.imread(file_path) # Get pixel
# cropped_image = crop_face(image, True)