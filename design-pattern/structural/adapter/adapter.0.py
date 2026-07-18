"""
Definition: Converts the interface of a class into another interface clients expect, allowing classes with incompatible interfaces to work together without modifying their source code.
Use Case: You have an existing class (often third-party or legacy) whose interface doesn't match what your code expects — e.g., integrating a new payment gateway library into a system built for a different API, without rewriting either side.
"""
from abc import ABC, abstractmethod

class IEuropeanSocket(ABC):
    @abstractmethod
    def voltage(self):
        pass

class EuropeanSocket(IEuropeanSocket):
    def voltage(self):
        return 200

class IUSASocket(ABC):
    @abstractmethod
    def voltage(self):
        pass

class USASocket(IUSASocket):
    def voltage(self):
        return 100

# adapts eurpoean socket to usa standard
class EuropeanToUSAdapter(IUSASocket):
    def __init__(self, european_socket: EuropeanSocket):
        self.european_socket = european_socket
        
    def voltage(self):
        return 100 if self.european_socket.voltage() > 100 else self.european_socket

class ElectricKettle:
    def __init__(self, power_source: IUSASocket):
        self.power_source = power_source
    
    def boil(self):
        if self.power_source.voltage() <= 110:
            print("Boiling water with US voltage...")
        else:
            print("Voltage too high, kettle would break!")

european_socket = EuropeanSocket()
usa_socket = USASocket()
europeanToUSAdapter = EuropeanToUSAdapter(european_socket)
kettle = ElectricKettle(europeanToUSAdapter)
kettle.boil()
