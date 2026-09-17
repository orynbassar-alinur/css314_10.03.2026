import multiprocessing as mp
import random
import time

TOTAL_POINTS = 50_000_000

def worker_sync(points_per_process, shared_hits, lock):
    for _ in range(points_per_process):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            with lock:
                shared_hits.value += 1

def main():
    start_single = time.time()
    single_hits = 0
    for _ in range(TOTAL_POINTS):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            single_hits += 1
    time_single = (time.time() - start_single) * 1000
    print(f"Single Process:            Time = {time_single:.0f} ms, pi = {4.0 * single_hits / TOTAL_POINTS:.5f}")

    shared_hits = mp.Value('l', 0, lock=True)
    lock = mp.Lock()
    points_per_proc = TOTAL_POINTS // 4
    
    start_sync = time.time()
    processes = [
        mp.Process(target=worker_sync, args=(points_per_proc, shared_hits, lock))
        for _ in range(4)
    ]
    
    for p in processes: p.start()
    for p in processes: p.join()
    time_sync = (time.time() - start_sync) * 1000
    
    print(f"Synchronized Multi-process: Time = {time_sync:.0f} ms, pi = {4.0 * shared_hits.value / TOTAL_POINTS:.5f}")

if __name__ == '__main__':
    main()