"""
Live gas/brake trace widget (graph)

Ties together telemetry.shared_memory.SharedMemoryReader and
telemetry.input_buffer.InputBuffer, rendering the rolling buffer with
pyqtgraph. This file only handles rendering — data reading and buffering
logic live in their own modules (already tested standalone).
"""

import pyqtgraph as pg
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QWidget, QVBoxLayout


from telemetry.shared_memory import SharedMemoryReader
from telemetry.input_buffer import InputBuffer


class InputTraceWidget(QWidget):
    def __init__(self, window_seconds: float = 6.0, poll_interval_ms: int = 16, parent=None):
        super().__init__(parent)

        self.reader = SharedMemoryReader()
        self.bugger = InputBuffer(window_seconds=window_seconds)
        self.window_seconds = window_seconds

        self.build_ui()

        self.timer = QTimer(self)