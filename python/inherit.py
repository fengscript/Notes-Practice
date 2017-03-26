# coding = utf-8

class SchoolMember:
    '''base class'''
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print('initialized member:{},age:{}'.format(self.name, self.age))


    def tell(self):
        '''tell me detail'''
        print('Super-Class-Method: Name:{}, Age{}'.format(self.name, self.age))

class Stu(SchoolMember):
    '''I'm a student'''
    def __init__(self, name, age):
        SchoolMember.__init__(self, name, age)
        print("initialized student:{}".format(self.name))

    def tell(self):
        SchoolMember.tell(self)
        print('Sub-Class-Method: FYG:"{:d}" '.format(self.age))

s = Stu('FYG', 25)
s.tell()
