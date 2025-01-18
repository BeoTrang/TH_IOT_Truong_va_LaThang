from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime
import time

# Cấu hình Flask
app = Flask(__name__)

# Cấu hình MQTT
broker = "192.168.0.103"  # Địa chỉ broker MQTT của bạn
port = 1883
topic = "MQTT_DongCo_DCs"
current_status = "0"  # Mặc định trạng thái động cơ là tắt
current_time = "N/A"  # Mặc định thời gian

client = mqtt.Client()

# Kết nối tới broker MQTT
client.connect(broker, port, 60)

# Lấy thời gian hiện tại
def get_current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# API gửi trạng thái MQTT
def send_mqtt_message(status):
    global current_status, current_time
    current_status = status  # Cập nhật trạng thái hiện tại
    current_time = get_current_time()  # Cập nhật thời gian hiện tại
    data = {
        "date": current_time.split()[0],
        "time": current_time.split()[1],
        "Tốc độ động cơ":"0%",
        "status": status  # 0: tắt, 1: bật
    }
    client.publish(topic, json.dumps(data))

# API để lấy trạng thái động cơ
@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"status": current_status, "time": current_time})

# Trang chủ, hiển thị giao diện điều khiển động cơ
@app.route('/')
def index():
    return render_template('index.html')

# API để thay đổi trạng thái động cơ
@app.route('/control_motor/<status>', methods=['GET'])
def control_motor(status):
    send_mqtt_message(status)
    return jsonify({"status": "success", "message": "Motor state updated"})

# Hàm cập nhật trạng thái động cơ liên tục
def update_status_periodically():
    while True:
        time.sleep(1)  # Mỗi giây kiểm tra và cập nhật trạng thái
        # Gửi lại trạng thái cho tất cả client
        client.loop()  # Giữ MQTT hoạt động liên tục

# Chạy thread để cập nhật trạng thái động cơ liên tục
thread = threading.Thread(target=update_status_periodically)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# MQTT_DongCo_DCs = {"date":"01/01/1970","time":"07:02:14","Tốc độ động cơ":"0%","status":"0"}