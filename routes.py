from flask import Flask, flash, redirect, render_template, request, session, abort,url_for,jsonify
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = "alsjkdlkajshflkshjdfa"
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'hms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()
#
# cursor.execute("SELECT * from users")
# data = cursor.fetchall()


@app.route('/')
@app.route('/login', methods=['GET'])
def login_view():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('dashboard')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['email']
    password = request.form['password']
    if username and password  and request.method == 'POST':

        sql = "SELECT * FROM users WHERE email=%s and password=%s and status='t'"
        data = (username, password)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        row = cursor.fetchone()

        if row:
            session['logged_in'] = True
            session['id'] = row[0]
            session['name'] = row[1]
            session['email'] = row[2]
            return redirect('/dashboard')
        else:
            flash('Email or password is invalid!')
            return login_view()
    else:
        return login_view()


@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return login_view()


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html',title="Dashbord")
    else:
        return redirect('login')


@app.route('/student/add')
def student_add_view():
    if session.get('logged_in'):
        return render_template('pages/student-add.html', title="Add Student")
    else:
        return redirect('login')


@app.route('/student/add', methods=['POST'])
def student_add():
    if session.get('logged_in'):
        sql = "INSERT INTO `students` (`name`, `father_name`, `student_email`, `guardian_contact`, `address`, `merit_no`, `program`, `created_at`, `updated_at`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (request.form['student_name'], request.form['father_name'],request.form['email'],request.form['contact'],request.form['address'],request.form['merit'],request.form['program'],datetime.now(),datetime.now())
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash("Student Successfully added")
        return render_template('pages/student-add.html', title="Add Student")
    else:
        return redirect('login')

@app.route('/student/search', methods=['GET'])
def student_search():
    if session.get('logged_in'):
        if request.args.get('student_name') or request.args.get('email') or request.args.get('program'):
            sql = "SELECT * FROM students WHERE "
            data = list()
            if request.args.get('student_name'):
                sql += " name = %s"
                data.append(request.args.get('student_name'))
            if request.args.get('email'):
                sql += " student_email = %s"
                data.append(request.args.get('email'))
            if request.args.get('program'):
                sql += " program = %s"
                data.append(request.args.get('program'))
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            row = cursor.fetchall()

            return render_template('pages/student-list.html', title="Search Student",row= row)
        else:
            return render_template('pages/student-list.html', title="Search Student")
    else:
        return redirect('login')




@app.route('/student/edit')
def student_edit_view():
    return render_template('pages/student-edit.html', title="Edit Student")

@app.route('/visitors/add')
def visitors_add_view():
    return render_template('pages/visitors-add.html', title="Add Visitors")

@app.route('/visitors/edit')
def visitors_edit_view():
    return render_template('pages/visitors-edit.html', title="Edit Visitors")

@app.route('/room/manage')
def room_manage_view():
    return render_template('pages/room-manage.html', title="Manage Rooms")

@app.route('/transport/add')
def transport_add_view():
    return render_template('pages/transport-add.html', title="Add Vehicle")

@app.route('/transport/edit')
def transport_edit_view():
    return render_template('pages/transport-edit.html', title="Edit Vehicle")

@app.route('/mess/off')
def mess_off():
    return render_template('pages/mess-off.html', title="Mess Off")

if __name__ == '__main__':
    app.run(debug=True)