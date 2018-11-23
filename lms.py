from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import psycopg2
# from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_pyfile('config.cfg')


mail = Mail(app)

# connect to DB
def connectToDB():
    # connection String
    conStr = "dbname=postgres user=postgres password=lms host=localhost"
    print("************",conStr)
    try:
        print("***** HELLO")
        return psycopg2.connect(conStr)
    except:
        print("Could not connect to DB")    

# MAIN PAGE
@app.route('/')
def homepage():
    return render_template('index.html')

# SEND EMAIL
@app.route('/send_request')
def send_request():
    #if request.method == 'GET':
     #   return "REQUEST COULD NOT BE SENT"

    email='mbarr241@fiu.edu'
    msg = Message('Confirm Email', sender='matheusbarros1305@hotmail.com', recipients=[email])

    msg.body = "I think we are good for now. Hopefully..."
    mail.send(msg)

    return "Check your fiu email ({})...".format(email)

# LOGIN - Still missing add to DB       
@app.route('/login', methods=['POST', 'GET'])
def login():
    print("hi")
    if request.method == 'POST':
        return "DONE. But not added...\n"
    return render_template('login.html')


@app.route('/admin')
def admin_page():
    print("ADMIN PAGE...")
    conn = connectToDB()
    cur = conn.cursor()

    try:
        cur.execute("SELECT s.studentId, s.firstName, s.lastName from Requests as r JOIN Student as s ON r.studentId = s.studentId where r.status = 'p'")
    except:
        print("ERROR executing query")
    results = cur.fetchall()
    return render_template('admin.html', students=results)
        
if __name__ == "__main__":
    # conn = connectToDB()
    app.run(host='0.0.0.0', port=80) # need ssl_context=

    '''
        cur = mysql.connection
        app.run(host='0.0.0.0')
    
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'matheus'
        app.config['MYSQL_PASSWORD'] = 'jovem'
        app.config['MYSQL_DB'] = 'unibooks'
    '''
        # cur = mysql.connection.cursor()
    
        # cur.execute(CREATE DATABASE book)