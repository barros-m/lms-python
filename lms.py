from flask import Flask, render_template
# from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')
    
if __name__ == "__main__":
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