class Circle(object):

  pi = 3.14159
   
  def __init__(self, **kwargs):
    print(set(kwargs.keys()))

    if len(set(['radius', 'diameter', 'circumference', 'area']) & set(kwargs.keys())) != 1:
       raise KeyError("constructor must be called with exactly one keyword from 'radius', 'diameter', 'circumference', or 'area'")

    try:  self.radius = kwargs['radius']
    except KeyError:
      try:  self.diameter = kwargs['diameter']
      except KeyError:
        try:  self.circumference = kwargs['circumference']
        except KeyError:  
          self.area = kwargs['area']
 
  def getradius(self):     
    if not 'radius' in dir(self):  raise UnboundLocalError("radius undefined")
    return self.radius

  def setradius(self, r):  
      self.radius = r

  def delradius(self):
    if 'radius' in dir(self):   del self.radius

  radius = property(getradius, setradius, delradius, 'circle radius')

  def setradius(self, r):  
      self.r = r
  
  def delradius(self):
    if 'r' in dir(self):   
        del self.r
  
  radius = property(getradius, setradius, delradius, 'circle radius')
  
  def getdiameter(self):     
    try:       return self.radius * 2
    except:    raise UnboundLocalError("diameter undefined")
  
  def setdiameter(self, d):  
      self.radius = d / 2
  
  def deldiameter(self):     
      del self.radius
  
  diameter = property(getdiameter, setdiameter, deldiameter, 'circle diameter')

  def getcircumference(self):     
    try:       return 2 * Circle.pi * self.radius
    except:    raise UnboundLocalError("circumference undefined")

  def setcircumference(self, c):  
      self.radius = c / (2 * Circle.pi)
  def delcircumference(self):     
      del self.radius
  
  circumference = property(getcircumference, setcircumference, delcircumference, 'circle circumference')
  
  def getarea(self):      
    try:       return Circle.pi * self.radius * self.radius
    except:    raise UnboundLocalError("circumference undefined")
 
  def setarea(self, a):   
      self.radius = pow(a / Circle.pi, 0.5)

  def delarea(self):      
      del self.radius

  area = property(getarea, setarea, delarea, 'circle area')

c = Circle(radius=3)
c.radius, c.diameter, c.circumference, c.area
c.area = 3
c.radius, c.diameter, c.circumference, c.area

del c.circumference

print(c.radius, c.diameter, c.circumference, c.area)
