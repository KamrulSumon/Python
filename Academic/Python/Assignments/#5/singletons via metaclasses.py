# adapted from http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
#
# the original has cls._instances[cls] instead of Singleton._instances[cls]
# since _instances is declared in Singleton, I don't see how the original can be correct
#
class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:      # instantiate shared class instance on first object instantiation 
      Singleton._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    else:   # reinvoke __init__ for the lone instance on subsequent instantiations.  remove clause if re-init not desired
      Singleton._instances[cls].__init__(*args, **kwargs) 
    return Singleton._instances[cls]

class OneValue(metaclass=Singleton):
  #
  # *** immutable values for class OneValue ***
  #
  # note about e.value: 
  #   since the advent of exception chaining in Python 3, not all built-in exceptions
  #   can be counted on to support .value attributes
  #
  _me = "?? OneValue.{}: "
  _e_value = lambda e: '' if 'value' not in dir(e) else ": " + e.value
  #
  #
  # *** class methods ***
  #
  # init - takes a list of arguments; has no effect for empty lists; uses just the first if present
  #
  def __init__(self, *args): 
    if len(args): self.value = args[0]
  #
  def get(self):
    self.assert_defined('get')
    return self.value
  #
  def set(self, newValue=None):  self.value = newValue
  #
  def inc(self, newValue=1):
    try:
      self.value += newValue
    except Exception as e:
      ex_msg_base = OneValue._me + "can't update value ({}){}"
      ex_msg = ex_msg_base.format('inc', self.value, OneValue._e_value(e))
      raise Exception(ex_msg)
  #
  def unset(self):  del self.value
  #
  # equality by equivalence
  #
  def __eq__(self, other):
    if not isinstance(other, OneValue): return False
    self.assert_defined('__eq__')
    other.assert_defined('__eq__')
    return True    # both instances will always share value
  #
  # memento pattern
  #
  def __repr__(self):
    self.assert_defined('__repr__')
    return "{}({})".format(self.__class__.__name__, self.value)
  #
  # supporting routintes
  #
  def assert_defined(self, routine):
    assert 'value' in dir(self), (OneValue._me + "value is undefined").format(routine)

#
# illustrating failure modes
#
a=OneValue()
a.inc(4)
a.unset()
a.get()
a
b=OneValue()
a == b

#
# illustrating normal operation
#
a=OneValue(1)
a
b=OneValue()
b
c=1
a.get()
a == b
a == c
a.inc()
a == b
a == c

#
# note that the two instances are indistinguishable
#
id(a)
id(b)
