import operator

class Hlist(list):

  def __lt__(self, other):
    return NotImplemented if not isinstance(other, Hlist) else self.comp(other,operator.lt)

  def __le__(self, other):
    return NotImplemented if not isinstance(other, Hlist) else self.comp(other,operator.le)

  def __eq__(self, other):
    return isinstance(other, Hlist) and self.comp(other,operator.eq)

  def __ne__(self, other):
    return not isinstance(other, Hlist) or self.comp(other,operator.ne)

  def __ge__(self, other):
    return NotImplemented if not isinstance(other, Hlist) else self.comp(other,operator.ge)

  def __gt__(self, other):
    return NotImplemented if not isinstance(other, Hlist) else self.comp(other,operator.gt)

  def comp(self, other, operator):
    T = 0
    F = 0
    for a in self:
        for b in other:
            if operator(a, b) is True: T += 1
            else: F += 1
    return True if T > F else False

list0 = Hlist([])
list1 = Hlist([0, 1, 2, 3])
list2 = Hlist([3, 4, 5, 6])
list3 = Hlist([6, 7, 8, 9])

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

print()
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
print("list1 >= list2", list1.__ge__(list2))
print()
print("list2 >= list1", list1.__ge__(list1))
print()

