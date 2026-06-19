import json
from kafka import KafkaProducer
from code.config import KAFKA_SERVER, KAFKA_TOPIC

producer = KafkaProducer( #kafka connection
    bootstrap_servers=KAFKA_SERVER, #localhost
    value_serializer=lambda data: json.dumps(data).encode("utf-8"), #into bytes
    key_serializer=lambda k: str(k).encode("utf-8") if k else None, #converts key to bytes
    acks="all",
    retries=5 #retry
)

def send_observation(data):
    if data is None:
        return

    producer.send(
        KAFKA_TOPIC,
        value=data
    )

    producer.flush()

if __name__ == "__main__":
    test = {
        "species": "Parus major",
        "latitude": 45.815,
        "longitude": 15.981,
        "confidence": 0.92
    }

    send_observation(test)