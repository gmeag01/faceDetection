'''
In first activation, you should run this file for make datasets 

You have to make directory './data' and put in dataset images

Then you can get a labels.csv file including name, path, min & max of x,y coordinations
'''

import os
import numpy as np
import csv
import cv2

# Get bounding box coordinate about face with Haar Cascade algorithm
def get_face_coordinate(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    frontal_face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')   # model import
    profile_face_cascade = cv2.CascadeClassifier('./model/haarcascade_profileface.xml')
    frontal_face = np.array(frontal_face_cascade.detectMultiScale(img, 1.3, 5))   # Get coordinate
    profile_face = np.array(profile_face_cascade.detectMultiScale(img, 1.3, 5))

    if frontal_face.any() and profile_face.any(): 
        return np.concatenate([frontal_face, profile_face])
    elif not frontal_face.any() and profile_face.any(): 
        return profile_face
    elif frontal_face.any() and not profile_face.any(): 
        return frontal_face
    else:
        pass

# Save coordinate to csv format(image_name, image_path, x_min, y_min, x_max, y_max) 
def save_coordinate(path, filename):
    name = filename[:-4]   # image name without format
    face = get_face_coordinate(os.path.join(path, filename))   # Get coordinate with HaarCascade algorithm
    for coor_arr in face:
        x_min, y_min, w, h = coor_arr   
        x_max, y_max = x_min+w, y_min+h
        # Save informations
        with open(os.path.join(path, 'labels.csv'), 'a', newline='') as file:
            wr = csv.writer(file)
            wr.writerow([name, os.path.join(path, filename), x_min, y_min, x_max, y_max])

# Adapt algorithm
def make_data(path):
    for filename in [file for file in os.listdir(path) if file.endswith('.jpg')]:
        try:
            save_coordinate(path, filename)
        except:
            pass  # if algorithm didn't get coordinate, just skip it.

def get_frame(video_folder_path, fps):
    for video_name in [video_path for video_path in os.listdir(video_folder_path) if video_path.endswith('.mp4')]:
        n = 0
        cap = cv2.VideoCapture(os.path.join(video_folder_path, video_name))
        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret : break

            frame = cv2.resize(frame, (960, 960))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if(int(cap.get(1)) % fps == 0):
                path = os.path.join(video_folder_path, video_name[:-4])+ '_' + str(n) + '.jpg'
                cv2.imwrite(path, frame)
            n += 1
        cap.release()
try:
    path = './data'
    with open(os.path.join(path, 'labels.csv'), 'w', newline='') as file:
        wr = csv.writer(file)
        wr.writerow(['name', 'path', 'x_min', 'y_min', 'x_max', 'y_max'])
    get_frame(path, 30)
    make_data(path)
except Exception as e:
    print('Error : ', e)