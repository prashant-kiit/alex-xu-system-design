from abc import abstractmethod


class Remote:
    def __init__(self, command: "Command"):
        self.command = command

    def execute(self):
        self.command.execute()


class Command:
    def __init__(self, device: "Device"):
        self.device = device

    @abstractmethod
    def execute(self):
        pass


class CommandOn(Command):
    def execute(self):
        self.device.on()


class CommandOff(Command):
    def execute(self):
        self.device.off()


class Device:
    @classmethod
    def register_step(cls, command, step_order):
        def my_wrapper(func):
            if "command_map" not in cls.__dict__:
                cls.command_map = {}
            steps = cls.command_map.setdefault(command, [])
            if len(steps) <= step_order:
                steps.extend([None] * (step_order + 1 - len(steps)))
            steps[step_order] = func
            return func
        return my_wrapper

    def _run_steps(self, command):
        for step in self.command_map.get(command, []):
            step()

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass


class Light(Device):
    def on(self):
        self._run_steps("ON")

    def off(self):
        self._run_steps("OFF")


class Fan(Device):
    def on(self):
        self._run_steps("ON")

    def off(self):
        self._run_steps("OFF")


@Light.register_step("ON", 0)
def light_on_step_1():
    print("Light is on 1")


@Light.register_step("ON", 1)
def light_on_step_2():
    print("Light is on 2")


@Light.register_step("OFF", 0)
def light_off_step_1():
    print("Light is off 1")


@Light.register_step("OFF", 1)
def light_off_step_2():
    print("Light is off 2")


@Fan.register_step("ON", 0)
def fan_on_step_1():
    print("Fan is on 1")


@Fan.register_step("ON", 1)
def fan_on_step_2():
    print("Fan is on 2")


@Fan.register_step("OFF", 0)
def fan_off_step_1():
    print("Fan is off 1")


@Fan.register_step("OFF", 1)
def fan_off_step_2():
    print("Fan is off 2")


if __name__ == "__main__":
    light = Light()
    fan = Fan()
    command = CommandOn(light)
    command.execute()
    command = CommandOn(fan)
    command.execute()
