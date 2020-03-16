'''
重点是jump = yield index这个语句。

分成两部分：

yield index 是将index return给外部调用程序。
jump = yield 可以接收外部程序通过send()发送的信息，并赋值给jump
'''


def jumping_range(N):
    index = 0
    while index < N:
        # 通过send()发送的信息将赋值给jump
        jump = yield index
        if jump is None:
            jump = 1
        index += jump


if __name__ == '__main__':
    itr = jumping_range(5)
    print(next(itr))
    print(itr.send(2))
    print(next(itr))
    print(itr.send(-1))