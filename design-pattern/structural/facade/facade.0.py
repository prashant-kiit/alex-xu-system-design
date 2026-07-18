"""
Definition: Provides a unified, simplified interface to a set of complex interfaces in a subsystem, making the subsystem easier to use by hiding its internal complexity from the client.
Use Case: You have a complex system with many interdependent classes (e.g., a home theater with a projector, sound system, lights, and streaming player), and you want to give clients a simple, single entry point instead of forcing them to understand and coordinate every subsystem class themselves.
"""

# Complex subsystem classes
class Projector:
    def on(self):
        print("Projector: turning on")
    
    def set_input(self, source):
        print(f"Projector: setting input to {source}")
    
    def off(self):
        print("Projector: turning off")


class SoundSystem:
    def on(self):
        print("Sound System: turning on")
    
    def set_volume(self, level):
        print(f"Sound System: setting volume to {level}")
    
    def off(self):
        print("Sound System: turning off")


class StreamingPlayer:
    def on(self):
        print("Streaming Player: turning on")
    
    def play(self, movie):
        print(f"Streaming Player: playing '{movie}'")
    
    def stop(self):
        print("Streaming Player: stopping")


class Lights:
    def dim(self, level):
        print(f"Lights: dimming to {level}%")
    
    def on(self):
        print("Lights: turning on")


# Facade - simplified interface hiding subsystem complexity
class HomeTheaterFacade:
    def __init__(self):
        self.projector = Projector()
        self.sound = SoundSystem()
        self.player = StreamingPlayer()
        self.lights = Lights()
    
    def watch_movie(self, movie):
        print("--- Getting ready to watch a movie ---")
        self.lights.dim(10)
        self.projector.on()
        self.projector.set_input("Streaming Player")
        self.sound.on()
        self.sound.set_volume(15)
        self.player.on()
        self.player.play(movie)
    
    def end_movie(self):
        print("--- Shutting down home theater ---")
        self.player.stop()
        self.sound.off()
        self.projector.off()
        self.lights.on()


# Usage - client interacts only with the facade
theater = HomeTheaterFacade()
theater.watch_movie("Inception")
print()
theater.end_movie()