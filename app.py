from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# MySQL Instance configurations
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')

mysql = MySQL(app)

@app.route("/add", methods=['POST'])  # Use POST method for adding a student
def add():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')

        if name and email:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students (studentName, email) VALUES (%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()

            return jsonify({"Result": "Success"})
        else:
            return jsonify({"Result": "Missing data"}), 400
    except Exception as e:
        return jsonify({"Result": "Error", "Message": str(e)}), 500

@app.route("/", methods=['GET'])
def read():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        rv = cur.fetchall()
        cur.close()

        results = []
        for row in rv:
            result = {
                'Name': row[0].replace('\n', ' '),
                'Email': row[1],
                'ID': row[2]
            }
            results.append(result)

        response = {'Results': results, 'count': len(results)}
        return jsonify(response)
    except Exception as e:
        return jsonify({"Result": "Error", "Message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)