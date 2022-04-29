from flask import Flask, render_template, Response, request
import camera_flask_app
import datetime, time
import cv2
from threading import Thread

x = camera_flask_app.picam()

def record():
    while(x.rec):
        time.sleep(0.05)
        x.write_out()

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    return render_template('login.html')
database={'user':'userpass'}

@app.route('/video_feed')
def video_feed():
    return Response(x.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    if request.method == 'POST':
        if request.form.get('rec') == 'Start/Stop Recording':
            rec = x.change_rec()
            if(rec):
                dt = datetime.datetime.now()
                file = str(datetime.date(dt.year, dt.month, dt.day))
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                x.define_out(cv2.VideoWriter(file + '.avi', fourcc, 25.0, (640, 480)))
                
                #Start new thread for recording the video
                thread = Thread(target = record)
                thread.start()
            
            elif(rec==False):
                x.out.release()
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

@app.route('/form_login', methods=['POST', 'GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
        return render_template('login.html', info='Invalid user')
    else:
        if database[name1] != pwd:
            return render_template('login.html', info='Invalid password')
        else:
            return render_template('index.html', name=name1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
     
# camera.release()
# cv2.destroyAllWindows()

