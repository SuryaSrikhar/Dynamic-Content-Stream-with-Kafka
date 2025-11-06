from kafka import KafkaConsumer
import json
import time
import threading
import requests

KAFKA_SERVER = "10.244.224.169"
ADMIN_API = "http://10.244.246.253:5000"

consumer = None
subscribed_topics = set()

def get_active_topics():
    try:
        resp = requests.get(f"{ADMIN_API}/topics").json()
        return {t["name"] for t in resp if t["status"] == "active"}
    except:
        return set()

def subscribe_to_changes():
    global consumer, subscribed_topics
    while True:
        active = get_active_topics()
        if active != subscribed_topics:
            subscribed_topics = active
            if consumer:
                consumer.unsubscribe()
            if active:
                consumer = KafkaConsumer(
                    *active,
                    bootstrap_servers=KAFKA_SERVER,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='latest'
                )
        time.sleep(3)

def consume_messages():
    global consumer
    while True:
        if consumer:
            records = consumer.poll(timeout_ms=500)
            for messages in records.values():
                for msg in messages:
                    print(f"[{msg.topic}] {msg.value}")
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=subscribe_to_changes, daemon=True).start()
    consume_messages()

