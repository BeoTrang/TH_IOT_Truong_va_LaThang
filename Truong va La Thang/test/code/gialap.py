import paho.mqtt.client as mqtt
import time
import random

# Kết nối tới MQTT Broker
broker_ip = "192.168.16.128"  # Địa chỉ IP của Raspberry Pi ảo
client = mqtt.Client()
client.connect(broker_ip, 1883, 60)

# Gửi dữ liệu giả lập
while True:
    temperature = random.uniform(20.0, 30.0)  # Nhiệt độ ngẫu nhiên
    humidity = random.uniform(40.0, 60.0)  # Độ ẩm ngẫu nhiên
    payload = f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%"
    client.publish("iot/dht22", payload)
    print(f"Gửi: {payload}")
    time.sleep(2)
