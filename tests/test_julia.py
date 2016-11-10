from unittest import TestCase

from julia import Julia

#run with python -m unittest in terminal

class TestJulia(TestCase):
    def test_get_file_name(self):
        cur_obj = Julia(100, 100, -1, 1, -1, 1)
        fn = cur_obj.get_file_name()
        fn2 = cur_obj.get_file_name()
        assert(fn != fn2)

    def test_solve(self):
        cur_obj = Julia(100, 100, -1, 1, -1, 1)
        cur_obj.solve()
        assert(len(cur_obj.img) == 30000)
        assert(cur_obj.img[0] == 255)
        assert(cur_obj.img[242] == 255)

    def test_init(self):
        cur_obj = Julia(100, 100, -1, 1, -1, 1)
        assert(cur_obj.max_iter == 100)
        assert(cur_obj.x_min == -1)
