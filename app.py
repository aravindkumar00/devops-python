
import os
from flask_mysqldb import MySQL
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector

app = Flask(__name__, static_url_path='/statics', static_folder='statics')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'aravind'
app.config['MYSQL_PASSWORD'] = 'Aravind@111'
app.config['MYSQL_DB'] = 'aru'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def sineup():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS candidates 
                (id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                email VARCHAR(255),
                password varchar(255),
                cpassword varchar(255))''')
    mysql.connection.commit()
    cur.close()
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit',methods=['POST'])
def submit():
    if request.method=='POST':
        
        name = request.form['name']
        email = request.form['email']
        passwor = request.form['password']
        cpassword = request.form['cpassword']
        if passwor==cpassword:
            sineup()
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO candidates (name, email, password, cpassword) VALUES (%s, %s, %s, %s)', (name, email, passwor, cpassword))
            mysql.connection.commit()
            cur.close()
            msg1="Registred successfully Please login"
            return render_template('index.html',msg1=msg1)
        else:
            msg="Password is not same"
            return render_template('login.html',msg=msg)
@app.route('/validate',methods=['POST'])
def validate():
    uname=request.form['un']
    upw=request.form['pw']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM candidates WHERE name = %s AND password = %s", (uname, upw))
    user = cur.fetchone()
    cur.close()
    if user:
        return render_template('Homepage.html')
    else:
        msg="Invalid credentials Please check Username and password"
        return render_template('index.html',msg=msg)
    
@app.route('/products')   
def products():
    return render_template('products.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/homepage')
def homepage():
    return render_template('Homepage.html')

if __name__ == '__main__':
    app.run(debug=True)