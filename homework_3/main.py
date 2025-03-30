import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin




class FileSaveMixin:
    def save_to_file(self, filename, fmt="%d"):
        np.savetxt(filename, self.content, fmt=fmt)

class SummationHashMixin:
    def __hash__(self):
        return int(np.sum(self.content))

class PrintMixin:
    def __str__(self):
        return str(self.content)


class MyMatrix(NDArrayOperatorsMixin, SummationHashMixin, FileSaveMixin, PrintMixin):
    def __init__(self, data):
        self._content = np.array(data)
        self._multiply_cache = {}

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_data):
        self._content = np.array(new_data)

    def __eq__(self, other):
        if isinstance(other, MyMatrix):
            return np.array_equal(self.content, other.content)
        return False

    def __hash__(self):
        return int(np.sum(self.content))

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        array_inputs = (x.content if isinstance(x, MyMatrix) else x for x in inputs)
        result = getattr(ufunc, method)(*array_inputs, **kwargs)
        if isinstance(result, tuple):
            return tuple(self.__class__(item) for item in result)
        else:
            return self.__class__(result)

    def __matmul__(self, other):
        key = (hash(self), hash(other))
        if key in self._multiply_cache:
            return self._multiply_cache[key]

        if self.content.shape[1] != other.content.shape[0]:
            raise ValueError("Некорректные размеры для матричного умножения")

        product_matrix = self.__class__(np.matmul(self.content, other.content))
        self._multiply_cache[key] = product_matrix
        return product_matrix


def save_hashes_to_file(obj1, obj2, filename="hash.txt"):
    with open(filename, "w") as f:
        f.write(f"Hash of first: {hash(obj1)}\n")
        f.write(f"Hash of second: {hash(obj2)}\n")


def main():
    np.random.seed(0)

    matA = MyMatrix(np.random.randint(0, 10, (3, 3)))
    matB = MyMatrix(np.random.randint(0, 10, (3, 3)))

    tmp_data = matA.content.copy()
    tmp_data[0, 0] += 1
    tmp_data[0, -1] -= 1

    while np.array_equal(tmp_data, matA.content):
        tmp_data[0, 0] += 1
        tmp_data[0, -1] -= 1

    matC = MyMatrix(tmp_data)

    matD = MyMatrix(matB.content.copy())

    assert hash(matA) == hash(matC), "Хэши matA и matC должны совпадать"
    assert not np.array_equal(matA.content, matC.content), "Содержимое matA и matC не должно совпадать"
    assert np.array_equal(matB.content, matD.content), "matB и matD должны совпадать"
    assert not np.array_equal((matA @ matB).content, (matC @ matD).content), \
        "Произведения matA @ matB и matC @ matD должны отличаться"

    matA.save_to_file("A.txt")
    matB.save_to_file("B.txt")
    matC.save_to_file("C.txt")
    matD.save_to_file("D.txt")

    resultAB = matA @ matB
    resultCD = matC @ matD

    resultAB.save_to_file("AB.txt")
    resultCD.save_to_file("CD.txt")

    save_hashes_to_file(resultAB, resultCD, filename="hash.txt")


if __name__ == "__main__":
    main()
