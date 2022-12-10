from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = "Never push this line to github public repo"

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', endpoint="home")
def index():
    return render_template('index.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        userDetails = request.form

        # Check the password and confirm password
        if userDetails['password'] != userDetails['confirmPassword']:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')

		# Check if StudentID is numeric
        if str(userDetails['studentID']).isnumeric() == False:
            flash('StudentID should be a number!', 'danger')
            return render_template('register.html')

		# Check if StudentID is correct
        if len(userDetails['studentID']) != 7:
            flash('StudentID needs to be a 7 digit number!', 'danger')
            return render_template('register.html')


        p1 = userDetails['firstName']
        p2 = userDetails['lastName']
        p3 = userDetails['studentID']
        p4 = userDetails['password']

        hashed_pw = generate_password_hash(p4)
        print(p1 + "," + p2 + "," + p3 + "," + p4 + "," + hashed_pw)

        queryStatement = (
            f"INSERT INTO "
            f"users(f_name, l_name, studentID, password, admin_role) "
            f"VALUES('{p1}', '{p2}', '{p3}', '{hashed_pw}', False)"
        )
        print(check_password_hash(hashed_pw, p4))
        print(queryStatement)
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        mysql.connection.commit()
        cur.close()

        flash("Form Submitted Successfully.", "success")
        return redirect('/')    
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        studentID = loginForm['studentID']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM users WHERE studentID = '{studentID}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
            user =  cur.fetchone()
            if check_password_hash(user['password'], loginForm['password']):
                
                #Recording Session Information
                session['login'] = True
                session['studentID'] = str(user['studentID'])
                session['adminID'] = str(user['admin_role'])
                session['firstName'] = user['f_name']
                session['lastName'] = user['l_name']
                print(session['studentID'] + " adminID: " + session['adminID'])
                flash('Welcome ' + session['firstName'],'success')
                return redirect('/')
            else:
                cur.close()
                flash("Password doesn't not match", 'danger')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)