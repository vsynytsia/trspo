from multiprocessing import Pool
from time import perf_counter
from typing import List, Callable


def collatz(n: int) -> List[int]:
    if n <= 0:
        raise ValueError('Collatz conjecture supports only natural numbers')

    collatz_seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        collatz_seq.append(n)
    return collatz_seq


def benchmark(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        t1 = perf_counter()
        res = func(*args, **kwargs)
        t2 = perf_counter()

        print(f'Function {func.__name__!r} took {t2 - t1:.4f} seconds')
        return res

    return wrapper


@benchmark
def test_collatz_linear(N: int) -> None:
    _ = list(map(collatz, range(1, N + 1)))


@benchmark
def test_collatz_parallel(N: int) -> None:
    with Pool() as pool:
        _ = pool.map(collatz, range(1, N + 1))


def main():
    N = 1_000_000

    test_collatz_linear(N)
    test_collatz_parallel(N)


if __name__ == '__main__':
    main()
