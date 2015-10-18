# -*- coding: utf-8 -*-

import unittest
from zerg.settings import project
from zerg.mark.compiler import MarkDown


class TestZerg(unittest.TestCase):
    def test_quick_zero(self):
        readme = project.parents[2].join('README.md').path
        MarkDown.from_fpath(readme).generate_fpath(project.parents[2].join('README.html').path)


if __name__ == '__main__':
    unittest.main()