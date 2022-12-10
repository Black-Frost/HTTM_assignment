import base64
from PIL import Image
from io import BytesIO
import io
import numpy as np
import cv2
import requests

with open("tmp2.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

print(encoded_string)

host = "https://dbf8-2001-ee0-53b6-6c70-9565-919a-860d-6833.ap.ngrok.io/api/v1/predict"
resp = requests.post(url=host, data=encoded_string)
print(resp.text)

# imgdata = base64.b64decode(encoded_string)
# print(io.BytesIO(imgdata))
# img = Image.open(io.BytesIO(imgdata))
# imgArray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
# print(imgArray)
# print(imgArray.shape)

# cv2.imshow("hello", imgArray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()