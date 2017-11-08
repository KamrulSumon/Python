import abc

class Pizza(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, type):
        self.name = name
        self.type = type

class Topping ():
    @abc.abstractmethod
    def __init__(self,name,type):
        self.name=name
        self.type=type
        
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

class CheeseTopping(Topping):
    @abc.abstractmethod
    def __init__(self,name):
        super().__init__(name,'cheese')

class MeatTopping(Topping):  
    @abc.abstractmethod
    def __init__(self,name):
        super().__init__(name,'meat')

class VegetableTopping(Topping): 
    @abc.abstractmethod
    def __init__(self,name):
        super().__init__(name,'vegetable')

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

pizza = Pizza('provolone', 'cheese')
print('The house pizza has', pizza.name, 'which is a', pizza.type, 'type of pizza.')

strangepizza = Pizza('horsefeathers', 'piffle')
print('The strange pizza has', strangepizza.name, 'which is a', strangepizza.type, 'type of pizza.')


