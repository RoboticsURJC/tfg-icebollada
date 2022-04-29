import cv2
import datetime
from threading import Thread


class picam():
    def __init__(self):
        self.__rec_frame = 0
        self.rec = 0
        self.out = 0
        self.__camera = cv2.VideoCapture(0)

    def gen_frames(self):  # generate frame by frame from camera
        while True:
            ret, frame = self.__camera.read()
            frame = cv2.rectangle(frame, (2,2), (275,35), (255,255,255), -1)
            frame = cv2.putText(frame, str(datetime.datetime.now().replace(microsecond=0)) , (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, cv2.LINE_AA)
            
            if ret:
                if(self.rec):
                    self.__rec_frame = frame
                    frame = cv2.putText(frame,"Recording...", (500,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),1)
                    
                try:
                    r, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    pass
                    
            else:
                pass

    def change_rec(self):
        self.rec = not self.rec
        return self.rec

    def define_out(self, value):
        self.out = value
    
    def write_out(self):
        self.out.write(self.__rec_frame)
        
    