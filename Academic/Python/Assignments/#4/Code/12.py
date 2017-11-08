class MyClass(object):

  def __init__(self, unreadFile, unwriteFile):             
    super().__setattr__('unreadFile', unreadFile)     
    super().__setattr__('unwriteFile', unwriteFile)

    try:
      self.unreadFileIO = open(unreadFile, 'r')
      self.unreadFile = self.unreadFileIO.read().split()
      self.unreadFileIO.close()
    except IOError:
      print('The file', unreadFile, 'could not be opened.')
      print()

    try:
      self.unwriteFileIO = open(unwriteFile, 'r')
      self.unwriteFile = self.unwriteFileIO.read().split()
      self.unwriteFileIO.close()     
    except IOError:
      print('The file', unwriteFile, 'could not be opened.')
      print()

  def get_c(self, attribute):
    return super().__getattribute__(attribute)
 
  def set_c(self, attribute, c):   
    return super().__setattr__(attribute, c)

  def __getattribute__(self, attr_name):
    if attr_name == 'c':  raise LookupError('c is private -- cannot be read')
    return super().__getattribute__(attr_name)
 
  def __setattr__(self, attr_name, c):
    if attr_name == 'c':  raise LookupError('c is private -- cannot be written')
    return super().__setattr__(attr_name, c)

test = MyClass('unwriteFile.txt','unreadFile.txt')

print(test.unreadFile)
print(test.unwriteFile)
test.set_c('ur_attribute', 'My son is in the 8th grade.')
print(test.get_c('ur_attribute'))
print()
test.set_c('uw_attribute', 'This is the second Python homework.')
print()
print(test.get_c('uw_attribute'))
print()






