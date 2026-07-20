"""
Definition: A behavioral design pattern where an object (the "subject") maintains a list of dependents (the "observers") and automatically notifies them of any state changes, usually by calling a method on each.

Use case: When multiple objects need to react to changes in another object without tight coupling — e.g., event systems, GUI widgets reacting to data changes, pub/sub messaging, stock price tickers, logging/monitoring hooks.
"""

from abc import ABC, abstractmethod
from typing import List


class Subscriber(ABC):
    @abstractmethod
    def consume(self):
        pass

class EmailSubscriber(Subscriber):
    def consume(self):
        print("Email sent")

class SMSSubscriber(Subscriber):
    def consume(self):
        print("SMS sent")


class Publisher():
    def __init__(self):
        self.subscribers: List[Subscriber] = []
    def subscribe(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)
    def produce(self):
        for subscriber in self.subscribers:
            subscriber.consume()

if __name__ == "__main__":
    subscriber1 = EmailSubscriber()
    subscriber2 = SMSSubscriber()
    producer = Publisher()
    producer.subscribe(subscriber1)
    producer.subscribe(subscriber2)
    producer.produce()