from flask import Flask, jsonify, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'mydatabase'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'asdfghjkl'

mysql = MySQL(app)
CORS(app)
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/')
def index():
    return jsonify(message='Welcome to the index page')

@app.route('/signup', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return jsonify(message='Registration successful. Please login.')

    return jsonify(errors=form.errors)

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]  # Store user ID in the session
            session.modified = True  # Ensure the session is marked as modified
            return jsonify(message='Login successful', user_id=user[0])
        else:
            return jsonify(error='Login failed. Please check your email and password')

    return jsonify(errors=form.errors)



@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        print(user_id)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return jsonify(user={
                'id': user[0],
                'name': user[1],
                'email': user[2]
            })
    
    return jsonify(error='Unauthorized. Please login.')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify(message='Logout successful')

if __name__ == '__main__':
    app.run(debug=True)
