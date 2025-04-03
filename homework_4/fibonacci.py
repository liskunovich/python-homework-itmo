import time
import threading
import multiprocessing
from typing import Callable, Any


def calculate_fibonacci(number: int) -> int:
    if number <= 1:
        return number
    
    prev, current = 0, 1
    for _ in range(2, number + 1):
        prev, current = current, prev + current
    return current


def measure_execution_time(task: Callable, *task_args: Any) -> float:
    start_time = time.perf_counter()
    task(*task_args)
    return time.perf_counter() - start_time


class FibonacciExecutor:
    def __init__(self, fib_number: int, repetitions: int):
        self.fib_number = fib_number
        self.repetitions = repetitions
    
    def run_sequential(self) -> None:
        for _ in range(self.repetitions):
            calculate_fibonacci(self.fib_number)
    
    def run_with_threads(self) -> None:
        workers = []
        for _ in range(self.repetitions):
            worker = threading.Thread(target=calculate_fibonacci, args=(self.fib_number,))
            workers.append(worker)
            worker.start()
        
        for worker in workers:
            worker.join()
    
    def run_with_processes(self) -> None:
        workers = []
        for _ in range(self.repetitions):
            worker = multiprocessing.Process(target=calculate_fibonacci, args=(self.fib_number,))
            workers.append(worker)
            worker.start()
        
        for worker in workers:
            worker.join()


def save_results(filename: str, **results: float) -> None:
    with open(filename, "w") as file:
        for strategy, duration in results.items():
            file.write(f"{strategy.replace('_', ' ').title()}: {duration:.4f} seconds\n")


if __name__ == "__main__":
    FIBONACCI_NUMBER = 500000
    REPETITION_COUNT = 10
    
    executor = FibonacciExecutor(FIBONACCI_NUMBER, REPETITION_COUNT)
    
    timing_results = {
        "sequential_execution": measure_execution_time(executor.run_sequential),
        "threaded_execution": measure_execution_time(executor.run_with_threads),
        "multiprocess_execution": measure_execution_time(executor.run_with_processes)
    }
    
    save_results("performance_results.txt", **timing_results)
    print("Performance results have been saved to 'performance_results.txt'")
