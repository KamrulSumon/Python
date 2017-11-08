import operator

class Elist(list):
  def __lt__(self, other):
    return NotImplemented if not isinstance(other, Elist) else self.comparison(other,operator.lt)

  def __le__(self, other):
    return NotImplemented if not isinstance(other, Elist) else self.comparison(other,operator.le)

  def __eq__(self, other):
    return isinstance(other, Elist) and self.comparison(other,operator.eq)

  def __ne__(self, other):
    return not isinstance(other, Elist) or self.comparison(other,operator.ne)

  def __ge__(self, other):
    return NotImplemented if not isinstance(other, Elist) else self.comparison(other,operator.ge)

  def __gt__(self, other):
    return NotImplemented if not isinstance(other, Elist) else self.comparison(other,operator.gt)

  def comparison(self,other,compOperator):
      return any([compOperator(a,b) for a in self for b in other])

list0 = Elist([])
list1 = Elist([0, 1, 2, 3])
list2 = Elist([3, 4, 5, 6])
list3 = Elist([6, 7, 8, 9])

list0 < []
list0 == []
list0 != []

(list0 < list0, list0 <= list0, list0 == list0, list0 != list0, list0 >= list0, list0 > list0)
(list0 < list1, list0 <= list1, list0 == list1, list0 != list1, list0 >= list1, list0 > list1)

(list1 < list1, list1 <= list1, list1 == list1, list1 != list1, list1 >= list1, list1 > list1)

(list1 < list2, list1 <= list2, list1 == list2, list1 != list2, list1 >= list2, list1 > list2)
(list2 < list1, list2 <= list1, list2 == list1, list2 != list1, list2 >= list1, list2 > list1)

(list2 < list3, list2 <= list3, list2 == list3, list2 != list3, list2 >= list3, list2 > list3)
(list3 < list2, list3 <= list2, list3 == list2, list3 != list2, list3 >= list2, list3 > list2)

(list1 < list3, list1 <= list3, list1 == list3, list1 != list3, list1 >= list3, list1 > list3)
(list3 < list1, list3 <= list1, list3 == list1, list3 != list1, list3 >= list1, list3 > list1)

print("list1 == list2", list1.__eq__(list2))
print()
print("list2 == list1", list2.__eq__(list1))
print()
print("list1 != list2", list1.__ne__(list2))
print()
print("list2 != list1", list1.__ne__(list1))
print()
print("list1 < list2", list1.__lt__(list2))
print()
print("list2 < list1", list1.__lt__(list1))
print()
print("list1 > list2", list1.__gt__(list2))
print()
print("list2 > list1", list2.__gt__(list1))
print()
print("list1 <= list2", list1.__le__(list2))
print()
print("list2 <= list1", list1.__le__(list1))
print()
print("list2 >= list1", list1.__ge__(list1))
print()
