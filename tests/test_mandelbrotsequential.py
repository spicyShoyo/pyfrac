from unittest import TestCase

from mandelbrotsequential import MandelbrotSequential

#run with python -m unittest in terminal

class TestMandelbrotSequential(TestCase):
    def test_get_file_name(self):
        cur_obj = MandelbrotSequential(100, 100, -1, 1, -1, 1)
        fn = cur_obj.get_file_name()
        assert(fn.split('.')[-1] == "png")
        assert(fn.split('.')[0].split('/')[0] == "out")

    def test_solve_cell(self):
        cur_obj = MandelbrotSequential(100, 100, -1, 1, -1, 1)
        assert(cur_obj.solve_cell(0, 0) == 255)
        assert(cur_obj.solve_cell(0.8, 0.1) == 252.45)

    def test_solve(self):
        cur_obj = MandelbrotSequential(100, 100, -1, 1, -1, 1)
        cur_obj.solve()
        assert(len(cur_obj.res) == 100)
        assert(len(cur_obj.res[0]) == 100)

    def test_init(self):
        cur_obj = MandelbrotSequential(100, 100, -1, 1, -1, 1)
        assert(cur_obj.max_iters == 100)
        assert(cur_obj.row_min == -1)
