from flask import Flask, render_template, Response, request

import cam

x = cam.seek_camera()

# Initialize Flask
app = Flask(__name__)

# Flask will open the main home page with /
@app.route('/')
def index():
    return render_template('login.html')
database={'user':'userpass'}

@app.route('/video_feed')
def video_feed():
    return Response(x.get_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/off')
def off():
    return render_template('index_camerastopped.html')

@app.route('/on')
def on():
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

# Initialize host address
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True, threaded=True)
    