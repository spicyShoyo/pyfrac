import imageio
import uuid
import os
from julia import Julia
from mandelbrot import Mandelbrot
from burningship import BurningShip
from demo import Demo
import os.path

FRAC_TYPE_DIC = {"Julia": Julia, "Mandelbrot": Mandelbrot, "Demo": Demo, "BurningShip": BurningShip}

class FracGIF:
    def __init__(self, frac_type, row_res, col_res, x_min, x_max, y_min, y_max, cr, ci):
        '''
        Init FracGIF
        :param frac_type: the type of the fractal
        :param row_res: the height of the output image
        :param col_res: the width of the output image
        :param x_min: the x coordinate of the left most pixel
        :param x_max: the x coordinate of the right most pixel
        :param y_min: the y coordinate of the bottom pixel
        :param y_max: the y coordinate of the top pixel
        :param cr: cr value if needed
        :param ci: ci value if needed
        '''
        self.frac_class = FRAC_TYPE_DIC[frac_type]
        self.row_res = row_res
        self.col_res = col_res
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.cr = cr
        self.ci = ci
        self.frame_fn = []
        self.frame_list = []

    def get_new_x(self, cur_x):
        '''
        get the next x value
        :param cur_x: current x value
        :return: the enlarged x
        '''
        return self.x_min + cur_x / self.row_res * (self.x_max - self.x_min)

    def get_new_y(self, cur_y):
        '''
        get the next y value
        :param cur_y: current y value
        :return: the enlarged y
        '''
        return self.y_min + cur_y / self.col_res * (self.y_max - self.y_min)

    def solve(self):
        '''
        solve the fractal for 31 frames
        '''
        cur_frac_obj = self.frac_class(self.row_res, self.col_res, self.x_min, self.x_max, self.y_min, self.y_max, self.cr, self.ci)
        cur_frac_obj.solve()
        cur_fn = cur_frac_obj.save_img()
        self.frame_fn.append("./frac/static/" + cur_fn)

        for i in range(30):
            new_x_min = self.get_new_x(0.05 * self.row_res)
            new_x_max = self.get_new_x(0.95 * self.row_res)
            new_y_min = self.get_new_y(0.05 * self.col_res)
            new_y_max = self.get_new_y(0.95 * self.col_res)
            cur_frac_obj = self.frac_class(self.row_res, self.col_res, new_x_min, new_x_max, new_y_min, new_y_max, self.cr, self.ci)
            cur_frac_obj.solve()
            cur_fn = cur_frac_obj.save_img()
            self.frame_fn.append("./frac/static/" + cur_fn)
            self.x_min = new_x_min
            self.x_max = new_x_max
            self.y_min = new_y_min
            self.y_max = new_y_max

    def save_gif(self):
        '''
        save the output gif
        :return: the filename of the output gif
        '''
        fn = self.get_file_name()
        with imageio.get_writer("./frac/static/" + fn, mode='I') as writer:
            for filename in self.frame_fn:
                image = imageio.imread(filename)
                writer.append_data(image)
                os.remove(filename)
        return fn

    def get_file_name(self):
        '''
        get the file name
        :return: the filename of the output image
        '''
        r = uuid.uuid4()
        return "out/" + str(r) + ".gif"
