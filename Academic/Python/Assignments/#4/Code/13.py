class pupil_set(object):
    
        class partially_qualified_pupil_set(object):

                def __init__(self, pupil, qualifier):
                    valid_qualifiers = ['first', 'middle','last']
                    assert qualifier.casefold() in valid_qualifiers, "invalid qualifier: {} (must be in {})".format(valid_qualifiers)
                    self.pupil = pupil
                    self.qualifier = valid_qualifiers.index(qualifier.casefold())

                def __getattr__(self, attr_name):
                    pupil_lst=[0,1,2]
                    pupil_lst.remove(self.qualifier)
                    return [(pupil[pupil_lst[0]], pupil[pupil_lst[1]])
                             for pupil in self.pupil if pupil[self.qualifier] == attr_name]              

        def __init__(self, pupil_set):
            self.pupil_set = pupil_set

        def __getattr__(self, attr_name):
                return pupil_set.partially_qualified_pupil_set(self.pupil_set, attr_name)

all_pupils = \
           ([('Evan', 'helpful', 'Blankenship'), ('Jordan', 'wonderstudent', 'Brown'), ('Mark', 'personality', 'Buckner'), ('Jason', 'quiet', 'Bunn'),
           ('Ben', 'nice', 'Burton'), ('Yan', 'quiet', 'Cao'), ('Brad', 'first_semester', 'Cross'), ('Joseph', 'Radford', 'Elliott'),
           ('Dale', 'extra_quiet', 'Giblin'), ('Kamrul', 'smart', 'Hasan'), ('Elijah', 'absent', 'Laws'), ('Jalaj', 'friendly', 'Nautiyal'),
           ('Pramod', 'programmer', 'Nepal'), ('Cindy', 'loveable', 'Taylor')] )

design_pupil = pupil_set(all_pupils)

print(design_pupil.middle.smart)
print()
print(design_pupil.First.Cindy)
print()
print(design_pupil.Middle.friendly)
print()
print(design_pupil.Last.Nepal)
print()
print(design_pupil.fIRSt.Evan)
print()

print('Here is a list of all pupils in software design:')
print()

for c in all_pupils:
    print ([c])
    print()