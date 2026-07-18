"""
Definition: Provides a surrogate or placeholder object that controls access to another object, allowing you to perform additional actions (like lazy loading, access control, caching, or logging) before or after the request reaches the real object — without the client knowing the difference.
Use Case: You want to control access to an expensive or sensitive resource — e.g., lazily loading a large image only when it's actually displayed, restricting access based on user permissions, or caching results of costly operations — while keeping the client code interacting with the same interface as the real object.
"""

from abc import ABC, abstractmethod

# Common interface
class Image(ABC):
    @abstractmethod
    def display(self):
        pass


# Real subject - expensive to create
class RealImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self._load_from_disk()
    
    def _load_from_disk(self):
        print(f"Loading {self.filename} from disk... (expensive operation)")
    
    def display(self):
        print(f"Displaying {self.filename}")


# Proxy - controls access, delays creation until needed
class ImageProxy(Image):
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None  # not loaded yet
    
    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)  # lazy load
        self._real_image.display()


# Usage
print("Creating proxy objects (no loading happens yet)...")
image1 = ImageProxy("vacation.jpg")
image2 = ImageProxy("mountains.png")

print("\nDisplaying image1 for the first time:")
image1.display()  # triggers loading + display

print("\nDisplaying image1 again:")
image1.display()  # already loaded, just displays

print("\nimage2 was never displayed, so it was never loaded.")