"""
Definition: Singleton Pattern: One Object of an Class in one Runtime
Use cases: Configuration managers, Database connection pools, Logging services etc., Best for stateless beans
Types:
Thread Unsafe Singleton
Thread Safe Singleton
"""
from threading import Lock, Thread

class SingletonMeta(type):
    __instance = {}
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:    
            if cls not in cls.__instance:
                cls.__instance[cls] = super().__call__(*args, **kwargs)
        return cls.__instance[cls]

class Singletone():
    def __init__(self, value):
        self.value = value
    
    def some_business_logic(self):
        pass

def create_singleton(value):
    s = Singletone(value)
    print(s.value)

if __name__ == "__main__":
    process1 = Thread(target=create_singleton, args=("ABC",))
    process2 = Thread(target=create_singleton, args=("PQR",))
    process1.start()
    process2.start()