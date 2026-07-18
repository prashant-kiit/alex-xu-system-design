"""
Definiton: step-by-step construction process can produce different configurations of that object.
Use cases: 
- Objects with many optional parameters
- Immutability
- Step-by-step construction with validation 
- Different representations from the same process - a MealBuilder could construct a "kids meal" or a "combo meal" using the same underlying build steps but different values.
"""

class Pizza:
    def __init__(self, size, crust, cheese, toppings, sauce):
        self.size = size
        self.crust = crust
        self.cheese = cheese
        self.toppings = toppings
        self.sauce = sauce

    def __str__(self):
        return (f"{self.size} {self.crust}-crust pizza with {self.cheese} cheese, "
                f"{self.sauce} sauce, and toppings: {', '.join(self.toppings) or 'none'}")


class PizzaBuilder:
    def __init__(self):
        # sensible defaults
        self._size = "medium"
        self._crust = "regular"
        self._cheese = "mozzarella"
        self._toppings = []
        self._sauce = "tomato"

    def set_size(self, size):
        self._size = size
        return self  # enables chaining

    def set_crust(self, crust):
        self._crust = crust
        return self

    def set_cheese(self, cheese):
        self._cheese = cheese
        return self

    def add_topping(self, topping):
        self._toppings.append(topping)
        return self

    def set_sauce(self, sauce):
        self._sauce = sauce
        return self

    def build(self) -> Pizza:
        return Pizza(self._size, self._crust, self._cheese, self._toppings, self._sauce)


# Usage — fluent, readable, and only sets what you actually care about
pizza = (
    PizzaBuilder()
    .set_size("large")
    .set_crust("thin")
    .add_topping("mushrooms")
    .add_topping("olives")
    .build()
)

print(pizza)
# large thin-crust pizza with mozzarella cheese, tomato sauce, and toppings: mushrooms, olives

# A second, completely different pizza — same builder API, no giant constructor call
simple_pizza = PizzaBuilder().build()
print(simple_pizza)
# medium regular-crust pizza with mozzarella cheese, tomato sauce, and toppings: none