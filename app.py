import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, request, render_template,session, url_for, abort, \
     render_template, flash, _app_ctx_stack
from wtforms import Form, TextField, validators

DATABASE = "/tmp/flaskr.db"

app = Flask(__name__)



def init_db():
    with app.app_contect():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    top = app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

@app.teardown_appcontext
def close_db_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

class RegistrationForm(Form):
    email = TextField('Email Address',
            validators.Email(message='Not a valid Email'))


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/email',  methods=['POST'])
def save_email():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.email.data
        db = get_db()
        db.execute('insert into entries (email) values (?)',
                     [request.form['email']])
        db.commit()
        return jsonify(success='Thanks for your email')
    return jsonify(error='Invalid Email')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
