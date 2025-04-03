import math
import time
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count
from typing import Callable, Tuple

logging.basicConfig(
    filename="integration_benchmark.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class IntegrationCalculator:
    def __init__(self, function: Callable, lower_bound: float, upper_bound: float):
        self.function = function
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def _compute_chunk(self, chunk_start: float, chunk_end: float, iterations: int) -> float:
        chunk_size = chunk_end - chunk_start
        step = chunk_size / iterations
        area = 0.0
        
        for i in range(iterations):
            x = chunk_start + i * step
            area += self.function(x) * step
        
        return area

    def _execute_integration(self, executor_class, worker_count: int, total_iterations: int) -> Tuple[float, float]:
        chunk_size = (self.upper_bound - self.lower_bound) / worker_count
        iterations_per_chunk = total_iterations // worker_count
        tasks = []

        start_time = time.perf_counter()
        
        with executor_class(max_workers=worker_count) as executor:
            for i in range(worker_count):
                chunk_start = self.lower_bound + i * chunk_size
                chunk_end = chunk_start + chunk_size
                
                logging.info(f"Processing chunk [{chunk_start:.4f}, {chunk_end:.4f}]")
                tasks.append(
                    executor.submit(
                        self._compute_chunk,
                        chunk_start,
                        chunk_end,
                        iterations_per_chunk
                    )
                )

            total = sum(task.result() for task in tasks)
        
        duration = time.perf_counter() - start_time
        return total, duration

    def with_threads(self, worker_count: int, total_iterations: int) -> Tuple[float, float]:
        return self._execute_integration(ThreadPoolExecutor, worker_count, total_iterations)

    def with_processes(self, worker_count: int, total_iterations: int) -> Tuple[float, float]:
        return self._execute_integration(ProcessPoolExecutor, worker_count, total_iterations)


def save_benchmark_results(filename: str, results: dict) -> None:
    with open(filename, "w") as output_file:
        for workers, (thread_time, process_time) in results.items():
            output_file.write(
                f"Workers: {workers}\n"
                f"  Threads: {thread_time:.4f} seconds\n"
                f"  Processes: {process_time:.4f} seconds\n"
                f"  Speedup: {thread_time/process_time:.2f}x\n\n"
            )


def run_benchmarks():
    lower = 0
    upper = math.pi / 2
    max_workers = cpu_count() * 2
    iterations = 10_000_000
    benchmark_results = {}

    calculator = IntegrationCalculator(math.cos, lower, upper)

    for worker_count in range(1, max_workers + 1):
        _, thread_time = calculator.with_threads(worker_count, iterations)
        _, process_time = calculator.with_processes(worker_count, iterations)
        benchmark_results[worker_count] = (thread_time, process_time)

    save_benchmark_results("integration_performance.txt", benchmark_results)
    logging.info("Benchmark completed and results saved")


if __name__ == "__main__":
    logging.info("Starting integration benchmark")
    run_benchmarks()
    logging.info("Benchmark finished")
    print("Integration benchmark completed. Check 'integration_performance.txt' for results.")
