"""
Definiton: step-by-step construction process can produce different configurations of that object.
Use cases: 
- Objects with many optional parameters
- Immutability
- Step-by-step construction with validation 
- Different representations from the same process - a MealBuilder could construct a "kids meal" or a "combo meal" using the same underlying build steps but different values.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Pizza:
    size: str = "medium"
    crust: str = "regular"
    cheese: str = "mozzarella"
    sauce: str = "tomato"
    toppings: List[str] = field(default_factory=list) # self.toppings = toppings if toppings is not None else []

pizza = Pizza(size="large", crust="thin", toppings=["mushrooms", "olives"])