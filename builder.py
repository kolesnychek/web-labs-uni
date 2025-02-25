class Burger:
    def __init__(self):
        self.ingredients = []
    
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
    
    def show(self):
        print("Burger with:", ", ".join(self.ingredients))

class BurgerBuilder:
    def __init__(self):
        self.burger = Burger()
    
    def add_cheese(self):
        self.burger.add_ingredient("cheese")
        return self
    
    def add_lettuce(self):
        self.burger.add_ingredient("lettuce")
        return self
    
    def add_patty(self):
        self.burger.add_ingredient("beef patty")
        return self
    
    def build(self):
        return self.burger

burger = BurgerBuilder().add_patty().add_cheese().add_lettuce().build()
burger.show()