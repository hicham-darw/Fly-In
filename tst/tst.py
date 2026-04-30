class A:
    def __init__(self):
        self.name = ''
        self.age = 0
        self.nickname = ''


    def set_name(self, name):
        self.name = name
        return self

    def set_age(self, age):
        self.age = age
        return self

    def set_nickname(self, nickname):
        self.nickname = nickname
        return self


obj = A()
obj = obj.set_name("darwin").set_age(17).set_nickname("Hicham")

print(obj.name)
print(obj.age)
print(obj.nickname)

