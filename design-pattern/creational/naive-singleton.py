"""
Definition: Singleton Pattern: One Object of an Class in one Runtime
Use cases: Configuration managers, Database connection pools, Logging services etc., Best for stateless beans
Types:
Thread Unsafe Singleton
Thread Safe Singleton
"""
class SingletonMeta(type):
    __instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super().__call__(*args, **kwargs)
        return cls.__instance[cls]

class Singletone():
    def some_business_logic(self):
        pass

if __name__ == "__main__":
    s1 = Singletone()
    s1 = Singletone()
    print(s1 is s1)


"""
More Pyhtonic Way of Singleton:

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)
        print(f"LOG: {message}")


# Usage
logger1 = Logger()
logger2 = Logger()

logger1.log("App started")
print(logger1 is logger2)   # True
print(logger2.logs)         # ["App started"] — shared state
"""