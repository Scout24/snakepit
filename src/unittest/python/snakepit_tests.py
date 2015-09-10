import unittest

from snakepit import (update_loaded,
                      add_conda_dist_flavour_prefix,
                      TEMPLATE_FILENAME,
                      TemplateNoteFoundException,
                      default_output_filename,
                      )


class TestSnakepit(unittest.TestCase):

    def test_update_loaded(self):
        defaults = {'spam': 1, 'ham': 2}
        loaded_yaml = {'ham': 3, 'eggs': 4}
        update_loaded(defaults, loaded_yaml)
        expected = {'spam': 1, 'ham': 3, 'eggs': 4}
        self.assertEquals(expected, loaded_yaml)

    def test_add_conda_dist_flavour_prefix(self):
        input_ = {'conda_dist_flavour': 'miniconda'}
        expected = {'conda_dist_flavour': 'miniconda',
                    'conda_dist_flavour_urlprefix': 'Miniconda'}
        add_conda_dist_flavour_prefix(input_)
        self.assertEquals(expected, input_)

