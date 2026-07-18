"""
Definition: Decouples an abstraction from its implementation so that both can vary independently, without one being tightly bound to the other. Instead of a rigid inheritance hierarchy, it uses composition — the abstraction holds a reference to an implementation object.
Use Case: You have multiple variants of an abstraction (e.g., shapes) and multiple variants of implementation (e.g., rendering engines), and you want to mix-and-match them without an explosion of subclasses (e.g., CircleOpenGL, CircleDirectX, SquareOpenGL, SquareDirectX...). Common in GUI toolkits, device drivers, and rendering systems.
"""

from abc import ABC, abstractmethod

# Implementation hierarchy (the "platform" side)
class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius):
        pass


class VectorRenderer(Renderer):
    def render_circle(self, radius):
        print(f"Drawing a circle with vector math, radius {radius}")


class RasterRenderer(Renderer):
    def render_circle(self, radius):
        print(f"Drawing pixels for a circle, radius {radius}")


# Abstraction hierarchy (the "shape" side)
class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer  # bridge to implementation
    
    @abstractmethod
    def draw(self):
        pass


class Circle(Shape):
    def __init__(self, renderer: Renderer, radius):
        super().__init__(renderer)
        self.radius = radius
    
    def draw(self):
        self.renderer.render_circle(self.radius)
    
    def resize(self, factor):
        self.radius *= factor


# Usage - mix and match shapes with renderers independently
vector_circle = Circle(VectorRenderer(), radius=5)
raster_circle = Circle(RasterRenderer(), radius=5)

vector_circle.draw()  # Drawing a circle with vector math, radius 5
raster_circle.draw()  # Drawing pixels for a circle, radius 5

vector_circle.resize(2)
vector_circle.draw()  # Drawing a circle with vector math, radius 10