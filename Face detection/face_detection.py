import cv2
import matplotlib.pyplot as plt
# import time

# img_path = "C:\PBL\ProctoCam-main\ProctoCam\Face detection\manicare-blog-face-shapes-inlaid-2.jpg"
# img = cv2.imread(img_path)
# print(img.shape) # 3d 

# # converting img to gray scale
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(gray_img.shape) # 2d

# # using the trained model
# face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# face = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors= 5, minSize= (40, 40))

# # drawing rectangles around faces
# for (x, y, w, h) in face:
#     cv2.rectangle(img, (x, y), ((x+w), y+h), (0, 255, 0), 4)

# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# plt.figure(figsize=(10, 20))
# plt.imshow(img_rgb)
# # time.sleep(5)
# plt.axis('off')

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0) # accessing webcam

while True:

    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully

    faces = detect_bounding_box(
        video_frame
    )  # apply the function to the video frame

    cv2.imshow(
        "Face Detection", video_frame
    )  # display the processed frame in a window named "Face Detection"

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()