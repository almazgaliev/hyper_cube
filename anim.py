from typing import List
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from core import prepare_image, scale_obj_on_img
from geo.arr_ops import create_transform_arr, multiply, vertexes_to_projective
from geo.rotate import rotate_arr
from mesh_file_utils import read_obj
from vis import draw_lines


def angle_fom_index(frame_index):
    return frame_index


class HyperCubeAnimation():
    def __init__(self, image_size: List[int], obj, frame_amount: int):
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("HyperCube")
        self.frame_amount = frame_amount
        self.vertexes = vertexes_to_projective(np.array(obj['vertexes']))
        self.lines = np.array(obj['lines'])
        self.background = prepare_image(image_size)
        self.frame_index = 0
        self.img = self.background.copy()
        # визуализация с анимацией
        plt.imshow(self.img, animated=True)

        # запуск анимации
        self.animation = FuncAnimation(fig=self.fig,
                                       func=self.update_frame,
                                       init_func=self.__first_frame,
                                       frames=self.frames,
                                       blit=True,
                                       interval=10)

    def run(self):
        plt.show()

    # FIX this works slow af
    def save(self, filepath: str):
        if not filepath.endswith(".gif"):
            filepath += ".gif"
        # https://github.com/matplotlib/matplotlib/issues/6985#issuecomment-242860920
        print("Saving animation...")
        self.animation.save(filepath, writer='imagemagick')
        print(f"Animation saved to {filepath}")

    def frames(self):
        for i in range(1, self.frame_amount):
            self.frame_index = i
            yield self.frame_index

    def __first_frame(self):
        vertexes = scale_obj_on_img(self.vertexes,
                                    np.array([N//2]*2),
                                    shape=[width, height])
        draw_lines(vertexes, self.lines, self.img, base_color)
        return plt.imshow(self.img, animated=True),

    def update_frame(self, frame, *fargs):
        angle = angle_fom_index(frame)
        # ! rotation matrix order is important !
        rotation = create_transform_arr([
            rotate_arr(angle, dim=4, axes=[2, 3], use_proj=True),
            rotate_arr(angle, dim=4, axes=[1, 3], use_proj=True),
            rotate_arr(angle, dim=4, axes=[1, 2], use_proj=True),
            rotate_arr(angle, dim=4, axes=[0, 3], use_proj=True),
            rotate_arr(angle, dim=4, axes=[0, 2], use_proj=True),
            rotate_arr(angle, dim=4, axes=[0, 1], use_proj=True),
        ])
        vertexes = multiply(self.vertexes, rotation)
        self.img = self.background.copy()

        vertexes = scale_obj_on_img(vertexes,
                                    np.array([N//2]*2),
                                    shape=[width, height])
        draw_lines(vertexes, self.lines, self.img, base_color)
        return plt.imshow(self.img, animated=True),

    def draw(self):
        self.img = self.background.copy()


if __name__ == "__main__":
    obj = read_obj("./hyper_cube_4d.obj")
    N = 600
    width, height = N, N
    mid = np.array([width, width])//2
    base_color = (125, 120, 255)
    base_color = (255, 0, 0)

    anim = HyperCubeAnimation([width, height, 3], obj, 360)
    anim.run()
    # anim.save("out.gif")
