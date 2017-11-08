class MyClass:
  static_value = 'initial static value'
  
  @staticmethod
  def set_static_value(newv):   
      MyClass.static_value = newv

  @staticmethod
  def get_static_value():      
      return MyClass.static_value

  #reset static_value from **kwds, if present
  #initialize instance_value from **kwds, if present; otherwise, set to None

  def __init__(self, **kwds):
    try:     MyClass.set_static_value( kwds[ 'static_value' ])
    except:  pass

    #the most common way of calling an instance method from within class scope 
    self.set_instance_value( kwds.get( 'instance_value', None ) )      
  
    #using class name with explicit 'self' argument also works
    def add_to_instance_value(self, v):                                         
    
        #equivalent to self.set_instance_value(self.get_instance_value() + v) or just self.instance_value += v
        MyClass.set_instance_value(self, MyClass.get_instance_value(self) + v)      
                                                                              

  def set_instance_value(self, v):     
      self.instance_value = v
 
  def get_instance_value(self):        
      return self.instance_value

  def update_values(self,stat,inst):
      self.instance_value = inst
      MyClass.static_value = stat

  def set_instance_value(self, v):     
      self.instance_value = v

  def get_instance_value(self):        
      return self.instance_value

# confirm that the initialization logic works as claimed
myclass_instance_1 = MyClass()
myclass_instance_1.get_static_value()
myclass_instance_1.get_instance_value()

myclass_instance_2 = MyClass()
#(static_value = 'updated static value', instance_value = 'initial instance value')
#myclass_instance_2.get_static_value()
#myclass_instance_2.get_instance_value()

#myclass_instance_2.add_to_instance_value( ', now with additional content')
#myclass_instance_2.get_instance_value()

myclass_instance_1.update_values('static1', 'instance1')
myclass_instance_2.update_values('static2', 'instance2')

print()
print(myclass_instance_1.get_static_value())
print()
print(myclass_instance_1.get_instance_value())
print()
print(myclass_instance_2.get_static_value())
print()
print(myclass_instance_2.get_instance_value())
print()
