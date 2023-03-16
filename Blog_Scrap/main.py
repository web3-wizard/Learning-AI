from flask import Flask, jsonify, request
from flask_cors import CORS
import json 
from datetime import datetime, timedelta
from random import randint
import jwt



app = Flask(__name__)
CORS(app)
# ------------------------------------------ Authentication -----------------------
app.config['SECRET_KEY'] = 'The^Most#Unhackable$Key!is@here'

# read user data from a JSON file
with open('user.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

# get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    all_users = []
    for user in users:
        all_users.append({'id': user['id'], 'name': user['username']})
    return jsonify(all_users)

# login endpoint generates a JWT token on successful login
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print("From python " , username, password)
    print("users ", users)
    user = next((user for user in users if user['username'] == username), None)
    if user and user['password'] == password:
        # generate JWT token with a 1-hour expiry time
        expiry = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode({'username': username, 'exp': expiry}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# logout endpoint requires a valid JWT token to log out
@app.route('/auth/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing token'}), 401
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload['username']
        return jsonify({'message': f'Goodbye, {username}!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

# route to check if user is logged in or not using JWT token
@app.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing token'}), 401
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload['username']
        return jsonify({'message': f'Welcome back, {username}!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

# ---------------------------------------------- Api Routes -----------------------
file = "data.json"

def read_data():
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_data(_data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(_data, f)

# / get route
@app.route("/")
def hello_world():
    return "Hello from Flask App!"

# /api/posts get route
@app.route("/api/posts", methods=['GET'])
def get_posts():
    posts = read_data()
    return jsonify(posts)

# /api/posts post route
@app.route("/api/posts", methods=['POST'])
def create_post():
    data = request.get_json()
    posts = read_data()
    post = {
        'id': len(posts) + 2,
        "title": data["title"], 
        "author": data["author"], 
        "author_image": data["author_image"], 
        "time": datetime.utcnow(), 
        "cover_image": data["cover_image"], 
        "likes" : randint(1, 25),
        "body": data["body"] 
    }

    posts.append(post)
    write_data(posts)
    return jsonify(post)


# /api/posts/:id get route
@app.route("/api/posts/<int:id>", methods=['GET'])
def get_post(id):
    posts = read_data()
    post = next((post for post in posts if post['id'] == id), None)
    if post:
        return jsonify(post)
    else:
        return jsonify({'error' : 'Post not found!'})


# /api/posts/:id put route
@app.route("/api/posts/<int:id>", methods=['PUT'])
def update_post(id):
    data = request.get_json()
    posts = read_data()
    post = next((post for post in posts if post['id'] == id), None)
    if post:
        post['title'] = data.get('title', post['title'])
        post['body'] = data.get('body', post['body'])
        post['time'] = datetime.utcnow()
        write_data(posts)
        return jsonify(post)
    else:
        return jsonify({'error':'Post not found'})


# /api/posts/:id delete route
@app.route("/api/posts/<int:id>", methods=['DELETE'])
def delete_post(id):
    posts = read_data()
    post = next((post for post in posts if post['id'] == id), None)
    if post:
        posts.remove(post)
        write_data(posts)
        return jsonify(post)
    else:
        return jsonify({'error': 'Post not found!'})


if __name__ == "__main__":
    app.run(debug=True)