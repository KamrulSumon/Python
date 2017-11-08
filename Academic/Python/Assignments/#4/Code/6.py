class MyMainClass:
  def __init__(self, v):    
      self.set_instance_value_1(v)
  
  def set_instance_value_1(self, v):    
      self.instance_value_1 = 'set from MyClass: ' + v

  def get_instance_value_1(self):       
      return self.instance_value_1

class MyMixinClass_1:
  def set_instance_value_2(self, v):    
      self.instance_value_2 = 'set from MyMixinClass_1: ' + v

  def get_instance_value_2(self):       
      return self.instance_value_2
  
  def set_instance_value_4(self, v):    
      self.instance_value_4 = 'set from MyMixinClass_1: ' + v
  def get_instance_value_4(self):       
      return self.instance_value_4

class MyMixinClass_2:
  def set_instance_value_3(self, v):    
      self.instance_value_3 = 'set from MyMixinClass_2: ' + v

  def get_instance_value_3(self):       
      return self.instance_value_3

  def set_instance_value_4(self, v):    
      self.instance_value_4 = 'set from MyMixinClass_2: ' + v

  def get_instance_value_4(self):       
      return self.instance_value_4

class MySubclass(MyMainClass, MyMixinClass_2, MyMixinClass_1):  pass

#confirming the class hierarchy

#base classes
# primary superclass, all superclasses
MyMainClass.__class__.__base__            
object.__class__.mro(MyMainClass)[1:]     

# primary superclass, all superclasses
MyMixinClass_1.__class__.__base__         
object.__class__.mro(MyMixinClass_1)[1:]  

# primary superclass, all superclasses
MyMixinClass_2.__class__.__base__         
object.__class__.mro(MyMixinClass_2)[1:]  

# primary superclass, all superclasses
MySubclass.__class__.__base__             
object.__class__.mro(MySubclass)[1:]      

#subclasses
object.__class__.__subclasses__(MyMainClass)

object.__class__.__subclasses__(MyMixinClass_1)

object.__class__.__subclasses__(MyMixinClass_2)

object.__class__.__subclasses__(MySubclass)

#showing the action of the final, mixin-based class class methods
my_subclass_instance = MySubclass('one')
my_subclass_instance.set_instance_value_2('two')
my_subclass_instance.set_instance_value_3('three')
my_subclass_instance.set_instance_value_4('four')

#from MyClass
print(my_subclass_instance.get_instance_value_1())

# from MyMixinMyClass_2  
print(my_subclass_instance.get_instance_value_2()) 

# from MyMixinMyClass_3
print(my_subclass_instance.get_instance_value_3())

#change just enough of the example to get the below to display
#set from MyMixinClass_2: four

# from MyMixinClass_1, which shadows MyMixinClass_2
print(my_subclass_instance.get_instance_value_4())
