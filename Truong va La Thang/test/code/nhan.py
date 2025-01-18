import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Kết nối MQTT thành công!")
        client.subscribe("truong/lathang")
    else:
        print("Kết nối thất bại. Mã lỗi:", rc)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        time = data.get("time")
        string = data.get("string")

        print(f"Nhận được dữ liệu từ topic '{msg.topic}':")
        print(f"  - Time: {time}")
        print(f"  - String: {string}")
    except json.JSONDecodeError as e:
        print("Lỗi phân tích JSON:", e)
    except Exception as e:
        print("Lỗi khác:", e)


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message


broker = "192.168.0.103"
port = 1883
client.connect(broker, port, 60)

client.loop_forever()
