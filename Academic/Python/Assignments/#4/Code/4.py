#2783-2799
#illustrating calling conventions for virtual and non-virtual method calls

class MyClass:

  def __init__(self, iv_1, iv_2):
    #a virtual method call
    self.set_instance_value_1( iv_1 ) 
    
    #a non-virtual method call            
    MyClass.set_instance_value_2( self, iv_2 )     

  def set_instance_value_1(self, v):    
      self.instance_value_1 = 'set from MyClass: ' + v

  def get_instance_value_1(self):       
      return self.instance_value_1

  def set_instance_value_2(self, v):    
      self.instance_value_2 = 'set from MyClass: ' + v

  def get_instance_value_2(self):       
      return self.instance_value_2

class MySubclass(MyClass):

  def set_instance_value_1(self, v):    
      self.instance_value_1 = 'set from MySubclass: ' + v

  def get_instance_value_1(self):       
      return self.instance_value_1
 
  def set_instance_value_2(self, v):    
     self.instance_value_2 = 'set from MySubclass: ' + v

  def get_instance_value_2(self):       
      return self.instance_value_2

#2803-2828
#confirm that the initialization logic works as claimed
mysubclass_instance = MySubclass( 'first', 'second' )

print(mysubclass_instance.get_instance_value_1())
print()
print(mysubclass_instance.get_instance_value_2())
print()

