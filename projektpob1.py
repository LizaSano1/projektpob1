from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, this is an HTTP/1.1 server!'

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    users.append(data)
    return jsonify({"message": "User created successfully"}), 201

if __name__ == '__main__':
    app.run('127.0.0.1', 8080, debug=True)