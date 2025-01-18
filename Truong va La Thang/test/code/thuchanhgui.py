import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json  # Thư viện xử lý JSON

# Thông tin MQTT Broker
broker = "192.168.0.103"
port = 1883
topic = "truonglathang"

# Tạo client MQTT
client = mqtt.Client()

# Kết nối đến MQTT Broker
client.connect(broker, port, 60)

print("Bắt đầu gửi dữ liệu thời gian thực dưới dạng JSON...")
try:
    while True:
        # Lấy thời gian hiện tại
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Chuỗi bổ sung
        additional_string = "25: Nhan dang khuon mat, 28: Nhan dang bien so"

        # Tạo dữ liệu JSON
        data = {
            "time": current_time,
            "string": additional_string
        }

        # Chuyển đổi dữ liệu sang JSON
        json_message = json.dumps(data)

        # Gửi dữ liệu JSON
        client.publish(topic, json_message)
        print(f"Đã gửi: {json_message}")

        # Gửi mỗi giây
        time.sleep(1)
except KeyboardInterrupt:
    print("Dừng gửi dữ liệu.")
finally:
    client.disconnect()
    print("Publisher đã ngắt kết nối.")