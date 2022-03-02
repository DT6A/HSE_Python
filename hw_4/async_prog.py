import concurrent
import datetime
import math
import time
import codecs
import multiprocessing as mp

from threading import Thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

ARG = 20000
THREADS = 10


def fib(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]

    nums = [0, 1]
    for i in range(n - 2):
        nums.append(nums[-1] + nums[-2])
    return nums


def integrate(f, a, b, job=0, n_jobs=1, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    l = n_iter // n_jobs * job
    r = min(n_iter // n_jobs * (job + 1), n_iter)
    for i in range(l, r):
        acc += f(a + i * step) * step
    return acc


messages = []


def worker_A(in_queue, out_queue):
    while True:
        if not in_queue.empty():
            out_queue.put(in_queue.get().lower())
            time.sleep(5)


def worker_B(in_queue, out_queue):
    while True:
        if not in_queue.empty():
            out_queue.put(codecs.encode(in_queue.get(), 'rot_13'))


def worker_writer(in_queue):
    while True:
        if not in_queue.empty():
            messages.append(f'{datetime.datetime.now()}: got processed message "{in_queue.get()}"\n')


if __name__ == '__main__':
    # Easy
    with open('artifacts/easy.txt', 'w') as f:
        f.write('Threads: ')
        threads = []
        start = time.time()
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            for _ in range(THREADS):
                threads.append(executor.submit(fib, ARG))
            for t in concurrent.futures.as_completed(threads):
                t.result()
            end = time.time()
        f.write(str(end - start) + ' seconds\n')

        f.write('Processes: ')
        procs = []
        start = time.time()
        with ProcessPoolExecutor(max_workers=THREADS) as executor:
            for _ in range(THREADS):
                procs.append(executor.submit(fib, ARG))
            for p in concurrent.futures.as_completed(procs):
                p.result()
            end = time.time()
        f.write(str(end - start) + ' seconds\n')

    cpu_num = mp.cpu_count()

    # Medium
    with open('artifacts/medium.txt', 'w') as f:
        for n_jobs in range(1, 2 * cpu_num + 1):
            threads = []
            f.write(f'Running with {n_jobs} threads:\n')
            start = time.time()
            with ThreadPoolExecutor(max_workers=n_jobs) as executor:
                integrate_res = 0
                for i in range(n_jobs):
                    threads.append(executor.submit(integrate, math.cos, 0, math.pi / 2, i, n_jobs))
                for t in concurrent.futures.as_completed(threads):
                    integrate_res += t.result()
                end = time.time()
            f.write(f'\tTime: {end - start} seconds\n\tResult: {integrate_res}\n')

            procs = []
            f.write(f'Running with {n_jobs} processes:\n')
            start = time.time()
            with ProcessPoolExecutor(max_workers=n_jobs) as executor:
                integrate_res = 0
                for i in range(n_jobs):
                    procs.append(executor.submit(integrate, math.cos, 0, math.pi / 2, i, n_jobs))
                for p in concurrent.futures.as_completed(procs):
                    integrate_res += p.result()
                end = time.time()
            f.write(f'\tTime: {end - start} seconds\n\tResult: {integrate_res}\n')

    # Hard
    A_queue = mp.Queue()
    B_queue = mp.Queue()
    writer_queue = mp.Queue()

    with open('artifacts/hard.txt', 'w') as f:
        A = mp.Process(target=worker_A, args=(A_queue, B_queue), daemon=True)
        B = mp.Process(target=worker_B, args=(B_queue, writer_queue), daemon=True)
        writer = Thread(target=worker_writer, args=(writer_queue,), daemon=True)

        A.start()
        B.start()
        writer.start()

        while True:
            msg = input('>> ')
            if msg == 'exit':
                messages.append(f'{datetime.datetime.now()}: Terminating\n')
                break
            messages.append(f'{datetime.datetime.now()}: got message "{msg}"\n')
            A_queue.put(msg)
        f.write(''.join(messages))
