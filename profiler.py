# For Profiling performance

import time
import math

from printer import Printer

class Profiler(object):
    def __init__(self):
        self.reset()
        self.printer = Printer()

    def measure(self, description):
        end = time.process_time()
        total = (end - self.start) * 1_000
        since_last = (end - self.intermediate_start) * 1_000
        self.intermediate_start = end
        self.printer.print(f"{description} (total: {total:.5g}ms, sinceLast: {since_last:.5g}ms)")

    def reset(self):
        self.start = time.process_time()
        self.intermediate_start = self.start