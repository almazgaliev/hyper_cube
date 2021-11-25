from typing import Callable, List
import numpy as np
from itertools import accumulate


def multiply(vertexes, arr):
    return arr.dot(vertexes.T).T


# возвращает матрицу сдвига
def move_arr(moves: np.ndarray):
    ar_f = np.eye(len(moves) + 1)
    ar_f[:-1:, -1] = moves
    return ar_f


# возвращает матрицу масштабирования
def scale_arr(ks: np.ndarray):
    n = len(ks) + 1
    ar_f = np.eye(n)
    np.reshape(ar_f, ar_f.size)[:-1:n+1] = ks  # (ar_f.size)
    return ar_f


# возвращает матрицу отражения
def reflect_arr(smt):
    s = []
    for el in smt:
        if el:
            s.append(-1)
        else:
            s.append(1)
    return scale_arr(np.array(s))


# функция масштабирования
def scale(v: np.ndarray, ks: np.ndarray):
    return multiply(v, scale_arr(ks))


# функция отражения
def reflect(v: np.ndarray, smt):
    return multiply(v, reflect_arr(smt))


# функция сдвига
def move(v: np.ndarray, moves: np.ndarray):
    return multiply(v, move_arr(moves))


def create_transform_arr(arr_list: List[np.ndarray]) -> np.ndarray:
    """Создает матрицу для комбинации афинных преобразований

    Args:
        arr_list (List[np.ndarray]): список матриц афинных преобразований
    """
    # return list(accumulate(arr_list, np.dot))[-1]
    out = np.eye(arr_list[0].shape[0])
    for index in range(len(arr_list) - 1, -1, -1):
        out = out.dot(arr_list[index])
    return out


def transform_builder(arr_list: List[np.ndarray]) -> Callable:
    """Создает функцию для применения комбинации преобразований к координатам

    Args:
        arr_list (List[np.ndarray]): список матриц афинных преобразований
    """
    a = create_transform_arr(arr_list)
    return lambda b: a.dot(b.T).T


# функция перевода в проективные координаты
def vertexes_to_projective(v: np.ndarray) -> np.ndarray:
    return np.hstack([v.copy(),
                     np.ones(shape=(v.shape[0], 1))])
