from flask_api import FlaskAPI
from flask_mysqldb import MySQL
from envparse import env
from lib.session import Session

app = FlaskAPI(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = env('MYSQL_HOST', cast=str)
app.config['MYSQL_USER'] = env('MYSQL_USER', cast=str)
app.config['MYSQL_PASSWORD'] = env('MYSQL_PASSWORD', cast=str)
app.config['MYSQL_DB'] = env('MYSQL_DB', cast=str)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialise MySQL
mysql = MySQL(app)


@app.route('/login', methods=['POST'])
def login():
    return Session.login(mysql=mysql)


@app.route('/logout', methods=['POST'])
def logout():
    return Session.logout()


@app.route('/session')
@Session.check_auth
def session():
    return Session.get_session_data()


if __name__ == '__main__':
    app.secret_key = env('SESSION_SECRET_KEY', cast=str)
    app.run(debug=env('DEBUG', cast=bool))
