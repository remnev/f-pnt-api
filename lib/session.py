from flask import request, session
from passlib.hash import phpass
from flask_api import status, exceptions
from functools import wraps


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

            return {'message': 'Logged in successfully'}

        else:
            raise exceptions.ParseError(detail='Login or password are incorrect')

    @staticmethod
    def logout():
        session.clear()

        return {'message': 'Logged out successfully'}

    @staticmethod
    def check_auth(f):
        @wraps(f)
        def checker(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)

            else:
                raise exceptions.PermissionDenied()

        return checker


    @staticmethod
    def get_session_data():
        return dict(session)
