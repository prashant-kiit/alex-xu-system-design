"""
Definition: A behavioral design pattern that passes a request along a chain of handlers, where each handler decides either to process the request or pass it to the next handler in the chain. Decouples the sender of a request from its receivers.
Use case: When multiple objects might handle a request but the exact handler isn't known in advance — e.g., middleware pipelines, request validation layers, logging levels (DEBUG/INFO/ERROR), approval workflows (manager → director → VP for expense approvals), event bubbling in GUIs.
"""

from abc import abstractmethod


class Approver:
    def __init__(self):
        self.next_approver = DefaultApprover()

    def set_next_approver(self, next_approver: "Approver"):
        self.next_approver = next_approver
        return self

    @abstractmethod
    def approve(self, amount):
        pass


class DefaultApprover(Approver):
    def __init__(self):
        self.next_approver = None

    def approve(self, amount):
        print("Default approved")


class Manager(Approver):
    def approve(self, amount):
        if amount <= 500:
            print("Manager approved")
        else:
            self.next_approver.approve(amount)


class Director(Approver):
    def approve(self, amount):
        if amount <= 1000:
            print("Director approved")
        else:
            self.next_approver.approve(amount)


class VP(Approver):
    def approve(self, amount):
        if amount <= 5000:
            print("VP approved")
        else:
            self.next_approver.approve(amount)


if __name__ == "__main__":
    manager = Manager()
    director = Director()
    vp = VP()
    manager.set_next_approver(director).set_next_approver(vp)
    manager.approve(4000)
