import datetime
import time
from flask import Flask,request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "nayana.jp@TA.COM"
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'HospitalManagement'

mysql = MySQL(app)


def check_user_exist(email):
    cursor = mysql.connection.cursor()
    user = cursor.execute(f"SELECT id, username FROM Users WHERE email='{email}'")
    cursor.close()
    if user:
        return False
    return True

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    cursor = mysql.connection.cursor()
    users = cursor.execute(f"SELECT id, username FROM Users WHERE username='{username}' AND password='{password}'")
    cursor.close()
    if users == 0:
        return jsonify({'error': 'No user found'}), 404
    print(f"{username=},{password=}, {users=}")
    return {"message": "Success"}


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password1')
    dob = request.json.get('dob')
    email = request.json.get('email')
    age = request.json.get('age')
    gender = request.json.get('gender')
    print("ncjndcjks")
    user_exist = check_user_exist(email)
    print("user_exist",user_exist)
    print(dob)
    if not user_exist:
        jsonify({'error': 'User already exists'}), 500
    else:
        print("scbsbc")
        print(f"{age=}, {type(age)}")
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO Users (username, email, password, created_at, dob, age, gender ) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (username, email, password, datetime.datetime.now(), dob, age, gender))
        print("cbsjcbsjbckjsndckj")
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Registration successful'})
if __name__ == '__main__':
    app.run(debug=True)