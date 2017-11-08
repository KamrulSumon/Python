class Circle(object):

  pi = 3.14159
     
  def __init__(self, **kwargs):
    if len(set(['radius', 'diameter', 'circumference', 'area']) & set(kwargs.keys())) != 1:
       raise KeyError("constructor must be called with exactly one keyword from 'radius', 'diameter', 'circumference', or 'area'")
    try:  self.radius = kwargs['radius']
    except KeyError:
      try:  self.diameter = kwargs['diameter']
      except KeyError:
        try:  self.circumference = kwargs['circumference']
        except KeyError:  
          self.area = kwargs['area']
  
  @property
  def radius(self):
    """circle radius"""  
    if not 'r' in dir(self):  raise UnboundLocalError("radius undefined")
    return self.r

  @radius.setter
  def radius(self, r):   
      self.r = r

  @radius.deleter
  def radius(self):
    if 'r' in dir(self):  del self.r
  
  @property
  def diameter(self):     
    """circle diameter"""
    try:       return self.radius * 2
    except:       raise UnboundLocalError("diameter undefined")

  @diameter.setter
  def diameter(self, d):  
      self.radius = d / 2

  @diameter.deleter
  def diameter(self):     
      del self.radius
  
  @property
  def circumference(self):     
    """circle circumference"""  
    try:       return 2 * Circle.pi * self.radius
    except:       raise UnboundLocalError("circumference undefined")

  @circumference.setter
  def circumference(self, c):  
      self.radius = c / (2 * Circle.pi)

  @circumference.deleter
  def circumference(self):     
      del self.radius

  @property
  def area(self):      
    """circle area"""  
    try:       return Circle.pi * self.radius * self.radius
    except:       raise UnboundLocalError("circumference undefined")

  @area.setter
  def area(self, a):   
      self.radius = pow(a / Circle.pi, 0.5)

  @area.deleter
  def area(self):      
      del self.radius

print('This is the directory of the Circle:')
print()
print(dir(Circle))
print()
print(Circle.area.__doc__)
print()
print(Circle.circumference.__doc__)
print()
print(Circle.radius.__doc__)
print()
print(Circle.diameter.__doc__)
print()
