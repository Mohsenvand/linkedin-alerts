from __future__ import with_statement
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, request, render_template,session, url_for, abort, \
     render_template, flash, _app_ctx_stack
from wtforms import Form, TextField, validators
from contextlib import closing


DATABASE = "./flaskr.db"
SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    top = _app_ctx_stack.top
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
    email = TextField('Email Address',[validators.Email('Not a valid Email')])


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/email',  methods=['POST'])
def save_email():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.email.data
        db = get_db()
        db.execute('insert into entries (email) values (?)',[request.form['email']])
        db.commit()
        return "Thanks for your e-mail."
    return "Please provide a valid Email."


@app.route('/_get_emails',  methods=['GET'])
def _get_emails():
    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM entries;')
    row = c.fetchall()
    return '<br />'.join([x[1] for x in row])


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
