"""
Definition: Minimizes memory usage by sharing as much data as possible with other similar objects. It separates an object's data into intrinsic state (shared, immutable, reusable across instances) and extrinsic state (unique, context-dependent, passed in by the client), storing only one copy of the intrinsic state for many logical instances.
Use Case: You need to create a huge number of similar objects that would otherwise consume excessive memory — e.g., rendering millions of trees in a forest simulation, characters in a text editor, or particles in a game — where most of the data (texture, color, font) is shared, and only position or other context varies per instance.
"""

# Flyweight - stores shared intrinsic state (immutable, reusable)
class TreeType:
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture  # imagine this is a large object
    
    def draw(self, x, y):
        print(f"Drawing {self.name} tree ({self.color}) at ({x}, {y})")


# Flyweight Factory - ensures TreeTypes are shared, not duplicated
class TreeTypeFactory:
    _tree_types = {}
    
    @classmethod
    def get_tree_type(cls, name, color, texture):
        key = (name, color, texture)
        if key not in cls._tree_types:
            print(f"Creating new TreeType object: {key}")
            cls._tree_types[key] = TreeType(name, color, texture)
        return cls._tree_types[key]
    
    @classmethod
    def total_types_created(cls):
        return len(cls._tree_types)


# Context - stores extrinsic state (unique per instance) + reference to flyweight
class Tree:
    def __init__(self, x, y, tree_type: TreeType):
        self.x = x           # extrinsic
        self.y = y            # extrinsic
        self.tree_type = tree_type  # shared flyweight reference
    
    def draw(self):
        self.tree_type.draw(self.x, self.y)


# Client - manages a forest of many trees
class Forest:
    def __init__(self):
        self.trees = []
    
    def plant_tree(self, x, y, name, color, texture):
        tree_type = TreeTypeFactory.get_tree_type(name, color, texture)
        self.trees.append(Tree(x, y, tree_type))
    
    def draw(self):
        for tree in self.trees:
            tree.draw()


# Usage
forest = Forest()
forest.plant_tree(1, 2, "Oak", "Green", "oak_texture.png")
forest.plant_tree(5, 8, "Oak", "Green", "oak_texture.png")   # reuses existing TreeType
forest.plant_tree(3, 3, "Pine", "Dark Green", "pine_texture.png")
forest.plant_tree(9, 1, "Oak", "Green", "oak_texture.png")   # reuses existing TreeType

forest.draw()
print(f"\nTotal Tree objects: {len(forest.trees)}")
print(f"Total TreeType objects actually created: {TreeTypeFactory.total_types_created()}")