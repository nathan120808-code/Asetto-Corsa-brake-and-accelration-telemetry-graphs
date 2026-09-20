import ctypes
import mmap
import time

class SPageFilePhysics(ctypes.Structure):

    """
    Partial mirror of AC's SPageFilePhysics structure
    Field order/sizes must much AC's actual layout exactly.
    """

    _fields_ = [
        ("packetId", ctypes.c_int),
        ("gas", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("fuel", ctypes.c_float),
        ("gear", ctypes.c_int),
        ("rpms", ctypes.c_int),
        ("steerAngle", ctypes.c_float),
        ("speedKmh", ctypes.c_float),
    ]

class SharedMemoryReader:
    def __init__(self):
        self._mmap = None

    def connect(self) -> bool:
        try:
            self._mmap = mmap.mmap(
                -1, ctypes.sizeof(SPageFilePhysics),
                "Local\\acpmf_physics", access=mmap.ACCESS_READ,
            )
            return True
        except Exception as e:
            print(f"Connection Failed: {e}")
            self._mmap = None
            return False

    def poll(self):
        if self._mmap is None and not self.connect():
            return None
        self._mmap.seek(0)
        physics = SPageFilePhysics.from_buffer_copy(
            self._mmap.read(ctypes.sizeof(SPageFilePhysics))
        )
        if physics.speedKmh == 0 and physics.rpms == 0 and physics.gear ==0:
            return None
        return physics.gas, physics.brake

if __name__ == "__main__":
    reader = SharedMemoryReader()
    print("Polling AC shared memory - Please start a session")
    while True:
        sample = reader.poll()
        if sample is None:
            print("No active session")
        else:
            gas, brake = sample
            print(f"gas={gas:.3f} brake={brake:.3f}")
        time.sleep(0.1)
        