import os
import re

from flask import Flask, request, render_template
#from wtforms import Form, TextField, validators

app = Flask(__name__)
EMAIL_RE = re.compile('[^@]+@[^@]+\.[^@]+')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/email',  methods=['POST'])
def save_email():
    if request.method == 'POST':
        email = request.form['email']
        print email
        if not EMAIL_RE.match(email):
            return "Please provide a valid email."
        return "Thanks for your e-mail!"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
