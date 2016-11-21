import numpy as np
import pyopencl as cl
import random
import matplotlib.image as mpimg
import uuid
import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1' #output warnings

class Blur:
    def __init__(self, res, smooth=5):
        '''
        Init Blur
        :param res: the resolution
        :param smooth: smooth value
        '''

        self.res = res
        self.smooth = smooth
        self.info = np.zeros(2).astype(np.int32)
        self.info[0] = self.res
        self.info[1] = self.smooth
        self.img = None

    def solve(self):
        '''
        Solve the blur noise
        :return: none
        '''
        rand = np.random.rand((self.res+2*self.smooth)**2).astype(np.float32)
        self.img = np.zeros(self.res**2).astype(np.int32)
        #PyOpenCL setup
        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]
        ctx = cl.Context([device])
        queue = cl.CommandQueue(ctx)
        mf = cl.mem_flags

        #Buffers setup
        rand_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=rand)
        info_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.info)
        res_g = cl.Buffer(ctx, mf.WRITE_ONLY, self.img.nbytes)

        #OpenCL function
        prg = cl.Program(ctx,'''
        __kernel void blur(
            __global int *info_g, __global int *res_g, __global float *rand_g)
        {
            int res = info_g[0];
            int smooth = info_g[1];
            int rand_res = res + 2 * smooth;
            int grid_width = 1 + 2 * smooth;
            int rid = get_global_id(0);
            int cid = get_global_id(1);

            int rand_rid = rid + smooth;
            int rand_cid = cid + smooth;
            float cur_sum = 0;
            for(int i=0; i<grid_width; i++) {
                int grid_rid = rand_rid - smooth + i;
                for(int j=0; j<grid_width; j++) {
                    int grid_cid = rand_cid - smooth + j;
                    cur_sum += rand_g[grid_rid*rand_res+grid_cid];
                }
            }
            res_g[rid*res+cid] = 255 * (cur_sum) / (float)(grid_width*grid_width);
        }
        ''').build()
        #execute OpenCL program
        prg.blur(queue, (self.res, self.res), None, info_g, res_g, rand_g)
        #copy back result
        cl.enqueue_copy(queue, self.img, res_g)
        self.img = self.img.reshape((self.res, self.res))
        print(rand)
        print(self.img)

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
