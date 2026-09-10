import multiprocessing as mp
import time
import math


def compute_chunk(start, end):
    total = 0.0

    for i in range(start, end):
        x = i * 0.000001

        for j in range(50):
            total += math.sqrt(x + j) * math.sin(x + j)

    return total


def run_benchmark(workers, total_work):
    chunk_size = total_work // workers
    tasks = []

    for i in range(workers):
        start = i * chunk_size

        if i == workers - 1:
            end = total_work
        else:
            end = (i + 1) * chunk_size

        tasks.append((start, end))

    start_time = time.perf_counter()

    with mp.Pool(processes=workers) as pool:
        results = pool.starmap(compute_chunk, tasks)

    end_time = time.perf_counter()

    return end_time - start_time, sum(results)


def main():
    thread_counts = [1, 2, 4, 8, 16, 32]

    total_work = 5_000_000

    print("Workload Algorithm: CPU-bound mathematical computation")
    print("Language & Runtime: Python multiprocessing")
    print()

    all_results = {}

    for workers in thread_counts:
        print(f"Testing N = {workers}")

        times = []

        for run in range(1, 4):
            elapsed, result = run_benchmark(workers, total_work)

            times.append(elapsed)

            print(f"Run {run}: {elapsed:.4f} seconds")

        average = sum(times) / len(times)

        all_results[workers] = average

        print(f"Average: {average:.4f} seconds")
        print()

    t1 = all_results[1]

    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    for workers in thread_counts:
        avg_time = all_results[workers]
        speedup = t1 / avg_time
        efficiency = speedup / workers * 100

        print(
            f"N={workers:<2} | "
            f"Avg={avg_time:.4f}s | "
            f"Speedup={speedup:.4f}x | "
            f"Efficiency={efficiency:.2f}%"
        )


if __name__ == "__main__":
    mp.freeze_support()
    main()