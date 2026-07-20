from abc import abstractmethod

class Remote():
    def __init__(self, command: "Command"):
        self.command = command
    def execute(self):
        self.command.execute()

class Command():
    def __init__(self, device: "Device"):
        self.device = device
    @abstractmethod
    def execute(self):
        pass

class CommandOn(Command):
    def execute(self):
        self.device.on_step1()
        self.device.on_step2()

class CommandOff(Command):
    def execute(self):
        self.device.off_step1()
        self.device.off_step2()

class Device():
    @abstractmethod
    def on_step1(self):
        pass
    @abstractmethod
    def on_step2(self):
        pass
    @abstractmethod
    def off_step1(self):
        pass
    @abstractmethod
    def off_step2(self):
        pass

class Light(Device):
    def on_step1(self):
        print("Light is on 1")
    def on_step2(self):
        print("Light is on 2")
    def off_step1(self):
        print("Light is off 1")
    def off_step2(self):
        print("Light is off 2")

class Fan(Device):
    def on_step1(self):
        print("Fan is on 1")
    def on_step2(self):
        print("Fan is on 2")
    def off_step1(self):
        print("Fan is off 1")
    def off_step2(self):
        print("Fan is off 2")

if __name__ == "__main__":
    light = Light()
    fan =  Fan()
    command = CommandOn(light)
    command.execute()
    command = CommandOn(fan)
    command.execute()
