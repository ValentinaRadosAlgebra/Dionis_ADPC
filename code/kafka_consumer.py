# from kafka import KafkaConsumer
# import json
# from pathlib import Path
# from code.clients import insert, find
# from code.config import KAFKA_TOPIC, KAFKA_SERVER

# # Number of expected files (used only as a hint, not strict requirement)
# expected = len(find("files"))

# # Safety fallback (prevents Kafka crash)
# if expected <= 0:
#     expected = 1

# consumer = KafkaConsumer(
#     KAFKA_TOPIC,
#     bootstrap_servers=KAFKA_SERVER,
#     value_deserializer=lambda x: json.loads(x.decode("utf-8")),
#     auto_offset_reset="earliest",
#     enable_auto_commit=True,
#     consumer_timeout_ms=10000
# )


# def run():
#     count = 0

#     try:
#         while True:
#             messages = consumer.poll(timeout_ms=5000, max_records=10)

#             if not messages:
#                 # No more messages available → stop safely
#                 break

#             for tp, msgs in messages.items():
#                 for msg in msgs:
#                     insert("observations", msg.value)
#                     count += 1

#     except Exception as e:
#         print(f"Kafka consumer error: {e}")

#     finally:
#         consumer.close()

#     Path("output/kafka.done").touch()
#     print("Kafka done")


# if __name__ == "__main__":
#     run()

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