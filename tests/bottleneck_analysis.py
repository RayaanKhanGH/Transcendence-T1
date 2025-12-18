import os

# AGGRESSIVE RESOURCE CONTROL
# strictly enforce single-threaded execution for all major math libraries
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TORCH_NUM_THREADS"] = "1"
os.environ["JOBLIB_MULTIPROCESSING"] = "0"

import logging

import time
import json
import psutil

from datetime import datetime
from src.system_core import Core
from src.utils.performance_monitor import PerformanceMonitor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def run_bottleneck_test(query: str = "quantum computing trends 2025"):
    """
    Runs the advanced bottleneck test.
    """
    print("="*60)
    print(" TRANSCENDENCE T1 - ADVANCED BOTTLENECK ANALYSIS")
    print("="*60)
    p = psutil.Process()
    print(f"Target Process: {p.name()} (PID: {p.pid})")
    try:
        # Nuclear Option: Physically bind to Core 0 to enforce hard cap of 100% (1 core)
        p.cpu_affinity([0])
        print("Hardware Constraint: Process bound exclusively to CPU Core 0")
    except Exception as e:
        print(f"Warning: Could not set CPU affinity: {e}")
        
    print(f"Test Query: '{query}'")
    print("-" * 60)

    # Initialize Core (Cold Start Measurement)
    with PerformanceMonitor("System Initialization (Cold Start)") as init_mon:
        core = Core()

    # Run Pipeline (Warm Execution Measurement)
    with PerformanceMonitor("Full Pipeline Execution") as exec_mon:
        # Mocking or using real execution
        # Note: If no API keys are present, this will be mostly logical flows
        try:
            result = core.run_pipeline({"query": query})
        except Exception as e:
            logger.error(f"Pipeline crashed during test: {e}")
            return

    # Generate Report
    print("\n" + "="*60)
    print(" FINAL BOTTLENECK REPORT")
    print("="*60)
    
    # Analyze init stats
    print(f"1. Initialization:")
    print(f"   - Duration: {init_mon.stats['duration']:.4f}s")
    print(f"   - RAM Cost: {init_mon.stats['end_ram'] - init_mon.stats['start_ram']:.2f} MB")

    # Analyze Execution stats
    print(f"\n2. Pipeline Execution:")
    print(f"   - Duration: {exec_mon.stats['duration']:.4f}s")
    print(f"   - CPU (Process Avg/Peak): {exec_mon.stats['avg_cpu']:.1f}% / {exec_mon.stats['peak_cpu']:.1f}%")
    print(f"   - CPU (System Avg/Peak): {exec_mon.stats['avg_cpu']/exec_mon.cpu_count:.1f}% / {exec_mon.stats['peak_cpu']/exec_mon.cpu_count:.1f}%")
    print(f"   - RAM (Avg/Peak): {exec_mon.stats['avg_ram']:.1f}MB / {exec_mon.stats['peak_ram']:.1f}MB")

    
    # Save detailed JSON
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "initialization": init_mon.stats,
        "execution": exec_mon.stats
    }
    
    filename = f"bottleneck_report_{int(time.time())}.json"
    with open(filename, "w") as f:
        json.dump(report_data, f, indent=4)
        
    print(f"\n[+] Detailed report saved to: {filename}")
    print("="*60)

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "latest advancements in solid state batteries 2024"
    run_bottleneck_test(query)
