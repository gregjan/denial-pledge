from flask import Flask, render_template, request, flash, redirect, url_for
import logging
import sqlite3
import os
import json
from itsdangerous import TimestampSigner

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.instance_path, 'flask.db'),
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='default',
    SECRET_KEY='INSECURE_DEVELOPMENT_KEY',
    PROPAGATE_EXCEPTIONS=True
))
verify_key = os.getenv('SECRET_VERIFY_KEY', 'DO NOT USE THIS ONE')
signer = TimestampSigner(verify_key)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/pledge')
def pledge():
    return render_template('pledge.html')


@app.route('/do_pledge', methods=['POST'])
def do_pledge():
    db = get_db()
    # read the posted values from the UI
    fullname = request.form['fullname']
    email = request.form['email']
    city = request.form['city']
    state = request.form['state']
    # validate the received values
    if fullname and email and city and state:
        cur = db.execute("""SELECT fullname FROM user
                        WHERE email = ?;""", [email])
        if len(cur.fetchall()) > 0:
            flash('This email has already requested to sign the pledge.')
            return redirect(url_for('welcome'))
        else:
            verify_token = signer.sign(email)
            signer.unsign(verify_token, max_age=5)
            db.execute("""INSERT INTO user(fullname, city, state, email, verify_token, submitted_on)
                           values(?, ?, ?, ?, ?, date('now'));""",
                       [fullname, city, state, email, verify_token])
            db.commit()
            flash('''Your verification email arrive after one day.
                  You have one day to consider your choice.''')
            return redirect(url_for('submitted'))
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/submitted')
def submitted():
    return render_template('submitted.html')


def get_db():
    """Connects to the specific database."""
    logging.info(str(app.config['DATABASE']))
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.before_first_request
def init_db():
    db = get_db()
    with app.open_instance_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    logging.warn('Database initialized.')


if __name__ == '__main__':
    app.run("0.0.0.0", processes=5)
