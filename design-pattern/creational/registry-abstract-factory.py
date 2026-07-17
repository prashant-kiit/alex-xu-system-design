"""
Definition: Where a regular Factory produces one type of object, an Abstract Factory produces a set of related objects that are designed to work together
Use Case: 
- Same as Factory pattern
- Isolating client code from concrete classes
- Swapping entire product families at once
"""

from abc import ABC, abstractmethod

class Memory(ABC):
    @abstractmethod
    def store(self):
        pass

class Process(ABC):
    @abstractmethod
    def execute(self):
        pass

class WindowsMemory(Memory):
    def store(self):
        print("Windows stores")

class WindowsProcess(Process):
    def execute(self):
        print("Windows executes")

class MacMemory(Memory):
    def store(self):
        print("Mac stores")

class MacProcess(Process):
    def execute(self):
        print("Mac executes")

class OS(ABC):
    @abstractmethod
    def create_memory():
        pass

    @abstractmethod
    def create_process():
        pass

class OSFactory():
    __instance = {}

    @classmethod
    def register(cls, os_type):
        def wrapper(os_cls):
            cls.__instance[os_type] = os_cls
        return wrapper

    @classmethod
    def get_os(cls, os_type):
        os_cls = cls.__instance.get(os_type)
        if os_cls is not None:
            return os_cls()
        else:
            raise Exception("Invalid os type")

@OSFactory.register("windows")
class WindowsOS(OS):
    def create_memory(self):
        return WindowsMemory()

    def create_process(self):
        return WindowsProcess()

@OSFactory.register("mac")
class MacOS(OS):
    def create_memory(self):
        return MacMemory()

    def create_process(self):
        return MacProcess()

class Machine():
    def __init__(self, os):
        self.os = os
    def create(self):
        self.memory = self.os.create_memory()
        self.process = self.os.create_process()
        return self
    def run(self):
        self.memory.store()
        self.process.execute()
        return self

if __name__ == "__main__":
    machine = Machine(OSFactory.get_os("mac"))
    machine.create().run()