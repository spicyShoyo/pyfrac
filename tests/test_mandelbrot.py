from unittest import TestCase

from mandelbrot import Mandelbrot

#run with python -m unittest in terminal

class TestMandelbrot(TestCase):
    def test_get_file_name(self):
        cur_obj = Mandelbrot(100, 100, -1, 1, -1, 1)
        fn = cur_obj.get_file_name()
        fn2 = cur_obj.get_file_name()
        assert(fn != fn2)

    def test_solve(self):
        cur_obj = Mandelbrot(100, 100, -1, 1, -1, 1)
        cur_obj.solve()
        assert(len(cur_obj.img) == 30000)
        assert(cur_obj.img[0] == 255)
        assert(cur_obj.img[242] == 220)

    def test_init(self):
        cur_obj = Mandelbrot(100, 100, -1, 1, -1, 1)
        assert(cur_obj.max_iter == 50)
        assert(cur_obj.x_min == -1)
