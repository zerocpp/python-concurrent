from inspect import getgeneratorstate


def mygen(n):
    now = 0
    while now < n:
        yield now
        now += 1


if __name__ == '__main__':
    gen = mygen(2)
    print(getgeneratorstate(gen))

    print(next(gen))
    print(getgeneratorstate(gen))

    print(next(gen))
    gen.close()  # 手动关闭/结束生成器
    print(getgeneratorstate(gen))