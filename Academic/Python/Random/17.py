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


def docTest(k):
    """
    Value 0:    
    >>> fibgen = Fib(0)
    >>> [i for i in fibgen]
    []
    
    value 1:
    >>> fibgen = Fib(1)
    >>> [i for i in fibgen]
    [0]
    
    value 2:
    >>> fibgen = Fib(2)
    >>> [i for i in fibgen]
    [0, 1]
    
    value 10:
    >>> fibgen = Fib(10)
    >>> [i for i in fibgen]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    String:
    >>> fibgen = Fib('ETSU')
    >>> [i for i in fibgen]
    Traceback (most recent call last):
    File "<pyshell#76>", line 1, in <module>
    [i for i in fibgen]
    File "<pyshell#76>", line 1, in <listcomp>
    [i for i in fibgen]
    File "C:/Users/sumonETSU/Documents/Python/17.py", line 10, in __next__
    if self.val_count <= 0:  raise StopIteration
    TypeError: unorderable types: str() <= int()
    
    """
    fibgen = Fib(k)
    return [i for i in fibgen]

