class MyMainClass:
  def __init__(self, **kwargs):   
      if len(set(['v1']) & set(kwargs.keys())) != 1:
        raise KeyError('v1 must be defined')
      self.set_instance_value_1( kwargs['v1'] ) 

  def set_instance_value_1(self, v):       
      self.instance_value_1 = 'set from MyMainClass: ' + v

  def get_instance_value_1(self):       
      return self.instance_value_1

class MyMixinClass:
  def __init__(self, **kwargs):   
      if len(set(['v2']) & set(kwargs.keys())) != 1:
        raise KeyError('v2 must be defined')
      self.set_instance_value_2( kwargs['v2'] )
  
  def set_instance_value_2(self, v):    
      self.instance_value_2 = 'set from MyMixinClass: ' + v

  def get_instance_value_2(self):       
      return self.instance_value_2

# - - - simpler here, I think, to name the classes then to refer to super(),
# - - - which would change if the order of inheritance is varied

class MySubclass(MyMainClass, MyMixinClass):  
  def __init__(self,**kwargs):
    for baseClass in MySubclass.__bases__:
      baseClass.__init__(self,**kwargs)

my_subclass_instance = MySubclass(v1 = 'one', v2 = 'two')
print(my_subclass_instance.get_instance_value_1())   # from MyClass
print(my_subclass_instance.get_instance_value_2())   # from MyMixinClass
