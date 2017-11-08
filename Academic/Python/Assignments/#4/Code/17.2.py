def print_first_n_powers_of_2(n):
  """  print the first n powers of 2, starting with 2^0

  routine prints the first n powers of 2 for a user-supplied integer n,
  starting with 2^0 and ending with 2^n-1.

  >>> print_first_n_powers_of_2(0.5)
  Traceback (most recent call last):
     ...
  TypeError: 'float' object cannot be interpreted as an integer
  >>> print_first_n_powers_of_2(-1)
  >>> print_first_n_powers_of_2(0)
  >>> print_first_n_powers_of_2(1)
  1
  >>> print_first_n_powers_of_2(5)
  1
  2
  4
  8
  16
  """
  p2 = powers_of_2()                      # obtain a copy of the generator function for local use
  for i in range(0,n):  print(next(p2)) 

# Python transforms the initial strings into docstrings
#
print(powers_of_2.__doc__)
print(print_first_n_powers_of_2.__doc__)

# Use doctest.run_docstring_examples to run print_first_n_powers_of_2's test cases, twice:
# -.  In a second mode that simply shows failed tests (default)
# -.  In a first mode that shows all test cases and their results as the cases execute
#
# More on docstring execution:
# -.  Test cases are signaled with initial ">>>" prompt strings.
# -.  Expected results are given after the commands to execute.
# -.  "Traceback" results are treated specially:
#     ..., with the ELLIPSIS option enabled, causes doctest to ignore Traceback details
#     when checking expected results.

import doctest

doctest.run_docstring_examples(print_first_n_powers_of_2, None, optionflags=doctest.ELLIPSIS)

doctest.run_docstring_examples(print_first_n_powers_of_2, None, optionflags=doctest.ELLIPSIS, verbose=True)

class Fib:
  def __init__(self, val_count = float('inf')):
    self.initial_val_count = val_count
  #
  def __iter__(self):
    self.val_count, self.result_queue = self.initial_val_count, [0, 1]
    return self
  #
  def __next__(self):
    if self.val_count <= 0:  raise StopIteration
    self.val_count -= 1
    self.next_result = self.result_queue[0]
    self.result_queue = [self.result_queue[1], self.result_queue[0] + self.result_queue[1]]
    return self.next_result
