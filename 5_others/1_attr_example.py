import heapq
class A:
    def __init__(self, x):
        self.x = x

    def __getattribute__(self, attr):
        print('getting attribute', attr)
        return super().__getattribute__(attr)


class B:
    def __init__(self, x):
        self.x = x
        self.holder = 1

    def __getattribute__(self, attr):
        print('getting attribute', attr)
        return super().__getattribute__(attr)

    def __getattr__(self, attr):
        print(attr)
        return self.holder


a = A(x='a')

b = B(x='b')

print('a.x =', a.x)
print('b.x =', b.x)

print('b.c =', b.c)
print('a.c =', end='')
print(a.c)