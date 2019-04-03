
from threading import Lock

class AtomicCounter:

    def __init__(self, initial: int = 0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self.value = initial
        self._lock = Lock()

    def increment(self, num: int = 1):
        """Atomically increment the counter by num (default 1) and return the
        new value.
        """
        with self._lock:
            self.value += num
            return self.value