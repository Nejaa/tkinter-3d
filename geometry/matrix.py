from __future__ import annotations

from typing import List


class Matrix:
    def __init__(self, data: List[List[float]]):
        self.data = data

    @staticmethod
    def identity(size: int) -> Matrix:
        return Matrix([[1 if x == y else 0 for x in range(size)] for y in range(size)])
