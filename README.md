# EmotionRecognition
This repository represents a code for creating a SVM model using FER 2013 dataset comes with its evaluation and an android application performing recognition of facial emotions on an image.  

## Author
**Quach Minh Tuan - Vo Van Tien Dung**

## Code for SVM model
### Requirements
+ `Python` >= 3.9.7
+ `Pip` >= 21.2.3
+ Suggest have `GPU`

### Check out the code and install
```sh
git clone https://github.com/Black-Frost/HTTM_assignment.git
cd HTTM_assignment
```

### Install dependencies
```sh
pip install -r requirements.txt
```

### Run code
Using `Jupyter Notebook` and run all blocks in file `fer.ipynb` to create the related figure and SVM model saved as `svm_model.sav` and load again in API connect to Android app below.

Or we can run `Jupyter Notebook` with Google Colab at https://drive.google.com/file/d/18LWGP43WZtp_8SAiTWdT8Egfxu8-sJIe/view?usp=sharing


## The application
To detect faces on an image the application, we uses OpenCV.
After detection complete the face image area converted into greyscale 48*48 pixel format, each pixel represents as [0, 1] float number.
Finally, converted area fed to our custom model, which uses the **SVM** algorithm.
