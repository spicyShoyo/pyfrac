import numpy as np
import pyopencl as cl
import random
import matplotlib.image as mpimg
import uuid
import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1' #output warnings

class Diamondsquare:
    def __init__(self, n, smooth=0.1):
        '''
        Init diamondsquare
        :param res: the resolution
        :param smooth: smooth value
        '''
        self.res = 2 ** n + 1
        self.smooth = smooth
        self.img = None

    def check_range(self, x, y):
        return x >= 0 and y >= 0 and x < self.res and y < self.res

    def diamond(self, x, y, half_stride):
        ret = 0
        count = 0
        for i in [-1, 1]:
            for j in [-1, 1]:
                diamond_x = x + i * half_stride
                diamond_y = y + j * half_stride
                if self.check_range(diamond_x, diamond_y):
                    count += 1
                    ret += self.img[diamond_y][diamond_x]
        return ret / count

    def square(self, x, y, half_stride):
        ret = 0
        count = 0
        for i in [-1, 1]:
            square_x = x
            square_y = y + i * half_stride
            if self.check_range(square_x, square_y):
                count += 1
                ret += self.img[square_y][square_x]
            square_x = x + i * half_stride
            square_y = y
            if self.check_range(square_x, square_y):
                count += 1
                ret += self.img[square_y][square_x]
        return ret / count

    def diamondsquare(self, x, y, stride):
        if stride <= 1:
            return;
        half_stride = stride // 2
        mid_x = x + half_stride
        mid_y = y + half_stride
        if self.check_range(mid_x, mid_y):
            self.img[mid_y][mid_x] = self.smooth * random.random() * random.choice([-1, 1])
            self.img[mid_y][mid_x] += self.diamond(mid_x, mid_y, half_stride)

        for i in [-1, 1]:
            edge_x = mid_x
            edge_y = mid_y + i * half_stride
            if self.check_range(edge_x, edge_y):
                self.img[edge_y][edge_x] = self.smooth * random.random() * random.choice([-1, 1])
                self.img[edge_y][edge_x] += self.square(edge_x, edge_y, half_stride)
            edge_x = mid_x + i * half_stride
            edge_y = mid_y
            if self.check_range(edge_x, edge_y):
                self.img[edge_y][edge_x] = self.smooth * random.random() * random.choice([-1, 1])
                self.img[edge_y][edge_x] += self.square(edge_x, edge_y, half_stride)

        for i in [0, 1]:
            for j in [0, 1]:
                self.diamondsquare(x+i*half_stride, y+j*half_stride, half_stride)

    def solve(self):
        '''
        Solve the diamondsquare noise
        :return: none
        '''
        self.img = np.zeros((self.res, self.res))
        for i in [0, self.res-1]:
            for j in [0, self.res-1]:
                self.img[i][j] = random.random()
        self.diamondsquare(0, 0, self.res)
        # res = np.zeros((self.res, self.res)).astype(np.int32)
        # res = 255 * self.img
        # self.img = res

    def save_img(self):
        '''
        save the output image
        :return: the filename of the output image
        '''
        fn = self.get_file_name()
        mpimg.imsave("./frac/static/" + fn, self.img, cmap='Greys_r')
        return fn

    def get_file_name(self):
        '''
        get the file name
        :return: the filename of the output image
        '''
        r = uuid.uuid4()
        return "out/" + str(r) + ".png"
