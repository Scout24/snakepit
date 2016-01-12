import unittest2
import os
import requests_mock
from snakepit import main, add_conda_dist_flavour_prefix, \
    custom_output_filename


class TestSnakepit(unittest2.TestCase):
    def setUp(self):
        self.args = {'--force': True,
                     '--debug': False,
                     '--distribution': 'miniconda',
                     '--build': 0,
                     '--output': '/tmp/snakepit.spec',
                     '<file>': 'src/unittest/testdata/package_from_devpi.yaml'}

    def test_add_conda_dist_flavour_prefix(self):
        input_ = {'conda_dist_flavour': 'miniconda'}
        expected = {'conda_dist_flavour': 'miniconda',
                    'conda_dist_flavour_urlprefix': 'Miniconda'}
        add_conda_dist_flavour_prefix(input_)
        self.assertEquals(expected, input_)

    def test_return_custom_filename_with_directory(self):
        output_filename = custom_output_filename("package.spec", "/some/where")
        self.assertEqual(output_filename, "/some/where/package.spec")

    def test_main__ok_devpi_with_pypi_version_latest_and_pyrun(self):
        self.args['--distribution'] = 'pyrun'
        self.args['<file>'] = 'src/unittest/testdata/lastest_pkg_devpi.yaml'
        main(self.args)
        with open(self.args['--output'], "r") as fp:
            lines = fp.read()
        self.assertIn("package\n", lines)
        # os.remove(args['--output'])

    def test_main__ok_devpi_with_pypi_version_latest_and_miniconda(self):
        self.args['<file>'] = 'src/unittest/testdata/lastest_pkg_devpi.yaml'
        main(self.args)
        with open(self.args['--output'], "r") as fp:
            lines = fp.read()
        self.assertIn("package\n", lines)
        # os.remove(args['--output'])

    def test_main__ok_devpi_with_pypi_version_and_pyrun(self):
        self.args['--distribution'] = 'pyrun'
        main(self.args)
        with open(self.args['--output'], "r") as fp:
            lines = fp.read()
        self.assertIn("package==1.0\n", lines)
        # os.remove(args['--output'])

    def test_main__ok_devpi_with_pypi_version_and_miniconda(self):
        self.args['<file>'] = 'src/unittest/testdata/package_from_devpi.yaml'
        main(self.args)
        with open(self.args['--output'], "r") as fp:
            lines = fp.read()
        self.assertIn("package==1.0\n", lines)
        # os.remove(args['--output'])

    # @unittest2.skipif(True, 'Under Development')
    @requests_mock.Mocker()
    def test_main__ok_pypi_with_pypi_json(self, mocker):
        response = '{"info": {"version": "1.0", "summary": ' \
                   '"text", "license": "Public"}}'
        mocker.get(
            'https://pypi.python.org/pypi/my_package/json',
            status_code=200,
            text=response)
        self.args['<file>'] = 'src/unittest/testdata/package_from_pypi.yaml'
        main(self.args)
        with open(self.args['--output'], "r") as fp:
            lines = fp.read()
        self.assertIn("package==1.0\n", lines)
        # os.remove(args['--output'])
