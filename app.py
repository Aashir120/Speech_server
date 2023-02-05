from flask import Flask, make_response, request, jsonify,session,Response
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
from Models import db,User,File
from config import ApplicationConfig
from flask_session import Session
import os
from werkzeug.utils import secure_filename
from Speech import SpeechToText
from Classify import classify
import pickle
import jsonpickle

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

ALLOWED_EXTENSIONS = set(['mp3','mp4','wav'])
transcribe_files=[]
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/register", methods=["POST"])
def register_user():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.objects(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    new_user.save()

    session["user_id"] = new_user.id

    return jsonify(new_user)


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.objects(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id

    return jsonify(user)
    

@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.objects(id=user_id).first()
    return jsonify(user) 

@app.route('/')
def home_page():
    return jsonify('Hello World')

# route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        new_file = File(filename=file.filename, data=file)
        new_file.save()
        resp = jsonify({'message' : 'Files successfully uploaded',"id":str(new_file.id)})
        resp.status_code = 201
        SpeechToText(filename)
        with open('classify.txt','r') as f:
            topic_classify = f.read()
        classify(topic_classify)
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

@app.route('/download', methods=['GET'])
def download():
    array=[]
    file_name = "output.txt"
    with open(file_name, "r") as file:
        for line in file:
            array.append(line.strip())
    print(array)
    return jsonify(array)

@app.route('/topic', methods=['GET'])
def topic():
    array=[]
    file_name = "Topic.txt"
    with open(file_name, "r") as file:
        for line in file:
            array.append(line.strip())
    print(array)
    return jsonify(array)

@app.route('/speech', methods=['GET'])
def speech():
    array=[]
    file_name = "classify.txt"
    with open(file_name, "r") as file:
        for line in file:
            array.append(line.strip())
    print(array)
    return jsonify(array)


if __name__ =="__main__":
    app.run(debug=True)
