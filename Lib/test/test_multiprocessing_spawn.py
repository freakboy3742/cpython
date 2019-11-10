import os
import unittest

if not os.allows_subprocesses:
    raise unittest.SkipTest('Test requires support for subprocesses.')

import test._test_multiprocessing

from test import support

if support.PGO:
    raise unittest.SkipTest("test is not helpful for PGO")

test._test_multiprocessing.install_tests_in_module_dict(globals(), 'spawn')

if __name__ == '__main__':
    unittest.main()
