from flask import Flask, render_template, request, session, redirect
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
    try:
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

# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = connectToDB()
        cur = conn.cursor()

        try:
            sql = "SELECT s.studentId, r.status, s.password from Requests as r JOIN Student as s ON r.studentId = s.studentId where s.email='{}'".format(email)
            cur.execute(sql)
        except:
            print("Could not run query")

        results = cur.fetchone()
        if results == None:
            return "User not in the DB"
    
        if results[2] != password:
            perror = "Wrong password"
            return render_template('login.html', email=email, perror=perror)
        # if status == 'a' (accepted)
        if results[1] == 'a' :
            session['logged_in'] = True
            return render_template('content.html', user=results[0])
        elif results[1] == 'p':
            return  "Still pending professor's approval. Please contanct him."

        cur.close()
        conn.close()

        
    return render_template('login.html')

# Register       
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        pword = request.form['password']
        cpword = request.form['confirmPassword']

        # incorrect password...
        if pword != cpword:
            perror = "Passwords must match"
            return render_template('register.html', fname=fname, lname=lname, email=email, perror=perror)
        if len(pword) < 3:
            perror = "Password too small"
            return render_template('register.html', fname=fname, lname=lname, email=email, perror=perror)

        # incorrect email...
        if '@' not in email or '.' not in email or len(email) < 5:
            eerror = "Invalid email"
            return render_template('register.html', fname=fname, lname=lname, eerror=eerror)

        if register_student(fname, lname, email, pword) == True:
            return "DONE. {} Added...\n".format(fname)
        else:
            #return "COULD NOT ADD {}".format(fname)
            eerror = "Email already taken" # hopefully, only this error could be generated
            return render_template('register.html', fname=fname, lname=lname, eerror=eerror)            
    return render_template('register.html')

def register_student(f, l, e, p):
    conn = connectToDB()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Student(studentId, firstName, lastName, email, password, grade) VALUES (nextval('student_sequence'), %s, %s, %s, %s, 0)", (f, l, e, p))
        conn.commit()
        return True    
    except:
        return False
    

#@app.route('/administrator')
def admin_page():
    if request.method == 'POST':
        conn = connectToDB()
        cur = conn.cursor()
    
        try:
            cur.execute("SELECT s.studentId, s.firstName, s.lastName, s.email from Requests as r JOIN Student as s ON r.studentId = s.studentId where r.status = 'p'")
        except:
            print("ERROR executing query")
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin.html', pendingStudents=results)

@app.route('/admin', methods=['POST', 'GET'])
def admin_page_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
        if email == 'admin' and password == 'admin':
            return admin_page()
        return render_template('loginAdmin.html', perror="wrong email or password")
    return render_template('loginAdmin.html')
    
@app.route('/authorize/<id>')
def authorize(id):
    sql = "UPDATE requests SET status='a' WHERE studentId='{}'".format(id)

    conn = connectToDB()
    cur = conn.cursor()
    
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()
    return redirect('/admin')       


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