import abc
class Pizza(object):

    def __init__(self, toppings):
        self.toppings = toppings
        for b in self.toppings:
            assert isinstance (b,Topping), "bogus"
            
    def show_topping_names(self):
        def get_name(t):
            return t.get_name()
        print("topping names = {}".format(set([get_name(t) for t in self.toppings])))
        print()

    def show_topping_types(self):
        def get_type(t):
             return t.get_type()
        print("topping types = {}".format(set([get_type(t) for t in self.toppings])))
        print()

    def __eq__(self, other): return isinstance(other,Pizza) and self.toppings == other.toppings

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
       
class Topping ():  
    @abc.abstractmethod
    def __init__(self,name,type):
        self.name = name
        self.type = type
        
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

    def __repr__(self):
        return object.__name__

    def __eq__(self, other): return isinstance(other,Topping) and self.name == other.name and self.type == other.type
  
    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

class CheeseTopping(Topping):
    @abc.abstractmethod 
    def __init__(self,topName):
        super().__init__(topName,'cheese')

class MeatTopping(Topping):
    @abc.abstractmethod
    def __init__(self,topName):
        super().__init__(topName,'meat')

class VegetableTopping(Topping):
    @abc.abstractmethod
    def __init__(self,topName):
        super().__init__(topName,'vegetable')

class Provolone(CheeseTopping):
    def __init__(self):
        super().__init__('provolone')

class Chicken(MeatTopping):
    def __init__(self):
        super().__init__('chicken')

class RedPepper(VegetableTopping):
    def __init__(self):
        super().__init__('red pepper')

class HorseFeathers():
    def get_name(self):
        return 'horsefeather'

    def get_type(self):
        return 'piffle'
        
provolone = Provolone()
chicken = Chicken()
red_pepper = RedPepper()
horsefeather = HorseFeathers()
piffle = HorseFeathers()
cheese = CheeseTopping('provolone')
meat = MeatTopping('chicken')
vegetable = VegetableTopping('red pepper')

typelst = [meat, vegetable, cheese]
namelst = [provolone, chicken, red_pepper]

PizzaTOP = Pizza(typelst)
PizzaTYP = Pizza(namelst)

showTop2 = PizzaTOP.show_topping_names()
showType2 = PizzaTYP.show_topping_types()

nameP1 = [provolone, red_pepper]
nameP2 = [chicken, provolone]
pizza1 = Pizza(nameP1)
pizza2 = Pizza(nameP2)

EqualNotEqual = nameP1.__eq__(nameP2)
print('Is pizza one equal to pizza two?', EqualNotEqual)
print()

print(Pizza.__repr__(provolone))
print(Pizza.__repr__(chicken))





