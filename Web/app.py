from flask import Flask, render_template, Response, url_for 
import cv2 

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
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(): 
    cap = cv2.VideoCapture(0) # 初始化網路攝影機物件。0 表示使用系統預設的網路攝影機。
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600) # 設定影像寬度為 600 像素。
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 設定影像高度為 480 像素。
    cap.set(cv2.CAP_PROP_FPS, 40) # 設定幀率 (Frames Per Second) 為 40。

    while True: # 無限迴圈，持續從網路攝影機讀取影像幀。
        ret, img = cap.read() # 讀取一幀影像。ret 是布林值，表示是否成功讀取；img 是讀取到的影像幀。
        if not ret: # 如果沒有成功讀取影像幀，則跳出迴圈。
            break
        
        # 將影像編碼為 JPEG 格式。
        # ret 是布林值，表示是否成功編碼；jpeg 是編碼後的影像數據。
        ret, jpeg = cv2.imencode('.jpg', img) 
        if not ret: # 如果沒有成功編碼，則跳過當前幀，繼續處理下一幀。
            continue
        
        # 使用 yield 返回一個字節串，這就是 MJPEG 串流的一個影像幀。
        # 它包含了 MJPEG 串流的標準頭部信息 (Content-Type) 和實際的 JPEG 影像數據。
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release() # 當迴圈結束時，釋放網路攝影機資源。

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)