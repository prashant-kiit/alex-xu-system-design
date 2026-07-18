"""
Definition: Composes objects into tree structures to represent part-whole hierarchies, letting clients treat individual objects (leaves) and compositions of objects (composites) uniformly through a common interface.
Use Case: You need to represent hierarchical structures like file systems (files and folders), UI components (widgets containing widgets), or organization charts, where a client should be able to call the same operation on a single item or an entire group without caring which it is.
"""


from abc import ABC, abstractmethod

# Common interface for both leaves and composites
class FileSystemComponent(ABC):
    @abstractmethod
    def show_details(self, indent=0):
        pass
    
    @abstractmethod
    def get_size(self):
        pass


# Leaf: a single file, no children
class File(FileSystemComponent):
    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    def show_details(self, indent=0):
        print(" " * indent + f"📄 {self.name} ({self.size} KB)")
    
    def get_size(self):
        return self.size


# Composite: a folder that can contain files or other folders
class Folder(FileSystemComponent):
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add(self, component: FileSystemComponent):
        self.children.append(component)
    
    def remove(self, component: FileSystemComponent):
        self.children.remove(component)
    
    def show_details(self, indent=0):
        print(" " * indent + f"📁 {self.name}/")
        for child in self.children:
            child.show_details(indent + 2)
    
    def get_size(self):
        return sum(child.get_size() for child in self.children)


# Usage
root = Folder("root")
docs = Folder("docs")
docs.add(File("resume.pdf", 120))
docs.add(File("notes.txt", 5))

pics = Folder("pictures")
pics.add(File("vacation.jpg", 2500))

root.add(docs)
root.add(pics)
root.add(File("readme.md", 2))

root.show_details()
print(f"\nTotal size: {root.get_size()} KB")