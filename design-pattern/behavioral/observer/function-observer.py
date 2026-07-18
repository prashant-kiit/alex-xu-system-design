from typing import Callable, List


def email_subscriber_consume():
    print("Email sent")

def sms_subscriber_consume():
    print("SMS sent")


class Publisher():
    def __init__(self):
        self.subscriber_consume: List[Callable[[], None]] = []
    def subscribe(self, subscriber_consume: Callable[[], None]):
        self.subscriber_consume.append(subscriber_consume)
    def produce(self):
        for subscriber_consume in self.subscriber_consume:
            subscriber_consume()

if __name__ == "__main__":
    producer = Publisher()
    producer.subscribe(email_subscriber_consume)
    producer.subscribe(sms_subscriber_consume)
    producer.produce()