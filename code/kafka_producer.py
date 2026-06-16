import json
from kafka import KafkaProducer
from code.config import KAFKA_SERVER, KAFKA_TOPIC

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_observation(data):
    producer.send(KAFKA_TOPIC, data)
    producer.flush()

if __name__ == "__main__":
    test = {
        "species": "Parus major",
        "location": "Zagreb",
        "confidence": 0.92
    }

    send_observation(test)