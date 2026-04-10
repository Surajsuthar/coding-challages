import threading


class Store:
    def __init__(self) -> None:
        self._dict = {}
        self._lock = threading.Lock()

    def set(self, key, value):
        with self._lock:
            self._dict[key] = value

    def get(self, key):
        with self._lock:
            return self._dict.get(key)

    def __repr__(self) -> str:
        return f"Store({self._dict})"
