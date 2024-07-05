import threading
import queue

class Topic:
    def __init__(self) -> None:
        self.subscribers = []
        self.messages = queue.Queue()
        self.new_message_event = threading.Event()
        self.subscribers_lock = threading.Lock()
    
    def publish(self, message, publisher_name):
        self.messages.put((message, publisher_name))
        self.new_message_event.set()

    def subscribe(self, subscriber):
        with self.subscribers_lock:
            self.subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber):
        with self.subscribers_lock:
            self.subscribers.remove(subscriber)


class Subscriber(threading.Thread):
    def __init__(self, name, topic) -> None:
        super().__init__()
        self.name = name
        self.topic = topic
        self.last_message_index = -1
    
    def run(self):
        while True:
            self.topic.new_message_event.wait()
            while self.last_message_index < self.topic.messages.qsize() - 1:
                self.last_message_index += 1
                message, publisher_name = self.topic.messages.queue[self.last_message_index]
                print(f"Subscriber {self.name} received message from {publisher_name}: {message}")
            self.topic.new_message_event.clear()

class PubSubSystem:
    def __init__(self):
        self.topics = {}

    def create_topic(self, topic_name):
        if topic_name not in self.topics:
            self.topics[topic_name] = Topic()

    def publish(self, topic_name, message, publisher_name):
        if topic_name in self.topics:
            self.topics[topic_name].publish(message, publisher_name)
        else:
            print("Topic does not exist")

    def subscribe(self, topic_name, subscriber_name):
        if topic_name in self.topics:
            subscriber = Subscriber(subscriber_name, self.topics[topic_name])
            self.topics[topic_name].subscribe(subscriber)
            subscriber.start()
        else:
            print("Topic does not exist")

# Example usage
pub_sub_system = PubSubSystem()

pub_sub_system.create_topic("topic1")
pub_sub_system.create_topic("topic2")

pub_sub_system.publish("topic1", "Message 1", "Publisher A")
pub_sub_system.publish("topic1", "Message 2", "Publisher B")

pub_sub_system.subscribe("topic1", "Subscriber X")
pub_sub_system.subscribe("topic1", "Subscriber Y")

pub_sub_system.publish("topic1", "Message 3", "Publisher C")

pub_sub_system.publish("topic2", "Message 5", "Publisher C")
pub_sub_system.publish("topic2", "Message 6", "Publisher D")

pub_sub_system.subscribe("topic2", "Subscriber L")
pub_sub_system.subscribe("topic2", "Subscriber M")

pub_sub_system.publish("topic2", "Message 7", "Publisher C")
pub_sub_system.publish("topic2", "Message 8", "Publisher D")