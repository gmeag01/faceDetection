import os
import csv
import numpy as np
import cv2

# Get bounding box coordinate about face with Haar Cascade algorithm
def get_face_coordinate(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)   # Convert color image to grayscale image
    face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')   # model import
    face = face_cascade.detectMultiScale(img, 1.5, 5)   # Get coordinate
    return face

# Save coordinate to csv format(image_name, image_path, x_min, y_min, x_max, y_max) 
def save_coordinate(path, filename):    
    name = filename[:-4]   # image name without format
    face = get_face_coordinate(os.path.join(path, filename))   # Get coordinate with HaarCascade algorithm
    for coor_arr in face:
        x_min, y_min, w, h = coor_arr   
        x_max, y_max = x_min+w, y_min+h
        # Save informations
        with open(os.path.join(path, 'labels.csv'), 'a', newline='') as file:
            w = csv.writer(file)
            w.writerow([name, os.path.join(path, filename), x_min, y_min, x_max, y_max])

for dir in os.listdir('./data'):
    path = os.path.join('./data', dir)
    for filename in [file for file in os.listdir(path) if file.endswith('.jpg')]:
        try:
            save_coordinate(path, filename)
        except:
            pass