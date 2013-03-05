import os

from flask import Flask, jsonify, request, render_template
from wtforms import Form, TextField, validators

app = Flask(__name__)


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
        user = User(form.email.data)
        db_session.add(user)
        return jsonify(success='Thanks for your email')
    return jsonify(error='Invalid Email')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
