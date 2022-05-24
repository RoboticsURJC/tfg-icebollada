#!/usr/bin/env python3
import sys
if('/root/.local/lib/python3.9/site-packages' in sys.path):
    sys.path.remove('/root/.local/lib/python3.9/site-packages')
if('/home/pi/.local/lib/python3.9/site-packages' not in sys.path):
    sys.path.append('/home/pi/.local/lib/python3.9/site-packages')
from flask import Flask, render_template, Response, request
import camera_flask_app
import datetime, time
import cv2
from threading import Thread
import base64
import os
from io import BytesIO
from flask import Flask, render_template, redirect, Response, request, url_for, flash, session, \
    abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, EqualTo
import onetimepass
import pyqrcode
import ast
x = camera_flask_app.picam()
#instatiate flask app  
#app = Flask(__name__, template_folder='./templates')

# create application instance
app = Flask(__name__)
app.config.from_object('config')

# initialize extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager(app)
def record():
    while(x.rec):
        time.sleep(0.05)
        x.write_out()



class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    otp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)


@lm.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    password_again = PasswordField('Repeat Password',
                                   validators=[Required(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    token = StringField('Token', validators=[Required(), Length(6, 6)])
    submit = SubmitField('Login')

def getSession(x):
    i = x.index("{")
    f = x.rindex("}")
    s = x[i:f+1]
    return(ast.literal_eval(s))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return render_template('logged.html')
    form = RegisterForm()
    
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('register'))
        # add new user to the database
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # redirect to the two-factor auth page, passing username in session
        session['username'] = user.username

        return redirect(url_for('two_factor_setup', user=user.username, session=session))
    return render_template('register.html', form=form)


@app.route('/twofactor')
def two_factor_setup():
    s = request.args.get('session')
    session = getSession(s)

    if 'username' not in session:
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('index'))
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('two-factor-setup.html', session=session), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    s = request.args.get('session')
    session = getSession(s)
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return render_template('logged.html')
    
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data) or \
                not user.verify_totp(form.token.data):
            flash('Invalid username, password or token.')
            return redirect(url_for('login'))

        # log user in
        login_user(user)
        flash('You are now logged in!')
        return render_template('logged.html')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('index'))


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
        return render_template('logged.html')
    return render_template('logged.html')

@app.route('/logged')
def logged():
    return render_template('logged.html')


# create database tables if they don't exist yet
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
     
# camera.release()
# cv2.destroyAllWindows()

