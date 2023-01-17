import cv2
import pytesseract
from matplotlib import pyplot as plt

def preprocess(img):
    img = cv2.medianBlur(img,7)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    return th2

def predict(img,custom_config):
    return pytesseract.image_to_string(img, config=custom_config)

def recognize(path):
	print("hello")
	image = cv2.imread(path,0)
	custom_config = r'--oem 3 --psm 6  outputbase digits'
	pr_image = preprocess(image)
	res = predict(pr_image, custom_config)

	return res


############
print(recognize('robots.jpg'))