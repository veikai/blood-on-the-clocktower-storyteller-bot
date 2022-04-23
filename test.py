from functools import partial


a = [1, 2, 3]


def t(b):
    print(b)

c = partial(t, a)
a = [1, 2, 3, 5]
c()