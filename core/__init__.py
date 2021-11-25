from typing import List
import numpy as np
import matplotlib.pyplot as plt
from geo.arr_ops import move, scale

# отображение изображения и сохранение в файл


def show_image(image):
    image = image.transpose((1, 0, 2))[::-1, :, :]
    # Image.fromarray(image).save("out.png")
    plt.imshow(image)
    plt.show()


def prepare_image(shape=(1000, 1000, 3)) -> np.ndarray:
    return np.zeros(shape=shape, dtype=np.uint8)


def scale_obj_on_img(v: np.ndarray, xy: np.ndarray, shape: List):
    dims = v.shape[1]-1
    min_ = np.min(v, axis=0)[:-1]
    v = move(v, -min_)
    c = np.min(xy / np.max(v, axis=0)[:2])

    v = scale(v, np.array([c-1]*dims))
    img_mid = np.array([0]*dims)
    img_mid[:2] = np.array(shape)//2
    obj_mid = ((np.min(v, axis=0) + np.max(v, axis=0))//2)[:-1]
    vec = img_mid - obj_mid
    vec[2:] = 0
    return move(v, vec).astype(np.int32)
