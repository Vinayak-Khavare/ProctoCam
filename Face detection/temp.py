import cv2
import numpy as np


cap = cv2.VideoCapture(0)    
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        eyes = eye_cascade.detectMultiScale(gray[y:y+h, x:x+w])
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)
            # Calculate the center of the eyes.
            eye_centers = [(ex + ew / 2, ey + eh / 2) for (ex, ey, ew, eh) in eyes]
            # Calculate the direction of the gaze.
            gaze_direction = np.array(eye_centers[1]) - np.array(eye_centers[0])
            # Normalize the gaze direction.
            gaze_direction = gaze_direction / np.linalg.norm(gaze_direction)
            # Print the gaze direction.
            print(gaze_direction)
        
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    