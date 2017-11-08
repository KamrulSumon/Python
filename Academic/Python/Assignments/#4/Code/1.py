#Classes are created by an executable compound statement, class.  It consists of two parts:
#1. a header that names the class to create, and (optionally) its superclasses
#2. a body that specifies the class's initial content

class Trivial: pass

#as a class, Trivial has a unique (if uninteresting) id

print('This is Trivial class unique id:', id(Trivial))
print()

#if a class's superclass is not specified, it is assigned one superclass: class object
#shows a class's immediate superclass

print('This shows a class immediate superclass', Trivial.__class__.__base__)

print('This is Trivial:', Trivial)
print()

#'Trivial is a subclass of object and inherits object attributes

print('This is object attributes:')
print(dir(object))
print()
print()

print('This is trivial attributes:')
print(dir(Trivial))
print()
print()

#showing that every attribute in object is in Trivial
set (dir(object))
print('After setting the directory for object, this is object attribues:')
print(dir(object))
print()
print()

set(dir(Trivial))
print('After setting the directory for Trivial, this is Trivial attribues:')
print(dir(Trivial))
print()
print()

#showing that Trivial adds a few attributes to object
set (dir(Trivial))
print('After setting the directory for Trivial, this is Trivial attribues:')
print(dir(Trivial))
print()
print()

set (dir(object))
print('After setting the directory for object, this is object attribues:')
print(dir(object))
print()
print()

#Trivial can be used to generate new objects
trivial_instance_1 = Trivial()
print('This is trivial_instance_1 value:', trivial_instance_1)

trivial_instance_2 = Trivial()
print('This is trivial_instance_2 value:', trivial_instance_2)
print()

#these objects are both type Trivial
print('This is the type of trivial_instance_1:', type(trivial_instance_1))

print('This is the type of trivial_instance_2:', type(trivial_instance_2))
print()

#they are, however, distinct from Trivial as well as each other
print('This is id(Trivial):', id(Trivial))

print('This is id(trivial_instance_1):', id(trivial_instance_1))

print('This is id(trivial_instance_2):', id(trivial_instance_2))
print()

print('This is the outcome of id(Trivial) == id(trivial_instance_1):', id(Trivial) == id(trivial_instance_1))

print('This is the outcome of id(Trivial) == id(trivial_instance_2):', id(Trivial) == id(trivial_instance_2))

print('This is the outcome of id(trivial_instance_1) == id(trivial_instance_2):', id(trivial_instance_1) == id(trivial_instance_2))
print()
