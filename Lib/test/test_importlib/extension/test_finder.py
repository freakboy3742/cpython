from test.support import is_apple_mobile
from test.test_importlib import abc, util

machinery = util.import_importlib('importlib.machinery')

import unittest
import warnings


class FinderTests(abc.FinderTests):

    """Test the finder for extension modules."""

    def find_module(self, fullname):
        if is_apple_mobile:
            # Apple mobile platforms require a specialist loader that uses
            # .fwork files as placeholders for the true `.so` files.
            loaders = [
                (
                    self.machinery.AppleFrameworkLoader,
                    [
                        ext.replace(".so", ".fwork")
                        for ext in self.machinery.EXTENSION_SUFFIXES
                    ]
                )
            ]
        else:
            loaders = [
                (
                    self.machinery.ExtensionFileLoader,
                    self.machinery.EXTENSION_SUFFIXES
                )
            ]

        importer = self.machinery.FileFinder(util.EXTENSIONS.path, *loaders)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            return importer.find_module(fullname)

    def test_module(self):
        self.assertTrue(self.find_module(util.EXTENSIONS.name))

    # No extension module as an __init__ available for testing.
    test_package = test_package_in_package = None

    # No extension module in a package available for testing.
    test_module_in_package = None

    # Extension modules cannot be an __init__ for a package.
    test_package_over_module = None

    def test_failure(self):
        self.assertIsNone(self.find_module('asdfjkl;'))


(Frozen_FinderTests,
 Source_FinderTests
 ) = util.test_both(FinderTests, machinery=machinery)


if __name__ == '__main__':
    unittest.main()
