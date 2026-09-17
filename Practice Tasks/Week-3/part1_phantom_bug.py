import multiprocessing as mp
import random

TOTAL_POINTS = 50_000_000

def worker(points_per_process, shared_hits):
    for _ in range(points_per_process):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            shared_hits.value += 1

def main():
    points_per_proc = TOTAL_POINTS // 4

    for run in range(1, 6):
        shared_hits = mp.Value('l', 0, lock=False)
        processes = [
            mp.Process(target=worker, args=(points_per_proc, shared_hits))
            for _ in range(4)
        ]
        
        for p in processes: p.start()
        for p in processes: p.join()

        pi = 4.0 * shared_hits.value / TOTAL_POINTS
        print(f"Run {run}: pi = {pi:.5f} (hits: {shared_hits.value})")

if __name__ == '__main__':
    main()