from random import uniform, randint
from threading import Thread, Condition
from time import time


class MyClass1:
    def __init__(self, n: int):
        self.__n = n

    def read(self):
        return self.__n

    def write(self, n):
        self.__n = n


class MyClass2:
    def __init__(self, m: float):
        self.__m = m

    def read(self):
        return self.__m

    def write(self, m):
        self.__m = m


def f1(cls: MyClass1, k1: int, condition: Condition):
    condition.acquire()
    try:
        for k in range(k1):
            cls.write(cls.read() + uniform(1, 2))
            cls.write(cls.read() + uniform(3, 4))
    finally:
        condition.release()


def f2(cls: MyClass2, k2: int, condition: Condition):
    condition.acquire()
    try:
        for k in range(k2):
            cls.write(cls.read() + uniform(5, 6))
            cls.write(cls.read() + uniform(7, 8))
    finally:
        condition.release()


def main():
    time_start = time()
    condition = Condition()

    class1, class2 = MyClass1(n=5), MyClass2(m=2.5)

    n_threads = randint(10, 20)

    k1 = randint(10000, 20000)
    k2 = randint(20000, 30000)

    threads_first_group = [Thread(target=f1, args=(class1, k1, condition)) for _ in range(n_threads // 2)]
    threads_seconds_group = [Thread(target=f2, args=(class2, k2, condition)) for _ in range(n_threads - n_threads // 2)]

    [thread.start() for thread in (threads_first_group + threads_seconds_group)]

    condition.acquire()
    try:
        condition.notify_all()
        all_time = time() - time_start
        print(f'Time taken: {round(all_time, 5)} seconds')
    finally:
        condition.release()


if __name__ == '__main__':
    main()

