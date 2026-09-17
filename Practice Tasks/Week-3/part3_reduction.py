import multiprocessing as mp
import random
import time

TOTAL_POINTS = 100_000_000

def worker_local(points_per_process, return_dict, proc_id):
    hits = 0
    for _ in range(points_per_process):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            hits += 1
    return_dict[proc_id] = hits  # Локальное накопление без общих блокировок

def main():
    print("=== PART 3: OpenMP-Style Reduction ===")
    thread_counts = [1, 2, 4, 8, 16, 32]
    t1_time = 0

    print(f"{'Threads(T)':<10} | {'Runtime(ms)':<12} | {'Speedup (T1/TN)':<18} | {'Efficiency':<12}")
    print("-" * 60)

    for num_procs in thread_counts:
        manager = mp.Manager()
        return_dict = manager.dict()
        points_per_proc = TOTAL_POINTS // num_procs

        start = time.time()
        processes = [
            mp.Process(target=worker_local, args=(points_per_proc, return_dict, i))
            for i in range(num_procs)
        ]
        
        for p in processes: p.start()
        for p in processes: p.join()

        duration = (time.time() - start) * 1000

        if num_procs == 1:
            t1_time = duration

        speedup = t1_time / duration if duration > 0 else 1.0
        efficiency = (speedup / num_procs) * 100

        print(f"{num_procs:<10} | {duration:<12.0f} | {speedup:<18.2f}x | {efficiency:<11.1f}%")

if __name__ == '__main__':
    main()