from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
import stream

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    stream.run_in_background()  # 開始背景錄影
    app.run(host='0.0.0.0', port=5000, debug=True)