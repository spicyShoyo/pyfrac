import numpy as np
import pyopencl as cl
import random
import matplotlib.image as mpimg
import uuid

MAX_ITER = 100
RGB_LEN = 3

class Mandelbrot:
    def __init__(self, row_res, col_res, x_min, x_max, y_min, y_max):
        '''
        Init mandelbrot set
        :param row_res: the height of the output image
        :param col_res: the width of the output image
        :param x_min: the x coordinate of the left most pixel
        :param x_max: the x coordinate of the right most pixel
        :param y_min: the y coordinate of the bottom pixel
        :param y_max: the y coordinate of the top pixel
        '''
        self.max_iter = MAX_ITER
        self.img = None

        self.col_length = col_res
        self.row_length = row_res

        self.x_min = x_min
        self.y_min = y_min

        self.col_step = float((x_max - x_min)) / self.col_length
        self.row_step = float((y_max - y_min)) / self.row_length

        self.info = np.zeros(6).astype(np.float32)
        self.info[0] = self.x_min
        self.info[1] = self.y_min
        self.info[2] = self.col_step
        self.info[3] = self.row_step
        self.info[4] = self.col_length
        self.info[5] = self.max_iter

    def solve(self):
        '''
        Solve the mandelbrot set
        :return: none
        '''
        self.img = np.zeros(RGB_LEN * self.row_length * self.col_length).astype(np.int32)

        #PyOpenCL setup
        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]
        ctx = cl.Context([device])
        queue = cl.CommandQueue(ctx)
        mf = cl.mem_flags

        #Buffers setup
        info_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.info)
        res_g = cl.Buffer(ctx, mf.WRITE_ONLY, self.img.nbytes)

        #OpenCL function
        prg = cl.Program(ctx,'''
        __kernel void mandelbrot(
            __global int *res_g, __global float *info_g)
        {
            int width = (int)(info_g[4]);
            int max_iter = (int)(info_g[5]);
            int gid = get_global_id(0);
            int cid = gid % width;
            int rid = width - gid / width - 1;
            double zr = 0;
            double zi = 0;

            double cr = info_g[0] + info_g[2] * cid;
            double ci = info_g[1] + info_g[3] * rid;

            bool over = 0;  //over
            bool assigned = 0;
            bool do_assign = 0;
            int ret = 0;
            double res = 0;

            for(int i=0; i<max_iter; i++) {
                double new_zr = zr * zr + cr - zi * zi;
                double new_zi = 2 * zr * zi + ci;
                zr = new_zr;
                zi = new_zi;
                res = zr * zr + zi * zi;

                over = res > 2;
                do_assign = over & (!assigned);
                int first = 0;
                int second = 0;
                for(int j=0; j<32; j++) {
                    first = first | (((int)res) & do_assign << j);
                    second = second | (ret &(!do_assign) << j);
                }
                ret = (first) | second;
                assigned = assigned | do_assign;
            }
            double r_f = 255 * __cl_pow(ret, 3.0);
            double g_f = 255 * __cl_pow(ret, 0.7);
            double b_f = 255 * __cl_pow(ret, 0.5);
            int r_i = (int)r_f;
            int g_i = (int)g_f;
            int b_i = (int)b_f;

            res_g[gid * 3] = r_i;
            res_g[gid * 3 + 1] = g_i;
            res_g[gid * 3 + 2] = b_i;
        }
        ''').build()
        #execute OpenCL program
        prg.mandelbrot(queue, (self.img.shape[0] // RGB_LEN,), None, res_g, info_g)
        #copy back result
        cl.enqueue_copy(queue, self.img, res_g)

    def save_img(self):
        '''
        save the output image
        :return: the filename of the output image
        '''
        self.img = self.img.reshape((self.row_length, self.col_length, RGB_LEN))
        fn = self.get_file_name()
        mpimg.imsave("./frac/static/" + fn, self.img)
        return fn

    def get_file_name(self):
        '''
        get the file name
        :return: the filename of the output image
        '''
        r = uuid.uuid4()
        return "out/" + str(r) + ".png"
