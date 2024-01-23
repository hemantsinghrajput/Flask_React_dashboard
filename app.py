from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalanyfufh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure random key
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/signup", methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    user_exists = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
    if user_exists:
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return jsonify(access_token=access_token, email=new_user.email)

@app.route("/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def login_user():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first() or User.query.filter_by(username=email).first()

    if user is None or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token, email=user.email)

@app.route('/dashboard', methods=['GET'])
@jwt_required()
@cross_origin(supports_credentials=True)
def get_dashboard_data():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    dashboard_data = {
        'username': user.username,
        'email': user.email,
        'dashboard_info': 'Some dashboard information',
    }

    return jsonify(dashboard_data)

@app.route('/all_profiles', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_profiles():
    users = User.query.all()
    profiles = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(profiles)

if __name__ == "__main__":
    app.run(debug=True)
