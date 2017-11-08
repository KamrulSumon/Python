class Fib:
  def __init__(self, val_count = float('inf')):
    self.initial_val_count = val_count
  
  def __iter__(self):
    self.val_count, self.result_queue = self.initial_val_count, [0, 1]
    return self

  def __next__(self):
    if self.val_count <= 0:  raise StopIteration
    self.val_count -= 1
    self.next_result = self.result_queue[0]
    self.result_queue = [self.result_queue[1], self.result_queue[0] + self.result_queue[1]]
    return self.next_result

def FibTest(k):
    """ print the Fib series, starting with 0

    >>> FibTest('firstkval')
    Traceback(most recent call last):
    >>> FibTest(a)
    []
    >>> FibTest(0)
    []
    >>> FibTest(1)
    [0]
    >>> FibTest(2)
    [0, 1]
    >>> FibTest(10)
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    return [i for i in Fib(k)]                      

import doctest
doctest.run_docstring_examples(FibTest, None, optionflags=doctest.ELLIPSIS, verbose=True)

