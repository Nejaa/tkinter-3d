from __future__ import annotations

from typing import List


class EmptyMatrixException(Exception):
    pass


class InconsistentMatrixException(Exception):
    pass


class IncompatibleMatricesException(Exception):
    pass


class UnsuportedOperationException(Exception):
    pass


class Matrix:
    def __init__(self, data: List[List[float]], padding=False):
        self.height = len(data)
        if self.height == 0:
            raise EmptyMatrixException()

        self.width = len(data[0])

        # find out if there are rows with a different number of elements
        # and throw exception or prepare for normalization
        normalize = False
        for row in data:
            rowLen = len(row)
            if rowLen != self.width:
                if not padding:
                    raise InconsistentMatrixException()
                normalize = True
                if rowLen > self.width:
                    self.width = rowLen

        if normalize:
            for row in data:
                rowLen = len(row)
                if rowLen != self.width:
                    missingCount = self.width - rowLen
                    for i in range(missingCount):
                        row.append(0.0)

        self.data = data

    @staticmethod
    def identity(size: int) -> Matrix:
        return Matrix([[1 if x == y else 0 for x in range(size)] for y in range(size)])

    def __mul__(self, other: Matrix):
        if self.width != other.width or self.height != other.height:
            raise IncompatibleMatricesException()

        newRows = []
        for j in range(self.height):
            newRow = []
            for i in range(self.width):
                newRow.append(self[j][i] * other[j][i])
            newRows.append(newRow)

        return Matrix(newRows)

    def __matmul__(self, other: Matrix):
        if self.width != other.height:
            raise IncompatibleMatricesException()

        newRows = []
        for aj in range(self.height):
            newRow = []
            for bi in range(other.width):
                newCell = 0.0
                for ai in range(self.width):
                    p = self[aj][ai] * other[ai][bi]
                    newCell += p
                newRow.append(newCell)
            newRows.append(newRow)

        return Matrix(newRows)

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return "{}".format(self.data)

    def quick_invert(self) -> Matrix:
        if self.width != 4 and self.height != 4:
            raise UnsuportedOperationException()

        newMatrix = Matrix([
            [self[0][0], self[1][0], self[2][0], 0.0],
            [self[0][1], self[1][1], self[2][1], 0.0],
            [self[0][2], self[1][2], self[2][2], 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

        newMatrix[3][0] = -(self[3][0] * newMatrix[0][0] + self[3][1] * newMatrix[1][0] + self[3][2] * newMatrix[2][0])
        newMatrix[3][1] = -(self[3][0] * newMatrix[0][1] + self[3][1] * newMatrix[1][1] + self[3][2] * newMatrix[2][1])
        newMatrix[3][2] = -(self[3][0] * newMatrix[0][2] + self[3][1] * newMatrix[1][2] + self[3][2] * newMatrix[2][2])
        return newMatrix
