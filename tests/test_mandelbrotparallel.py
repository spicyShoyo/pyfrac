from unittest import TestCase

from mandelbrotparallel import MandelbrotParallel

#run with python -m unittest in terminal

class TestMandelbrotParallel(TestCase):
    def test_get_file_name(self):
        cur_obj = MandelbrotParallel(100, 100, -1, 1, -1, 1)
        fn = cur_obj.get_file_name()
        assert(fn.split('.')[-1] == "png")
        assert(fn.split('.')[0].split('/')[0] == "out")

    def test_solve(self):
        cur_obj = MandelbrotParallel(100, 100, -1, 1, -1, 1)
        cur_obj.solve()
        assert(len(cur_obj.img) == 10000)

    def test_init(self):
        cur_obj = MandelbrotParallel(100, 100, -1, 1, -1, 1)
        assert(cur_obj.max_iter == 100)
        assert(cur_obj.row_min == -1)
