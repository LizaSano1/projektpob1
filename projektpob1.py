from flask import Flask, request, jsonify

app = Flask(__name__)

users = []
user_id_counter = 1

def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, this is an HTTP/1.1 server!'

@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": f"User with id {user_id} not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    global user_id_counter
    user = {
        "id": user_id_counter,
        "name": data.get("name", ""),
        "lastname": data.get("lastname", "")
    }
    user_id_counter += 1
    users.append(user)
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with id {user_id} not found"}), 404

    data = request.json
    if 'name' in data:
        user['name'] = data['name']
    if 'lastname' in data:
        user['lastname'] = data['lastname']
    return "", 204