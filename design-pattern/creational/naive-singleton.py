"""
Definition: Singleton Pattern: One Object of an Class in one Runtime
Use cases: Configuration managers, Database connection pools, Logging services etc.
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