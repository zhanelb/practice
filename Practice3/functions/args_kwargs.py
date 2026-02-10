def total(*args):
    print(sum(args))

total(1, 2, 3)
total(10, 20)


def info(**kwargs):
    for key, value in kwargs.items():
        print(key, "=", value)

info(name="Zhanel", city="Almaty")


def show(a, *args, **kwargs):
    print("a:", a)
    print("args:", args)
    print("kwargs:", kwargs)

show(5, 1, 2, x=10, y=20)
