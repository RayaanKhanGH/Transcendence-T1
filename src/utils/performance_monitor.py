import time
import psutil
import os
import threading
import logging
import functools
from statistics import mean

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """
    Context manager to monitor CPU and RAM usage of the current process during a code block execution.
    """
    def __init__(self, step_name: str = "Operation"):
        self.step_name = step_name
        self.process = psutil.Process(os.getpid())
        self.cpu_count = psutil.cpu_count() or 1
        self.running = False
        self.stats = {
            "duration": 0,
            "avg_cpu": 0,
            "peak_cpu": 0,
            "start_ram": 0,
            "avg_ram": 0,
            "peak_ram": 0,
            "end_ram": 0
        }
        self._monitor_thread = None
        self._samples = {"cpu": [], "ram": []}

    def _sample(self):
        """Sampling loop running in a separate thread."""
        while self.running:
            try:
                # Use 0.25s interval to smooth out OS timer jitter that causes >100% artifacts on Windows
                cpu = self.process.cpu_percent(interval=0.25) 
                ram = self.process.memory_info().rss / (1024 * 1024) # MB
                
                self._samples["cpu"].append(cpu)
                self._samples["ram"].append(ram)
            except Exception:
                break

    def __enter__(self):
        self.start_time = time.time()
        self.stats["start_ram"] = self.process.memory_info().rss / (1024 * 1024)
        
        # Prime psutil (not strictly needed with blocking interval but good practice)
        self.process.cpu_percent(interval=None)
        
        self.running = True
        self._monitor_thread = threading.Thread(target=self._sample)
        self._monitor_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self._monitor_thread:
            self._monitor_thread.join()
            
        end_time = time.time()
        self.stats["duration"] = end_time - self.start_time
        self.stats["end_ram"] = self.process.memory_info().rss / (1024 * 1024)
        
        if self._samples["cpu"]:
            self.stats["avg_cpu"] = mean(self._samples["cpu"])
            self.stats["peak_cpu"] = max(self._samples["cpu"])
        
        if self._samples["ram"]:
            self.stats["avg_ram"] = mean(self._samples["ram"])
            self.stats["peak_ram"] = max(self._samples["ram"])
            
        self.log_report()

    def log_report(self):
        avg_sys_cpu = self.stats['avg_cpu'] / self.cpu_count
        peak_sys_cpu = self.stats['peak_cpu'] / self.cpu_count
        
        logger.info(f"\n{'='*50}\n"
                    f"PERFORMANCE REPORT: {self.step_name}\n"
                    f"{'='*50}\n"
                    f"Duration : {self.stats['duration']:.4f} sec\n"
                    f"Process CPU: {self.stats['avg_cpu']:.1f}% (Avg) | {self.stats['peak_cpu']:.1f}% (Peak) [100% = 1 Core]\n"
                    f"System CPU : {avg_sys_cpu:.1f}% (Avg) | {peak_sys_cpu:.1f}% (Peak) [Normalized Total]\n"
                    f"RAM Usage  : {self.stats['start_ram']:.1f}MB -> {self.stats['end_ram']:.1f}MB | Peak: {self.stats['peak_ram']:.1f}MB\n"
                    f"{'='*50}")

def monitor_performance(step_name: str):
    """Decorator for function performance monitoring."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with PerformanceMonitor(step_name=step_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator

