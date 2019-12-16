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
            session['name'] = row[2]
            session['email'] = row[3]
            session['type'] = row[7]
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

@app.route('/request/add')
def request_add_view():
    if session.get('logged_in'):
        return render_template('pages/request-add.html', title="Add Request")
    else:
        return redirect('login')

@app.route('/request/add', methods=['POST'])
def request_add():
    if session.get('logged_in'):
        sql = "INSERT INTO `requests` (`student_id`, `request_name`,`reason`,`status`, `created_at`, `updated_at`) values (%s,%s,%s,%s,%s,%s)"
        data = (session.get('id'),request.form['type'], request.form['reason'],'t', datetime.now(), datetime.now())
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash("Request Successfully added")
        return render_template('pages/request-add.html', title="Add Request")

    else:
        return redirect('login')



#request/add
@app.route('/room/add')
def room_add_view():
    if session.get('logged_in'):
        return render_template('pages/room-add.html', title="Add Room")
    else:
        return redirect('login')

@app.route('/room/add', methods=['POST'])
def room_add():
    if session.get('logged_in'):
        sql = "INSERT INTO `rooms` (`name`, `capacity`, `created_at`, `updated_at`) values (%s,%s,%s,%s)"
        data = (request.form['name'], request.form['capacity'],datetime.now(),datetime.now())
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash("Room Successfully added")
        return render_template('pages/room-add.html', title="Add Room")
    else:
        return redirect('login')



@app.route('/room/list', methods=['GET'])
def room_list():
    if session.get('logged_in'):
        sql = "SELECT * FROM rooms "

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()

        return render_template('pages/room-list.html', title="Room List",row= row)

    else:
        return redirect('login')

@app.route('/visitor/add')
def visitor_add_view():
    if session.get('logged_in'):
        sql = "SELECT id,name FROM students"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        return render_template('pages/visitors-add.html', title="Add Visitor",row=row)
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


@app.route('/visitor/add', methods=['POST'])
def visitor_add():
    if session.get('logged_in'):
        sql = "INSERT INTO `visitors` (`student_id`, `relation`, `date`, `contact_no`, `created_at`, `updated_at`) values (%s,%s,%s,%s,%s,%s)"
        data = (request.form['student_id'], request.form['relation'],request.form['date'],request.form['contact'],datetime.now(),datetime.now())
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash("Visitor Successfully added")
        return visitor_add_view()
    else:
        return redirect('login')


@app.route('/visitor/search', methods=['GET'])
def visitor_search():
    if session.get('logged_in'):
        if request.args.get('student_name') or request.args.get('email'):

            sql = "SELECT s.name,v.relation,v.date,v.contact_no FROM visitors as v join students as s on v.student_id = s.id WHERE "
            data = list()
            if request.args.get('student_name'):
                sql += " s.name = %s and"
                data.append(request.args.get('student_name'))
            if request.args.get('email'):
                sql += " s.student_email = %s and"
                data.append(request.args.get('email'))

            sql = sql[:-3]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            row = cursor.fetchall()

            return render_template('pages/visitor-list.html', title="Search Visitor",row= row)
        else:
            sql = "SELECT s.name,v.relation,v.date,v.contact_no FROM visitors as v join students as s on v.student_id = s.id "
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchall()
            return render_template('pages/visitor-list.html', title="Search Visitor",row=row)
    else:
        return redirect('login')

@app.route('/student/search', methods=['GET'])
def student_search():
    if session.get('logged_in'):
        if request.args.get('student_name') or request.args.get('email') or request.args.get('program'):
            # select * from students where name = %s and

            sql = "SELECT s.*, u.student_id as user_assign,r.name as room_name FROM students as s " \
                  " left join users as u on u.student_id = s.id  " \
                  " left join room_allotments as ra on ra.student_id = s.id and ra.deleted_at is null" \
                  " left join rooms as r on r.id = ra.room_id WHERE "
            data = list()
            if request.args.get('student_name'):
                sql += " s.name = %s and"
                data.append(request.args.get('student_name'))
            if request.args.get('email'):
                sql += " s.student_email = %s and"
                data.append(request.args.get('email'))
            if request.args.get('program'):
                sql += " s.program = %s and"
                data.append(request.args.get('program'))
            sql = sql[:-3]
            sql += " order by s.merit_no asc"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            row = cursor.fetchall()

            return render_template('pages/student-list.html', title="Search Student",row= row)
        else:
            sql = "SELECT s.*, u.student_id as user_assign,r.name as room_name FROM students as s " \
                  " left join users as u on u.student_id = s.id  " \
                  " left join room_allotments as ra on ra.student_id = s.id and ra.deleted_at is null" \
                  " left join rooms as r on r.id = ra.room_id order by s.merit_no asc "

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchall()
            return render_template('pages/student-list.html', title="Search Student",row=row)
    else:
        return redirect('login')


@app.route('/student/edit/<id>', methods=['GET'])
def student_edit_view(id):
    if session.get('logged_in'):
        sql = "SELECT * FROM students where id = %s"
        data = (id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        row = cursor.fetchone()
        return render_template('pages/student-edit.html', title="Edit Student",row =row)
    else:
        return redirect('login')

@app.route('/student/remove/room/<id>', methods=['GET'])
def remove_room_of_student(id):
    if session.get('logged_in'):
        sql = "UPDATE `room_allotments` SET `deleted_at`=%s  WHERE student_id = %s"
        data = (datetime.now(),
            id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash("Student Room has been remove",'success')

        return student_search()
    else:
        return redirect('login')

#/student/remove/room/
@app.route('/student/signup/<id>', methods=['GET'])
def student_signup(id):
    if session.get('logged_in'):
        sql = "SELECT * FROM students where id = %s"
        data = (id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        row = cursor.fetchone()

        can = is_student_exist(row[3])
        if can:
            student_insert_to_user(row)
            flash('User has been created', 'success')
        else:
            flash('User email already exists','danger')

        return student_search()
    else:
        return redirect('login')



def student_insert_to_user(row):
    sql = "INSERT INTO `users` (`student_id`, `name`, `email`, `phone`, `password`, `status`,`type_of_account`,`created_at`,`updated_at`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (
    row[0], row[1], row[3], row[4],row[4],'t','s', datetime.now(),
    datetime.now())
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()


def is_student_exist(email):
    sql = "SELECT * FROM users where email = %s"
    data = (email)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    row = cursor.fetchone()
    if row:
        return False
    else:
        return True



@app.route('/student/edit', methods=['POST'])
def student_edit():
    if session.get('logged_in'):
        sql = "UPDATE `students` SET `name`=%s , `father_name`=%s, `student_email`=%s, `guardian_contact`=%s, `address`=%s, `merit_no`=%s, `program`=%s WHERE id = %s"
        data = (
        request.form['student_name'], request.form['father_name'], request.form['email'], request.form['contact'],
        request.form['address'], request.form['merit'], request.form['program'], request.form['id'])
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash("Student record has been updated")
        id = request.form['id']
        return redirect("/student/edit/" + str(id))
    else:
        return redirect('login')

#/room/assign
@app.route('/room/assign', methods=['GET'])
def student_room_assign_view():
    if session.get('logged_in'):
        students = get_students_from_user_room_not_assign()
        rooms   = get_room_list()
        return render_template('pages/room-assign.html', title="Assign Room to Student",students =students,rooms=rooms)
    else:
        return redirect('login')


@app.route('/room/assign', methods=['POST'])
def student_room_assign():
    if session.get('logged_in'):
        student_id = request.form['student_id']
        room_id = request.form['room_id']
        capacity = get_room_capacity(room_id)
        count = room_count_by_id(room_id)

        if ( int(count) < int(capacity)):
            flash('Room has been assign','success')
            assign_room_to_student(student_id,room_id)
        else:
            flash('Room unable to assign','danger')

        return student_room_assign_view()
    else:
        return redirect('login')

def assign_room_to_student(student_id,room_id):
    sql = "INSERT INTO `room_allotments` (`room_id`,`student_id`,`created_at`,`updated_at`) values (%s,%s,%s,%s)"
    data = (
        room_id,student_id,   datetime.now(),
        datetime.now())
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()


def room_count_by_id(room_id):
    sql = "SELECT count(id) FROM room_allotments where room_id = %s and deleted_at is null"
    data = (str(room_id))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    row = cursor.fetchone()
    if row:
        return str(row[0])
    else:
        return "0"

def get_room_capacity(room_id):
    sql = "SELECT * FROM rooms where id = %s"
    data = (str(room_id))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,data)
    row = cursor.fetchone()
    if row:
        return str(row[2])
    else:
        return "0"

def get_room_list():
    sql = "SELECT * FROM rooms"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_students_from_user_room_not_assign():
    sql = "SELECT s.* FROM students as s join users as u on u.student_id = s.id WHERE s.id NOT IN (SELECT student_id FROM room_allotments where deleted_at is null)"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

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