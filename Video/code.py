# -*- coding: utf-8 -*-
"""Task2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zfFcL7TAUPF-VOnc6JR2EGIQiG21lo1z
"""

import face_recognition
import cv2

# This code implements face recognition on a video(input.mp4)
# and saves the result in a new video file(output.avi)

# Opening the input
input_video = cv2.VideoCapture("input1.mp4")
length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

# Creating the output file with specifications same as input file
fourcc = cv2.VideoWriter_fourcc('M','P','E','G')
output_video = cv2.VideoWriter('output.avi', fourcc, 23.976024, (1280, 538))

# Providing sample images to learn how to recognize them
image1 = face_recognition.load_image_file("ryan.jpeg")
image1_encoding = face_recognition.face_encodings(image1)[0]

image2 = face_recognition.load_image_file("steve.jpeg")
image2_encoding = face_recognition.face_encodings(image2)[0]

# Initializing an array of known faces
known_faces = [
    image1_encoding,
    image2_encoding
]

face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Selecting one frame of the video
    ret, frame = input_video.read()
    frame_number += 1

    # Stop at Enf Of File(Video)
    if not ret:
        break

    # OpenCV uses BGR color, converting it to RGB color used by face_recognition
    rgb_frame = frame[:, :, ::-1]

    # Detecting all the faces in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Checking if face matches to a known face
        check = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        name = None
        if check[0]:
            name = "Ryan"
        elif check[1]:
            name = "Steve"
        else:
          name = "Unknown"

        face_names.append(name)

    # Labeling the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Write the label(Name of person) below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Writing the resulting image to the output video
    print("Writing frame {} / {}".format(frame_number, length))
    output_video.write(frame)

# Releasing the memory
input_video.release()

# Done

!pip install face_recognition