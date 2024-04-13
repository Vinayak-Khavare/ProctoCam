import cv2
import numpy as np

# For the face and eye detection load the Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_eyes_and_face(gray_frame, colored_frame):
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_color = colored_frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        cv2.rectangle(colored_frame, (x,y), (x+w, y+h), (255, 0, 0), 4)
        face_center = (x+w//2, y+h//2)
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            center = (x+ex+ew // 2, y+ey+eh // 2)
            cv2.circle(colored_frame, center, 2, (0, 0, 255), -1)
            eye_center = (ex+ew // 2, ey+eh // 2)
            
            # getting the direction of gaze
            direction = gaze_direction(face_center, eye_center)
            print(direction)
        
            if eye_gaze(colored_frame, x, y, w, h):
                # Notify the user.
                print("User is looking away from the camera.")
    
    return colored_frame

def eye_gaze(frame, x, y, w, h):
    eye_region = frame[y:y+h, x:x+w]
    eye_region_gray = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(eye_region_gray, scaleFactor=1.1, minNeighbors=5)
    # If no eyes are detected, then the user is looking away from the camera.
    if len(eyes) == 0:
        return True
    # Otherwise, the user is looking at the camera.
    return False

def gaze_direction(face_center, eye_center):
    angle = np.arctan2(eye_center[1] - face_center[1], eye_center[0] - face_center[0])
    angle = angle * 180 / np.pi
    return angle

# open webcam
webcam_capture = cv2.VideoCapture(0)
print("""Press "q" to Exit.""")
while(True):
    ret, video_frame = webcam_capture.read()
    if(ret is False):
        break
    gray_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
    result = detect_eyes_and_face(gray_frame, video_frame)
    cv2.imshow("Face and Eye", result)
    
    if(cv2.waitKey(1) & 0XFF==ord('q')):
        break

webcam_capture.release()
cv2.destroyAllWindows()