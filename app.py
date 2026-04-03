from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '100802' 
app.config['MYSQL_DB'] = 'flask_api'

mysql = MySQL(app)

# REGISTER
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
                (data['name'], data['email'], data['password']))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "User registered"})

# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                (data['email'], data['password']))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"})

# LOGOUT
@app.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful"})

# CREATE EMPLOYEE
@app.route('/api/employee', methods=['POST'])
def create_employee():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO employee(number,first_name,last_name) VALUES(%s,%s,%s)",
                (data['number'], data['first_name'], data['last_name']))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Employee added"})

# GET ALL EMPLOYEE
@app.route('/api/employee', methods=['GET'])
def get_employee():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

# GET EMPLOYEE BY ID
@app.route('/api/employee/<int:id>', methods=['GET'])
def get_employee_id(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee WHERE id=%s", [id])
    data = cur.fetchone()
    cur.close()
    return jsonify(data)

# UPDATE EMPLOYEE
@app.route('/api/employee', methods=['PUT'])
def update_employee():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("UPDATE employee SET number=%s, first_name=%s, last_name=%s WHERE id=%s",
                (data['number'], data['first_name'], data['last_name'], data['id']))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Updated"})

# DELETE EMPLOYEE
@app.route('/api/employee', methods=['DELETE'])
def delete_employee():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE id=%s", [data['id']])
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    app.run(port=5100, debug=True)