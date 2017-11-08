from abc import ABCMeta, abstractmethod

class Pizza(object):
    def __init__(self, toppings):
        self.toppings = toppings
        for t in self.toppings:
            assert isinstance(t,Topping), "bogus"
    def show_topping_names(self):
        def get_name(t):
            return t.get_name()
        print("toppings = ", end='')
        for t in self.toppings[:-1]:  print(get_name(t), ",", sep="", end="")
        print(get_name(self.toppings[-1]))
    def show_topping_types(self):
        def get_type(t):
             return t.get_type()
        print("topping types = {}".format(set([get_type(t) for t in self.toppings])))


class Topping ():
    __metaclass__=ABCMeta
    
    @abstractmethod
    def __init__(self,name,type):
        self.name=name
        self.type=type
        
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type


class CheeseTopping(Topping):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,topName):
        super().__init__(topName,'cheese')

class MeatTopping(Topping):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,topName):
        super().__init__(topName,'meat')

class VegetableTopping(Topping):
    __metaclass__ = ABCMeta

    @abstractmethod
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
        return 'horesefeathers'

    def get_type(self):
        return 'piffle'
        


