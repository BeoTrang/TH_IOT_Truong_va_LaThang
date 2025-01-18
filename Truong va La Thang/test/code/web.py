from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt
import threading

app = Flask(__name__)

broker = "nekotrang.duckdns.org"
port = 1883
topic = "home/esp8266"  # MQTT topic chung

# Biến toàn cục lưu dữ liệu cảm biến
sensor_data = "Chưa có dữ liệu"

# Callback khi nhận dữ liệu MQTT
def on_message(client, userdata, msg):
    global sensor_data
    sensor_data = msg.payload.decode()

# Cấu hình MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

def start_mqtt():
    mqtt_client.connect(broker, port, 60)
    mqtt_client.subscribe(topic)
    mqtt_client.loop_forever()

# API trả dữ liệu cảm biến cho AJAX
@app.route('/api/sensor', methods=['GET'])
def get_sensor_data():
    global sensor_data
    return jsonify({"data": sensor_data})

# Trang chính
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Chạy MQTT trong thread riêng
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    # Chạy Flask
    app.run(host='0.0.0.0', port=5000)
