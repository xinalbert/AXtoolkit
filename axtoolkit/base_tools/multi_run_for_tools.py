import psutil
from multiprocessing import Pool
from typing import Callable, List, Tuple, Any, Optional
from tqdm import tqdm


class MultiRun:
    def __init__(self, func: Callable, args_list: List[Tuple], max_threads: Optional[int] = None, **kwargs):
        """
        This class is used to run a function with multiple arguments in multiple threads.
        Args:
            func: The function to be run.
            args_list: A list of tuples, where each tuple contains the arguments for the function.
            max_threads: The maximum number of threads to use. If None, the number of threads will be determined automatically.
        """
        self.func = func
        self.args_list = args_list
        self.max_threads = max_threads
        self.kwargs = kwargs

    @staticmethod
    def get_free_cpus(threshold: int = 30) -> int:
        """
        This function returns the number of free CPUs on the system.
        Args:
            threshold: The threshold for CPU usage percentage, default is 30%.
        Returns:
            The number of free CPUs.
        """
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        free_cpus = sum(1 for p in cpu_percent if p < threshold)
        return free_cpus
    

    @staticmethod
    def multi_threads_run(
        func: Callable, args_list: List[Tuple], max_threads: Optional[int] = None
    ) -> List[Any]:
        """
        This function runs a function with multiple arguments in multiple threads.
        Args:
            func: The function to be run.
            args_list: A list of tuples, where each tuple contains the arguments for the function.
            max_threads: The maximum number of threads to use. If None, the number of threads will be determined automatically.
        Returns:
            A list of results from the function.

        """
        num_threads = int(0.6 * MultiRun.get_free_cpus())
        if max_threads is not None:
            num_threads = min(num_threads, max_threads)
        if num_threads <= 0:
            num_threads = 1  # at least use one thread
        if len(args_list) == 1:
            num_threads = 1  # at least use one thread
        print(f"Using {num_threads} threads...")
        
        # Use tqdm to display progress
        results = []
        with Pool(num_threads) as pool:
            with tqdm(total=len(args_list), desc="Processing") as pbar:
                for result in pool.starmap(func, args_list):
                    results.append(result)
                    pbar.update(1)
        return results

    def run(self) -> List[Any]:
        """
        调用实例的 `multi_threads_run` 方法并返回结果。
        """
        return MultiRun.multi_threads_run(self.func, self.args_list, self.max_threads)