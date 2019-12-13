from flask import Flask, jsonify,render_template
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/hello')
def hello():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()