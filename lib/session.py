from flask import request, session
from passlib.hash import phpass
from flask_api import FlaskAPI, status

class Session:
    @staticmethod
    def login(mysql):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        cur = mysql.connection.cursor()
        result = cur.execute('SELECT username, user_password FROM phpbb3_users WHERE username = %s', [username])
        data = cur.fetchone()
        cur.close()

        if result > 0 and phpass.verify(password, data['user_password']):
            session['logged_in'] = True
            session['username'] = username

            return {'msg': 'Logged in successfully'}

        else:
            return {'msg': 'Login or password are incorrect'}, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def logout():
        pass

    @staticmethod
    def check_auth():
        pass
