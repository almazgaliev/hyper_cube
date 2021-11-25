import numpy as np
from numpy import cos, sin
from typing import List, Union
from .arr_ops import multiply


# возвращает матрицу поворота
def rotate_arr2d(ang) -> np.ndarray:
    ang = np.deg2rad(ang)
    return np.array([[cos(ang), -sin(ang)],
                     [sin(ang), cos(ang)]])


# возвращает матрицу поворота в проективных координатах 3 мерного пространства
# def rotate_arr(ang, axis):
#     ang = np.deg2rad(ang)
#     if axis == 2:
#         return np.array([[cos(ang), -sin(ang), 0, 0],
#                          [sin(ang), cos(ang), 0, 0],
#                          [0, 0, 1, 0],
#                          [0, 0, 0, 1]])
#     elif axis == 1:
#         return np.array([[cos(ang), 0, sin(ang), 0],
#                          [0, 1, 0, 0],
#                          [-sin(ang), 0, cos(ang), 0],
#                          [0, 0, 0, 1]])
#     elif axis == 0:
#         return np.array([[1, 0,        0,         0],
#                          [0, cos(ang), -sin(ang), 0],
#                          [0, sin(ang), cos(ang),  0],
#                          [0, 0,        0,         1]])

def rotate_arr(ang: float,
               dim: int = 2,
               axes: Union[List, int] = 2,
               use_proj: bool = False):
    """Функция создающая матрицу поворота в n мерном пространстве
    Args:
        ang (float): угол в градусах
        dim (int, optional): Размерность пространства. Defaults to 2.
        axes (Union[List, int], optional): вектора вокруг которых происходит
        вращение. Defaults to 2.
        use_proj (bool,optional):создать матрицу (n+1,n+1) вместо (n,n) Defaults to False

    Raises:
        Exception: Если число векторов не верно или размерность пространства
        не верно указана

    Returns:
        np.ndarray: Матрица поворота в N мерном пространстве
    """
    if dim <= 1:
        raise Exception("Ti Eblo")
    if dim == 2:
        indexes = np.array([[x, y] for x in range(2)
                           for y in range(2)])
    else:
        if type(axes) != list:
            if dim != 3:
                raise Exception("axes should be list")
            axes = [axes]
        indexes = list((set(range(dim)) - set(axes)))
        if len(indexes) != dim - len(axes):
            raise Exception("axis index error")
        indexes.sort()

        indexes = np.array([[x, y] for x in indexes
                            for y in indexes])
    matrix = np.eye(dim+use_proj)
    matrix[indexes[:, 0], indexes[:, 1]] = rotate_arr2d(ang).flatten()
    return matrix


# # функция поворота
# def rotate(v, ang, axis):
#     return multiply(v, rotate_arr(ang, axis))
