from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'rnc'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()
#
# cursor.execute("SELECT * from users")
# data = cursor.fetchall()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('dashboard')

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['email'] == 'talha@gmail.com':
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return login_view()

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()