class MyClass:
    
    #The next six lines define two static methods for this class
    #These two lines define a setter for MyClass's static_value variable

    def set_static_value(newv): 
        MyClass.static_value = newv    
    
    #This line redefines set_static_value as a static method
    set_static_value = staticmethod(set_static_value)

    #These two lines define a getter for MyClass static_value variable
    def get_static_value():   
        return MyClass.static_value

    #This line redefines get_static_value as a static method
    get_static_value = staticmethod(get_static_value)
    
    #The next six lines define two class methods for this class
    #The following 3 lines define a classmethod for MyClass that sets an arbitrary attribute
    def set_classattr_foo(thisclass, value):            
        thisclass.foo = value

    #This is required to make set_classattr a classmethod
    set_classattr_foo = classmethod(set_classattr_foo)

    #These 3 lines define a classmethod for MyClass
    def get_classattr_foo(thisclass):                   
        return thisclass.foo

    #This is required to make get_classattrs a classmethod
    get_classattr_foo = classmethod(get_classattr_foo)  

    #These final four lines define two instance methods for MyClass
    #These 2 lines define an instance method for MyClass:
    def set_instance_value(self, v):                   
        self.instance_value = v

    #These 2 lines define an instance method for MyClass:
    def get_instance_value(self):                       
        return self.instance_value
    
#Creating a trivial subclass of this class to illustrate the method operation
class MySubclass(MyClass): pass

#Show Python protocols for invoking instance methods, static methods, and class methods
#Creating instances of these classes to illustrate the method operation
myclass_instance_1 = MyClass()
type(myclass_instance_1)

myclass_instance_2 = MyClass()
type(myclass_instance_2)

mysubclass_instance = MySubclass()
type(mysubclass_instance)

#2a - 2567-2569 which assignment(s) affect a common variable
#instance methods are commonly invoked by class instance 
#illustrates instance method invocation and operation
myclass_instance_1.set_instance_value(1)
myclass_instance_2.set_instance_value(2)
mysubclass_instance.set_instance_value(3)

print(myclass_instance_1.get_instance_value())  #prints 1
print(myclass_instance_2.get_instance_value())  #prints 2
print(mysubclass_instance.get_instance_value()) #prints 3
print()

#2b - 2585-2587 which assignment(s) affect a common variable 
#illustrate staticmethod invocation and operation
#static methods can be invoked by class instance
myclass_instance_1.set_static_value(1) 
myclass_instance_2.set_static_value(2)
mysubclass_instance.set_static_value(3)

print(myclass_instance_1.get_static_value())  #prints 3
print(myclass_instance_2.get_static_value())  #prints 3
print(mysubclass_instance.get_static_value()) #prints 3
print()

#staticmethods are more commonly invoked drectly, by class name; no instance is required
MyClass.set_static_value(1)                      
MySubclass.set_static_value(2)

MyClass.get_static_value()
MySubclass.get_static_value()

#2c 2605-2607 which assignment(s) affect a common variable
#classmethods can be invoked by class instance
myclass_instance_1.set_classattr_foo(1)         
myclass_instance_2.set_classattr_foo(2)
mysubclass_instance.set_classattr_foo(3)

print(myclass_instance_1.get_classattr_foo())  #prints 2       
print(myclass_instance_2.get_classattr_foo())  #prints 2
print(mysubclass_instance.get_classattr_foo()) #prints 2
print()

#classmethods are more commonly invoked directly, by class name; no instance is required
MyClass.set_classattr_foo(1)                   
MySubclass.set_classattr_foo(2)

MyClass.get_classattr_foo()
MySubclass.get_classattr_foo()
