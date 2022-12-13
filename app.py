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

# Home Page
@app.route('/', endpoint="home")
def index():
    try:
        username = session['user_id']
        isAdmin = session['adminID']
        if isAdmin != '0':
            return redirect("/admin")
    except:
        return render_template('index.html')
    return render_template('index.html')

# Page which shows all the cycles to rent
@app.route('/renting/')
def renting():
    try:
        username = session['user_id']
        isAdmin = session['adminID']
        if isAdmin != '0':
            return redirect("/")
    except:
        flash('Please log in first', 'danger')
        return redirect('/login')
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM bicycle")
    print(resultValue)
    if resultValue > 0:
        bicycles = cur.fetchall()
        cur.close()
        return render_template('renting.html', bicycles=bicycles, user=int(session['user_id']))
    cur.close()
    return render_template('renting.html', bicycles=None)

# Page for individual bike "Renting Form"
@app.route('/renting/bicycles/<int:id>/', methods=['GET', 'POST'])
def bicycle(id):
    cur = mysql.connection.cursor()
    queryStatement = f"SELECT * from bicycle WHERE bike_id = {id}"
    print(queryStatement)
    resultValue = cur.execute(queryStatement)
    if resultValue > 0:
        bicycle = cur.fetchone()
        if request.method == 'GET':
            return render_template('bicycle.html', bicycle=bicycle)
        elif request.method == 'POST':
            bicycleDetails = request.form
            #Check if correct user is asking to rent cycle
            if bicycleDetails['ID'] != session['user_id']:
                flash('ID Mismatch!', 'danger')
                return render_template('bicycle.html', bicycle=bicycle)

            cur.execute(queryStatement)
            bicycleReCheck = cur.fetchone()
            #Re checking if Bicycle is available since it might have been used
            if bicycleReCheck['bike_state'] != 'Available':
                resultValue =  cur.execute("SELECT * FROM bicycle")
                flash('Bicycle is currently unavailable.', 'danger')
                if resultValue > 0:
                    bicycles = cur.fetchall()
                    cur.close()
                return render_template('renting.html', bicycles=bicycles)

            #Change the bike status to Awaiting Approval
            #Add User_ID, Phone_Num, Time to Database
            student_id = bicycleDetails['ID']
            phone_num = bicycleDetails['phone']
            time = bicycleDetails['time']
            queryStatement = f"UPDATE bicycle SET bike_state='Awaiting Approval' WHERE bike_id = {id}"
            cur.execute(queryStatement)
            queryStatement = f"UPDATE bicycle SET user_id='{student_id}', phone_num='{phone_num}', last_return_time='{time}' WHERE bike_id = {id}"
            cur.execute(queryStatement)
            mysql.connection.commit()
            cur.close()
            flash("Rent request has been sent to admin.", "success")
            return redirect('/')  
    return 'Cycle not found'

@app.route('/renting/return-bicycle/<int:id>')
def return_bike(id):
    cur = mysql.connection.cursor()
    query_statement = f"UPDATE bicycle SET bike_state='Awaiting Return Approval' WHERE bike_id = {id}"
    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()
    flash('Return request has been sent to admin.', 'success')
    return redirect('/')

# Sign Up
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        try:
            username = session['user_id']
            flash('Please log out before you create a new account', 'danger')
            return redirect('/')
        except:
            return render_template('register.html')
    elif request.method == 'POST':
        userDetails = request.form

        # Check the password and confirm password
        if userDetails['password'] != userDetails['confirmPassword']:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')

		# Check if ID is numeric
        if str(userDetails['user_id']).isnumeric() == False:
            flash('ID should be a number!', 'danger')
            return render_template('register.html')

		# Check if ID is correct
        if len(userDetails['user_id']) != 7:
            flash('ID needs to be a 7 digit number!', 'danger')
            return render_template('register.html')

        p1 = userDetails['firstName']
        p2 = userDetails['lastName']
        p3 = userDetails['user_id']
        p4 = userDetails['password']

        
        hashed_pw = generate_password_hash(p4)
        print(p1 + "," + p2 + "," + p3 + "," + p4 + "," + hashed_pw)

        queryStatement = (
            f"INSERT INTO "
            f"users(f_name, l_name, user_id, password, admin_role) "
            f"VALUES('{p1}', '{p2}', '{p3}', '{hashed_pw}', False)"
        )
        print(check_password_hash(hashed_pw, p4))
        print(queryStatement)
        cur = mysql.connection.cursor()
        #Check if user_id is a duplicate
        queryStatementCheckID = (f"SELECT * FROM users WHERE user_id = '{p3}'")
        print(queryStatementCheckID)
        duplicateID = cur.execute(queryStatementCheckID)
        if duplicateID > 0:
            flash("This ID is already in the system.", 'danger')
            return render_template('register.html')
        cur.execute(queryStatement)
        mysql.connection.commit()
        cur.close()

        flash("Form Submitted Successfully.", "success")
        return redirect('/')    
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            username = session['user_id']
            flash('You are already logged in', 'danger')
            return redirect('/')
        except:
            return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        user_id = loginForm['user_id']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM users WHERE user_id = '{user_id}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
            user =  cur.fetchone()
            if check_password_hash(user['password'], loginForm['password']):
                
                #Recording Session Information
                session['login'] = True
                session['user_id'] = str(user['user_id'])
                session['adminID'] = str(user['admin_role'])
                session['firstName'] = user['f_name']
                session['lastName'] = user['l_name']
                print(session['user_id'] + " adminID: " + session['adminID'])
                flash('Welcome ' + session['firstName'],'success')

                print(session['adminID'])
                if session['adminID'] == '1':
                    return redirect('/admin/')
                else:
                    return redirect('/')
            else:
                cur.close()
                flash("Wrong Credentials", 'danger')
                return render_template('login.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')

# Delete a certain bike from the database
@app.route('/delete-bicycle/<int:id>/')
def delete_bike(id):
    cur = mysql.connection.cursor()
    query_statement = f"DELETE FROM bicycle WHERE bike_id = {id}"
    cur.execute(query_statement)
    mysql.connection.commit()
    flash("Bicycle has been deleted", 'success')
    return redirect('/admin/')

# Add a new bicycle
@app.route('/admin/bicycle/create/', methods=['GET', 'POST'])
def create_bicycle():
    if request.method == 'POST':
        bike_form = request.form
        bike_type = bike_form['bike_type']
        bike_building = bike_form['bike_building']
        cur = mysql.connection.cursor()
        query_statement = f"INSERT INTO bicycle(bike_types, building_name) VALUES ('{bike_type}', '{bike_building}')"
        cur.execute(query_statement)
        mysql.connection.commit()
        cur.close()
        flash("Added new bike", 'success')
        return redirect('/admin/')
    else:
        return render_template('create-bike.html')


# List all bicycles
@app.route('/admin/', methods=['GET'])
def all_bikes():
    cur = mysql.connection.cursor()
    result_val = cur.execute("SELECT * FROM bicycle")
    if result_val > 0:
        bicycles = cur.fetchall()
        cur.close()
        return render_template('admin.html', bicycles=bicycles)
    else:
        cur.close()
        return render_template('admin.html', bicycles=None)

# List bicycles that belong to a certain building for users
@app.route('/renting/bicycles/<building_name>/')
def all_bikes_by_buildings(building_name):
    try:
        username = session['user_id']
        isAdmin = session['adminID']
        if isAdmin != '0':
            return redirect("/")
    except:
        flash('Please log in first', 'danger')
        return redirect('/login')
    cur = mysql.connection.cursor()
    result_val = cur.execute(f"SELECT * FROM bicycle WHERE building_name = '{building_name}'")
    if result_val > 0:
        bicycles = cur.fetchall()
        cur.close()
        return render_template('renting.html', bicycles=bicycles)
    else:
        cur.close()
        return render_template('renting.html', bicycles=None)

# List bicycles that belong to a certain building
@app.route('/admin/bicycles/<building_name>/')
def all_bikes_by_building(building_name):
    cur = mysql.connection.cursor()
    result_val = cur.execute(f"SELECT * FROM bicycle WHERE building_name = '{building_name}'")
    if result_val > 0:
        bicycles = cur.fetchall()
        cur.close()
        return render_template('admin.html', bicycles=bicycles)
    else:
        cur.close()
        return render_template('admin.html', bicycles=None)

# Approve bicycle rent
@app.route('/admin/approve-rent/<int:id>/')
def approve_bike_rent(id):
    cur = mysql.connection.cursor()
    query_statement = f"UPDATE bicycle SET bike_state='Currently Rented' WHERE bike_id = {id}"
    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()
    flash('Bike rental approved', 'success')
    return redirect('/admin/')
      

# Approve bicycle return
@app.route('/admin/approve-return/<int:id>/')
def approve_bike_return(id):
    cur = mysql.connection.cursor()
    query_statement = f"UPDATE bicycle SET bike_state='Available' WHERE bike_id = {id}"
    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()
    flash('Bike rental approved', 'success')
    return redirect('/admin/')

# Filter bicycles by their type
@app.route('/admin/bicycles/filter_type/<bike_type>/')
def filter_bike_type(bike_type):
    cur = mysql.connection.cursor()
    result_val = cur.execute(f"SELECT * FROM bicycle WHERE bike_types = '{bike_type}'")
    if result_val > 0:
        bicycles = cur.fetchall()
        cur.close()
        return render_template('admin.html', bicycles=bicycles)
    else:
        cur.close()
        return render_template('admin.html', bicycles=None)

# Filter bicycles by their status
@app.route('/admin/bicycles/filter_status/<bike_status>/')
def filter_bike_status(bike_status):
    cur = mysql.connection.cursor()
    result_val = cur.execute(f"SELECT * FROM bicycle WHERE bike_state = '{bike_status}'")
    if result_val > 0:
        bicycles = cur.fetchall()
        cur.close()
        return render_template('admin.html', bicycles=bicycles)
    else:
        cur.close()
        return render_template('admin.html', bicycles=None)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)