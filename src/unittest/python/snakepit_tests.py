import unittest

from snakepit import add_conda_dist_flavour_prefix, custom_output_filename

class TestSnakepit(unittest.TestCase):

    def test_add_conda_dist_flavour_prefix(self):
        input_ = {'conda_dist_flavour': 'miniconda'}
        expected = {'conda_dist_flavour': 'miniconda',
                    'conda_dist_flavour_urlprefix': 'Miniconda'}
        add_conda_dist_flavour_prefix(input_)
        self.assertEquals(expected, input_)

    def test_return_custom_filename_with_directory(self):
        output_filename = custom_output_filename("package.spec", "/some/where")
        self.assertEqual(output_filename, "/some/where/package.spec")