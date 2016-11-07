from __future__ import absolute_import, print_function
import math
import matplotlib.pyplot as plt
import numpy as np
import pyopencl as cl
import time
import random
import matplotlib.image as mpimg

class MandelbrotSequential:
    def __init__(self, row_res, col_res, x_min, x_max, y_min, y_max):
        '''
        Init juliaset
        :param row_res: the height of the output image
        :param col_res: the width of the output image
        :param x_min: the x coordinate of the left most pixel
        :param x_max: the x coordinate of the right most pixel
        :param y_min: the y coordinate of the bottom pixel
        :param y_max: the y coordinate of the top pixel
        '''
        self.max_iters = 100
        self.col_length = col_res
        self.row_length = row_res
        self.col_min = y_min
        self.row_min = x_min
        self.ci_vals = np.linspace(y_min, y_max, num = self.row_length).astype(np.float32)
        self.cr_vals = np.linspace(x_min, x_max, num = self.col_length).astype(np.float32)

    def solve_cell(self, cr, ci):
        '''
        Solve the cell of the given real and imaginary part
        :param cr: real part
        :param ci: imaginary part
        :return: the value of the given cell
        '''
        zr = 0.0
        zi = 0.0
        ret = 0
        for i in range(self.max_iters):
            new_zr = zr**2 + cr - zi * zi
            new_zi = 2 * zr * zi + ci
            zr = new_zr
            zi = new_zi
            length = zr ** 2 + zi ** 2
            if length > 2:
                ret = 255 - i / float(self.max_iters)* 255
                return ret

        ret = 255
        return ret

    def solve(self):
        '''
        Solve the mandelbrot set
        :return: none
        '''
        self.res = []
        for row_idx in range(self.row_length):
            self.res.append([])
            ci = self.ci_vals[row_idx]
            for col_idx in range(self.col_length):
                cr = self.cr_vals[col_idx]
                cell = self.solve_cell(cr, ci)
                self.res[row_idx].append(cell)

    def save_img(self):
        '''
        save the output image
        :return: the filename of the output image
        '''
        fn = self.get_file_name()
        self.res = np.array(self.res)
        mpimg.imsave("./frac/static/" + fn, self.res, cmap = 'Greys_r')
        return fn

    def get_file_name(self):
        '''
        get the file name
        :return: the filename of the output image
        '''
        r = random.randint(0, 100)
        return "out/" + str(r) + ".png"
