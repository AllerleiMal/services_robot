#!/usr/bin/env python3.8
import cv2
import numpy as np
import pytesseract
import imutils
import copy
from PIL import Image
from controller import Robot, Camera, Receiver, DistanceSensor, CameraRecognitionObject

MAX_SPEED = 6.28
SENSOR_VALUE_DETECTION_THRESHOLD = 100

def preprocess(img):
    img = cv2.medianBlur(img,7)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    return img

def predict(img,custom_config):
    return pytesseract.image_to_string(img, config=custom_config)

def recognize(path):
    image = cv2.imread(path,0)
    custom_config = r'--oem 3 --psm 6  outputbase digits'
    pr_image = preprocess(image)
    res = predict(pr_image, custom_config)
    return res
 
     
# create the Robot instance.
robot = Robot()
timestep = int(robot.getBasicTimeStep())
#camera = Camera("camera(1)")
camera = Camera("camera(1)")
camera.enable(timestep);
camera.recognitionEnable(timestep)
receiver = Receiver("receiver")
receiver.enable(timestep)
distance_censor1 = DistanceSensor("ps4")
distance_censor2 = DistanceSensor("ps0")
distance_censor1.enable(timestep)
distance_censor2.enable(timestep)

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

speed = 0.5 * MAX_SPEED

word_to_color = {
    'blu': [0.0, 0.0, 1.0],
    'red': [1.0, 0.0, 0.0],
    'gre': [0.0, 1.0, 0.0],
    'yel': [1.0, 1.0, 0.0],
    'pur': [1.0, 0.0, 1.0]
}

eps_min = 0.15
eps_max = 2
goal_color = [0.0, 0.0, 0.0]
goal_number = "0"

pytesseract.pytesseract.tesseract_cmd = r'..\..\tesseract\tesseract.exe'

left_speed = speed
right_speed = speed * 0.93

leftMotor.setVelocity(left_speed)
rightMotor.setVelocity(right_speed)

robot.step(5000)
if receiver.getQueueLength() > 0:
    print("hello")
    while receiver.getQueueLength() > 0:
        message = receiver.getString()
        try:
            goal_color = word_to_color[message.replace('\0', '')]
        except KeyError as e:
            goal_number = message
        receiver.nextPacket()
            
print("Goal color: " + str(goal_color))
print("Goal number: " + goal_number)
       
while robot.step(timestep) != -1:
    if (speed < 0 and distance_censor1.getValue() > SENSOR_VALUE_DETECTION_THRESHOLD) or (speed > 0 and distance_censor2.getValue() > SENSOR_VALUE_DETECTION_THRESHOLD): 
        left_speed = -left_speed
        right_speed = -right_speed
        leftMotor.setVelocity(left_speed)
        rightMotor.setVelocity(right_speed)
     
    if camera.getRecognitionNumberOfObjects() > 0:
        # print("amount: " + str(camera.getRecognitionNumberOfObjects()))
        object = camera.getRecognitionObjects()[0]
        color_raw  = object.getColors()
        current_color = [color_raw[0], color_raw[1], color_raw[2]]
        print(current_color)
        if current_color == goal_color and eps_min <= abs(object.getPosition()[0]) <= eps_max:
            camera.saveImage(r'view.jpg', 100)
            number = recognize(r'view.jpg')
            number = number.strip()
            print("guess: " + number)
            print("need: " + goal_number)
            
            if len(number) > 0 and goal_number[0] in number:
                print("FOUND!")
                leftMotor.setVelocity(0)
                rightMotor.setVelocity(0)
                break
                
                goal_color = [0.0, 0.0, 0.0]
                goal_number = "0"
            else:
                robot.step(200)
