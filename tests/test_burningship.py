from unittest import TestCase

from burningship import BurningShip

#run with python -m unittest in terminal

class TestDemo(TestCase):
    def test_get_file_name(self):
        cur_obj = BurningShip(100, 100, -1, 1, -1, 1, 0, 0)
        fn = cur_obj.get_file_name()
        fn2 = cur_obj.get_file_name()
        assert(fn != fn2)

    def test_solve(self):
        cur_obj = BurningShip(100, 100, -1, 1, -1, 1, 0, 0)
        cur_obj.solve()
        assert(len(cur_obj.img) == 30000)
        assert(cur_obj.img[0] == 255)
        assert(cur_obj.img[242] == 220)

    def test_init(self):
        cur_obj = BurningShip(100, 100, -1, 1, -1, 1, 0, 0)
        assert(cur_obj.max_iter == 50)
        assert(cur_obj.x_min == -1)
