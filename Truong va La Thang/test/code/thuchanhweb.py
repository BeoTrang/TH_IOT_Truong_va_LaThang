from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import threading

app = Flask(__name__)

# MQTT Broker thông tin
broker = "192.168.0.103"
port = 1883
topic = "truonglathang"

# Biến toàn cục để lưu dữ liệu mới nhất
latest_data = None  # Biến này sẽ chứa dữ liệu mới nhất


# Hàm callback khi nhận được tin nhắn từ topic
def on_message(client, userdata, msg):
    global latest_data
    try:
        # Decode và xử lý payload
        payload = msg.payload.decode()
        data = json.loads(payload)

        # Tách các giá trị từ JSON
        time_received = data.get("time")
        string_received = data.get("string")

        # Cập nhật dữ liệu mới nhất
        latest_data = {
            "time": time_received,
            "string": string_received
        }

        print(f"Nhận được từ MQTT: Time: {time_received}, String: {string_received}")
    except Exception as e:
        print(f"Lỗi xử lý MQTT message: {e}")



# Hàm callback khi mất kết nối
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("MQTT kết nối bị mất. Thử kết nối lại...")
        client.reconnect()  # Tự động kết nối lại


# Hàm khởi động MQTT client
def start_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect  # Đăng ký callback on_disconnect
    mqtt_client.connect(broker, port, 60)
    mqtt_client.subscribe(topic)
    mqtt_client.loop_forever()


# Route chính
@app.route("/", methods=["GET", "POST"])
def index():
    global latest_data
    if request.method == "POST":
        # Lấy dữ liệu từ form
        custom_string = request.form.get("custom_string")
        if custom_string:
            # Nếu chưa có dữ liệu trước đó, tạo thời gian mới
            if latest_data is None:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                latest_data = {
                    "time": current_time,
                    "string": custom_string
                }
            else:
                # Cập nhật chuỗi mà giữ nguyên thời gian
                latest_data['string'] = custom_string

            # Gửi dữ liệu qua MQTT
            json_message = json.dumps(latest_data)
            mqtt_client.publish(topic, json_message)
            print(f"Đã gửi: {json_message}")

    return render_template("index.html", latest_data=latest_data)


# API để trả về dữ liệu nhận (chỉ trả về dữ liệu mới nhất)
@app.route("/get_received_data", methods=["GET"])
def get_received_data():
    global latest_data
    return jsonify(latest_data if latest_data else {})


if __name__ == "__main__":
    # Khởi động MQTT trong luồng riêng
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    # Tạo MQTT client cho Flask
    mqtt_client = mqtt.Client()
    mqtt_client.on_disconnect = on_disconnect  # Đăng ký callback on_disconnect
    mqtt_client.connect(broker, port, 60)

    # Chạy Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
