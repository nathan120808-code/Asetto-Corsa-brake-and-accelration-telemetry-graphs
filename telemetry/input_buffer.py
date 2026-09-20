import time
from collections import deque


class InputBuffer:
    """
    Rolling buffer of (timestamp, gas, brake) samples over a time window
    """

    def __init__(self, window_seconds: float = 6.0, max_samples: int = 20000):
        self.window_seconds = window_seconds
        self._t = deque(maxlen=max_samples)
        self._gas = deque(maxlen=max_samples)
        self._brake = deque(maxlen=max_samples)
        self._t0 = time.perf_counter()

    def add(self, gas: float, brake: float):
        now = time.perf_counter() - self._t0
        self._t.append(now)
        self._gas.append(gas)
        self._brake.append(brake)
        self._evict_old(now)

    def _evict_old(self, now: float):
        cutoff = now - self.window_seconds
        while self._t and self._t[0] < cutoff:
            self._t.popleft()
            self._gas.popleft()
            self._brake.popleft()

    def get_series(self):
        """
        returns(timestamps, gas_values, brake_values) as lists.
        """
        return list(self._t), list(self._gas), list(self._brake)

    def __len__(self):
        return len(self._t)

if __name__ == "__main__":
    # sanity test with fake data - remove when done
    buf = InputBuffer(window_seconds = 2.0)

    for i in range(50):
        buf.add(gas=i / 50, brake=1 - i / 50)
        time.sleep(0.05) #simulate -20hz polling

    t, gas, brake = buf.get_series()
    print(f"Buffer holds {len(buf)} samples")
    print(f"Oldest timestamp: {t[0]:.2f}s, newest: {t[-1]:.2f}s")
    print(f"Span: {t[-1] - t[0]:.2f}s (should be <= window_seconds)")
    print(f"First gas/brake: {gas[0]:.2f}/{brake[0]:.2f}")
    print(f"Last gas/brake: {gas[-1]:.2f}/{brake[-1]:.2f}")