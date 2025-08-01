from flask import Flask, render_template, request, redirect, url_for, Response, session
from stream import run_camera_loop

# 模擬帳密（正式上線建議使用資料庫 + 加密）
USERNAME = 'admin'
PASSWORD = '1234'

# 初始化 Flask 應用程式。__name__ 參數表示目前模組的名稱。
app = Flask(__name__)
app.secret_key = 'your-very-secret-key'

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error='帳號或密碼錯誤')

    return render_template('login.html')

@app.route('/main')
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html', videourl=url_for('video_feed'))

@app.route('/video_feed')
def video_feed():
    # 返回一個 Response 物件，它會以 multipart/x-mixed-replace 的 MIME 類型發送影像串流。
    # gen() 函式是一個生成器，它會持續產生影像幀。
    # boundary=frame 定義了每個影像幀之間的分隔符，這是 MJPEG 串流的標準。
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return Response(run_camera_loop(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)