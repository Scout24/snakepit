import unittest

from snakepit import update_loaded


class TestSnakepit(unittest.TestCase):

    def test_update_loaded(self):
        defaults = {'spam': 1, 'ham': 2}
        loaded_yaml = {'ham': 3, 'eggs': 4}
        update_loaded(defaults, loaded_yaml)
        expected = {'spam': 1, 'ham': 3, 'eggs': 4}
        self.assertEquals(expected, loaded_yaml)

