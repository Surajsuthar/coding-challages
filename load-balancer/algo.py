import threading

BACKENDS = [
    {"host": "localhost", "port": 8080},
    {"host": "localhost", "port": 8081},
    {"host": "localhost", "port": 8082},
]


class RoundRobin:
    def __init__(self):
        self.current_index = 0
        self.index_lock = threading.Lock()

    def get_next_backend(self):
        """Thread-safe round-robin selection."""
        with self.index_lock:
            backend = BACKENDS[self.current_index % len(BACKENDS)]
            self.current_index += 1
            return backend
