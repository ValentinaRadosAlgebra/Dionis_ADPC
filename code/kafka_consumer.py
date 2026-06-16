from kafka import KafkaConsumer
import json
from pathlib import Path
from code.clients import insert, find
from code.config import KAFKA_TOPIC, KAFKA_SERVER


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=10000
)


def run():
    count = 0

    try:
        for msg in consumer:
            if msg is None:
                continue

            insert("observations", msg.value)
            count += 1

    except Exception as e:
        print(f"Kafka error: {e}")

    finally:
        consumer.close()

    Path("output/kafka.done").touch()
    print(f"Kafka done ({count} messages)")


if __name__ == "__main__":
    run()