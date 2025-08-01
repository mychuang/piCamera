from flask import Flask, render_template, Response, url_for 
from stream import run_camera_loop

# 初始化 Flask 應用程式。__name__ 參數表示目前模組的名稱。
app = Flask(__name__)

@app.route('/') 
def index():
    # videourl 變數會傳遞給模板，它的值是 /video_feed 路由的 URL，這樣網頁上的 img 標籤就可以指向這個串流。
    return render_template('index.html', videourl=url_for('video_feed'))

@app.route('/video_feed')
def video_feed():
    # 返回一個 Response 物件，它會以 multipart/x-mixed-replace 的 MIME 類型發送影像串流。
    # gen() 函式是一個生成器，它會持續產生影像幀。
    # boundary=frame 定義了每個影像幀之間的分隔符，這是 MJPEG 串流的標準。
    return Response(run_camera_loop(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)