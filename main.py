from typing import Tuple
import numpy as np
from core import prepare_image, scale_obj_on_img, show_image
from geo.rotate import rotate_arr
from geo.arr_ops import create_transform_arr, multiply, vertexes_to_projective
from mesh_file_utils import read_obj
from vis import draw_lines


if __name__ == "__main__":
    N = 800
    width, height = N, N
    mid = np.array([width, height])//2
    base_color = (125, 120, 255)
    image = prepare_image((width, height, 3))

    # obj = read_obj('cube.obj')
    obj = read_obj('hyper_cube_4d.obj')

    vertexes = np.array(obj['vertexes'])
    lines = np.array(obj['lines'])

    vertexes = vertexes_to_projective(vertexes)
    # rotation = create_transform_arr([
    #     rotate_arr(30, dim=3, axes=0, use_proj=True),
    #     rotate_arr(30, dim=3, axes=1, use_proj=True),
    #     rotate_arr(30, dim=3, axes=2, use_proj=True),
    # ])
    # ! rotation matrix order is important !

    rotation = create_transform_arr([
        # rotate_arr(45, dim=4, axes=[0, 2], use_proj=True),
        rotate_arr(45, dim=4, axes=[0, 3], use_proj=True),
        rotate_arr(45, dim=4, axes=[1, 2], use_proj=True),
        rotate_arr(45, dim=4, axes=[0, 1], use_proj=True),
        # rotate_arr(45, dim=4, axes=[2, 3], use_proj=True),
    ])
    vertexes = multiply(vertexes, rotation)
    vertexes = scale_obj_on_img(vertexes,
                                np.array([N//2]*2),
                                shape=[width, height])
    draw_lines(vertexes, lines, image, base_color)
    show_image(image)
