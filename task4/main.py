import typing as tp
import numpy as np
import sys
import time
from mpi4py import MPI


def calculate_subset_sizes(n_processes: int, n_points: int) -> list[int]:
    count, remainder = divmod(n_points, n_processes)
    subset_sizes = [count * i for i in range(1, n_processes + 1)] 
    subset_sizes[-1] += remainder
    return subset_sizes

def generate_points(n: int) -> np.ndarray:
    return np.random.rand(n, 2)

def is_in_unit_circle(points: np.ndarray) -> np.ndarray:
    return np.square(points).sum(axis=1) <= 1

def estimate_pi(n: int) -> float:
    points = generate_points(n)
    in_unit_circle = is_in_unit_circle(points).astype(float).sum()
    return 4 * in_unit_circle / n

def estimate_pi_parallel(comm, n_points: int) -> dict[str, tp.Union[float, int]]:
    data = None
    if rank == 0:
        data = calculate_subset_sizes(comm.Get_size(), n_points)
    data = comm.scatter(data, root=0)

    t_start = time.perf_counter()
    pi_est = estimate_pi(data)
    t_end = time.perf_counter()

    time_ = round(t_end - t_start, 4)
    local_res = {'process': comm.Get_rank(), 'n_points': data, 'pi_est': pi_est, 'time': time_}

    global_res = comm.gather(local_res, root=0)
    if rank == 0:
        return global_res



if __name__ == '__main__':
    n_points = int(sys.argv[1])

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    n_processes = comm.Get_size()

    results = estimate_pi_parallel(comm, n_points)
    if rank == 0:
        for result  in results:
            for key, value in result.items():
                print(f'{key}: {value}')
            print('\n')
