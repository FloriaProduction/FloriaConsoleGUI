from typing import Union

class Counter:
    def __init__(self):
        self._data: dict[str, int] = {}
    
    def add(self, key: str, amt: int = 1, default_value: int = 0):
        if key not in self._data:
            self._data[key] = default_value
        self._data[key] += amt
    
    def pop(self, key: str, amt: int = 1):
        if key not in self._data:
            raise ValueError(f'Key "{key}" not found')
        self._data[key] -= amt
    
    def get(self, key: str) -> Union[int, None]:
        return self._data.get(key)
    
    def clearAll(self):
        self._data.clear()