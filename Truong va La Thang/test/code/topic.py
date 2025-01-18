import paho.mqtt.client as mqtt

# Callback khi kết nối thành công với broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Kết nối MQTT thành công!")
        # Subscribe vào topic mà Node-RED đang xuất dữ liệu
        client.subscribe("truonglathang")
    else:
        print("Kết nối thất bại. Mã lỗi:", rc)

# Callback khi nhận được dữ liệu từ topic
def on_message(client, userdata, msg):
    print(f"Nhận được dữ liệu từ topic '{msg.topic}': {msg.payload.decode()}")

# Tạo client MQTT
client = mqtt.Client()

# Đặt callback
client.on_connect = on_connect
client.on_message = on_message

# Kết nối tới MQTT Broker (thay 'localhost' bằng IP của Node-RED nếu cần)
broker = "192.168.0.103"  # Đổi thành IP hoặc hostname của broker nếu cần
port = 1883           # Cổng mặc định của MQTT là 1883
client.connect(broker, port, 60)

# Vòng lặp chờ dữ liệu
client.loop_forever()
