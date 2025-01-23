from flask import Flask, Response, jsonify
from flask_socketio import SocketIO, emit
import cv2 as cv
import numpy as np
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect(data):
    print(data)


def generate_frames():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    face_dect = cv.CascadeClassifier("./haarcascade_frontalface_default.xml")
    eye_dect = cv.CascadeClassifier("./haarcascade_eye.xml")
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_dect.detectMultiScale(gray, 1.3, 5)
            cheating_dect = False

            for (x, y, w, h) in faces:
                cv.rectangle(frame,(x,y),(x+w,y+h),(190,150,178),3)
                cv.circle(frame, (x+int(w*0.5),y+int(h*0.5)),3,(100,100,10),-1)
                
                eyes = eye_dect.detectMultiScale(gray[y:(y+h),x:(x+h)],1.3,5)

                if(len(faces)>1):
                    socketio.emit('cheating_detected', {'name': 'admin', 'message': 'Cheating detected!'})
                    cv.putText(frame,'CHEATING!!!! ',(100,100),cv.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 2, cv.LINE_4)
                    cheating_dect = True

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

            # ... (rest of your existing code for eye detection and angle calculation)
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

                    if(dx==0):
                        if(dy>=0):
                            angle = 90
                        else:
                            angle = -90
                    angle = np.arctan( dy / dx)
                    angle = (angle*180)/(np.pi)
                    
                #constraints
                    if(angle<=7 and angle>=-7):
                        cv.putText(frame,'STRAIGHT ',(20,20),cv.FONT_HERSHEY_SIMPLEX, 1, (255,87,51), 2, cv.LINE_4)
                    elif(angle<15 and angle>7):
                        cv.putText(frame,'RIGHT TILT: '+ str(int(angle)) + 'degrees',(20,20),cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,187), 2, cv.LINE_4)
                    elif(angle>-15 and angle<-7):
                        cv.putText(frame,'LEFT TILT: '+ str(int(angle)) + 'degrees',(20,20),cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,187), 2, cv.LINE_4)
                    else:
                        if((angle>=15 and angle<90) or (angle <= -15 and angle > -90)):
                            socketio.emit('cheating_detected', {'name':'admin', 'message': 'Cheating detected!'})
                            cv.putText(frame,'CHEATING!!!! ',(100,100),cv.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 2, cv.LINE_4)
                            cheating_dect = True
                        else:
                            cv.putText(frame,'STRAIGHT ',(20,20),cv.FONT_HERSHEY_SIMPLEX, 1, (255,87,51), 2, cv.LINE_4)


                # cv.imshow('Frame', frame)
                # if cheating_dect:
                #     count += 1
                #     if(count>8 and count<=20):
                #         timestamp = int(time.time())
                #         save_as = f'caught_{timestamp}.png'
                #         cv.imwrite(save_as,frame)
                #         cv.waitKey(500)
                #     elif count>20:
                #         break
                #
                # if cv.waitKey(1) & 0xFF == ord('q'): 
                #     break
                
                (flag, encodedImage) = cv.imencode(".jpg", frame)
                if not flag:
                    continue


            # Encode the frame in JPEG format
            (flag, encodedImage) = cv.imencode(".jpg", frame)
            if not flag:
                continue

            # Yield the output frame in byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                  bytearray(encodedImage) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    socketio.run(app, debug=True)
