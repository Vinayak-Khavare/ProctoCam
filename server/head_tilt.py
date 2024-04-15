import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to open camera.")
    exit()
face_dect = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_dect = cv.CascadeClassifier("haarcascade_eye.xml")
count = 0
while(True):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #detect the face
    faces = face_dect.detectMultiScale(gray, 1.3, 5)
    x,y,w,h = 0,0,0,0
    cheating_dect = False
    
    for (x, y, w, h) in faces:
        #draw a rectangle around the face
        cv.rectangle(frame,(x,y),(x+w,y+h),(190,150,178),3)
        #draw a circle at the center of the reactangle ie face
        cv.circle(frame, (x+int(w*0.5),y+int(h*0.5)),3,(100,100,10),-1)
    eyes = eye_dect.detectMultiScale(gray[y:(y+h),x:(x+h)],1.3,5) #detect the eyes in the face. since eyes will lie within rectangular box we
                                                              # the box region of image that is 'grey[y:y+h,x:x+w]
    index = 0
    eye_1=[None,None,None,None]
    eye_2=[None,None,None,None]

    for(ex,ey,ew,eh) in eyes:
        if index==0:
            eye_1 = [ex,ey,ew,eh]
        elif index==1:
            eye_2 = [ex,ey,ew,eh]
        
        cv.rectangle(frame[y:y+h,x:x+h],(ex,ey),(ex+ew,ey+eh),(150,18,179),4)
        index += 1

    if(eye_1[0] is not None) and (eye_2[0] is not None):
        if(eye_1[0]<=eye_2[0]):
            eye_l = eye_1
            eye_r = eye_2
        else:
            eye_l = eye_2
            eye_r = eye_1
        
        left_eye_center = (int(eye_l[0]+(eye_l[2]//2)),int(eye_l[1] + (eye_l[3]//2)))
        right_eye_center = (int(eye_r[0]+(eye_r[2]//2)),int(eye_r[1] + (eye_r[3]//2)))

        lex = left_eye_center[0]
        ley = left_eye_center[1]
        rex = right_eye_center[0]
        rey = right_eye_center[1]

        dx = rex-lex
        dy = rey-ley

        if(dx ==0):
            if(dy>=0):
                angle = 90
            else:
                angle = -90
        angle = np.arctan( dy / dx)
        angle = (angle*180)/(np.pi)
        
    #constraints
        if(angle<=3 and angle>=-3):
            cv.putText(frame,'STRAIGHT ',(20,20),cv.FONT_HERSHEY_SIMPLEX, 1, (255,87,51), 2, cv.LINE_4)
        elif(angle<12 and angle>3):
            cv.putText(frame,'RIGHT TILT: '+ str(int(angle)) + 'degrees',(20,20),cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,187), 2, cv.LINE_4)
        elif((angle>=12 or angle<=-12) and (angle != 90 or angle != -90)):
            cv.putText(frame,'CHEATING!!!! ',(100,100),cv.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 2, cv.LINE_4)
            cheating_dect = True
        elif(angle>-12 and angle<-3):
            cv.putText(frame,'LEFT TILT: '+ str(int(angle)) + 'degrees',(20,20),cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,187), 2, cv.LINE_4)
        

    cv.imshow('Frame', frame)
    if cheating_dect:
        count += 1
        if(count>8):
            timestamp = int(time.time())
            save_as = f'caught_{timestamp}.png'
            cv.imwrite(save_as,frame)
            cv.waitKey(2500)
  
    if cv.waitKey(1) & 0xFF == 27: 
        break
cap.release() 
cv.destroyAllWindows() 

