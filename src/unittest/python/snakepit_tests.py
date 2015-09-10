import unittest

from mock import patch, Mock

from snakepit import (update_loaded,
                      add_conda_dist_flavour_prefix,
                      locate_template,
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

    @patch('snakepit.osp.isfile', Mock(return_value=True))
    def test_locate_template_returns_filename_if_file_found(self):
        self.assertEquals(TEMPLATE_FILENAME, locate_template())

    @patch('snakepit.osp.isfile', Mock(return_value=False))
    def test_locate_template_raises_exception_if_file_not_found(self):
        self.assertRaises(TemplateNoteFoundException, locate_template)

    @patch('snakepit.osp.isfile')
    @patch('snakepit.osp.join', Mock(return_value='expected'))
    def test_locate_template_finds_file_near_module(self, isfile_mock):
        isfile_mock.side_effect = [False, True]
        self.assertEquals('expected', locate_template())

    def test_default_output_filename(self):
        self.assertEquals('mypackage.spec',
                          default_output_filename(
                              {'pypi_package_name': 'mypackage'}))

