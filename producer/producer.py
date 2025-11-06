from kafka import KafkaProducer
import json
import time
import random

# Kafka Producer with your broker IP
producer = KafkaProducer(
    bootstrap_servers=["10.244.224.169:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Topics your producer will publish to
topics = ["sports", "news", "finance", "tech"]

print(" Producer started... Sending messages...")

while True:
    topic = random.choice(topics)
    
    message = {
        "topic": topic,
        "content": f"Live {topic} update for streaming system",
        "timestamp": time.time()
    }
    
    producer.send(topic, value=message)
    producer.flush()
    
    print(f" Sent to {topic}: {message}")

    time.sleep(1)  
