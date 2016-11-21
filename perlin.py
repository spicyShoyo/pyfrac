import numpy as np
import pyopencl as cl
import random
import matplotlib.image as mpimg
import uuid
import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1' #output warnings

class Perlin:
    def __init__(self, res):
        '''
        Init perlin
        :param res: the resolution
        :param smooth: smooth value
        '''

        self.res = res
        self.info = np.zeros(1).astype(np.int32)
        self.info[0] = self.res
        self.img = None

    def solve(self):
        '''
        Solve the perlin noise
        :return: none
        '''
        gradient_x = np.random.rand(((1+self.res)**2)).astype(np.float32)
        gradient_y = np.ones((1+self.res)**2).astype(np.float32)
        gradient_y = gradient_y - gradient_x ** 2
        for i in range(gradient_x.size):
            gradient_y[i] = gradient_y[i] ** 0.5
            gradient_x[i] = random.choice([-1, 1]) * gradient_x[i]
            gradient_y[i] = random.choice([-1, 1]) * gradient_y[i]

        self.img = np.zeros(self.res**2).astype(np.int32)

        #PyOpenCL setup
        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]
        ctx = cl.Context([device])
        queue = cl.CommandQueue(ctx)
        mf = cl.mem_flags

        #Buffers setup
        gradient_x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=gradient_x)
        gradient_y_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=gradient_y)
        info_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.info)
        res_g = cl.Buffer(ctx, mf.WRITE_ONLY, self.img.nbytes)

        #OpenCL function
        prg = cl.Program(ctx,'''
        __kernel void perlin(
            __global int *info_g, __global int *res_g, __global float *gradient_x_g, __global float *gradient_y_g)
        {
            int res = info_g[0];
            int rid = get_global_id(0);
            int cid = get_global_id(1);

            float x = cid;
            float y = rid;
            int x0 = (int)x;
            int x1 = x0 + 1;
            int y0 = (int)y;
            int y1 = y0 + 1;

            float sx = x - (float)x0;
            float sy = y - (float)y0;

            float n0, n1, ix0, ix1, value;
            float dx, dy;
            int ix, iy;

            int ix_arr[2] = {x0, x1};
            int iy_arr[2] = {y0, y0};
            float* n_arr[2] = {&n0, &n1};
            for(int m=0; m<2; ++m) {
                ix = ix_arr[m];
                iy = iy_arr[m];
                dx = x - (float)ix;
                dy = y - (float)iy;
                *n_arr[m] = dx * gradient_x_g[iy*(1+res)+ix] + dy * gradient_y_g[iy*(1+res)+ix];
            }
            ix0 = (1.0 - sx) * n0 + sx * n1;
            iy_arr[0] = y1;
            iy_arr[1] = y1;
            for(int m=0; m<2; ++m) {
                ix = ix_arr[m];
                iy = iy_arr[m];
                dx = x - (float)ix;
                dy = y - (float)iy;
                *n_arr[m] = dx * gradient_x_g[iy*(1+res)+ix] + dy * gradient_y_g[iy*(1+res)+ix];
            }
            ix0 = (1.0 - sx) * n0 + sx * n1;

            value = (1.0 - sy) * ix0 + sy * ix1;
            res_g[rid*res+cid] = 255 * (value + 1) / 2;
        }
        ''').build()
        #execute OpenCL program
        prg.perlin(queue, (self.res, self.res), None, info_g, res_g, gradient_x_g, gradient_y_g)
        #copy back result
        cl.enqueue_copy(queue, self.img, res_g)
        self.img = self.img.reshape((self.res, self.res))

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
