import unittest

from bot.utils.shared import dict_merge


class UtilsTest(unittest.TestCase):
    def test_dict_merge(self):
        d1 = {
            'a': 1,
            'b': {'a': 1, 'b': 2},
        }
        d2 = {
            'b': {'b': -2, 'c': 3},
            'c': 3
        }
        d3 = {
            'c': -3,
            'd': 4
        }
        self.assertDictEqual(dict_merge(d1, d2, d3), {
            'a': 1,
            'b': {'a': 1, 'b': -2, 'c': 3},
            'c': -3,
            'd': 4
        })


if __name__ == '__main__':
    unittest.main()
