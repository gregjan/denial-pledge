from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    app.run("0.0.0.0", processes=5)
