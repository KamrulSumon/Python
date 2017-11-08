class OneValue(object):
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
  # *** mutable values for class OneValue ***
  # this is the shared state that implements the singleton pattern
  #
  _value = None
  #
  # *** class methods ***
  #
  # init - takes a list of arguments; has no effect for empty lists; uses just the first if present
  #
  def __init__(self, *args):  
    if len(args): OneValue._value = args[0]
  #
  def get(self):
    self.assert_defined('get')
    return OneValue._value
  #
  def set(self, newValue=None):  OneValue._value = newValue
  #
  def inc(self, incValue=1):
    try:
      OneValue._value = OneValue._value + incValue
    except Exception as e:
      ex_msg_base = OneValue._me + "can't update value ({}) using {}{}"
      ex_msg = ex_msg_base.format('inc', OneValue._value, incValue, OneValue._e_value(e))
      raise Exception(ex_msg)
  #
  def unset(self):  del OneValue._value
  #
  # equality by equivalence
  #
  def __eq__(self, other):
    if not isinstance(other, OneValue): return False
    self.assert_defined('__eq__')
    other.assert_defined('__eq__')
    return True    # both instances will always share _value
  #
  # memento pattern
  #
  def __repr__(self):
    self.assert_defined('__repr__')
    return "{}({})".format(self.__class__.__name__, self._value)
  #
  # supporting routintes
  #
  def assert_defined(self, routine):
    assert '_value' in dir(OneValue), (OneValue._me + "value is undefined").format(routine)

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
# note that the two instances preserve their identity
#
id(a)
id(b)
