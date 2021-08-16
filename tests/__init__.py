try:
    import unittest
except ImportError:
    import unittest2 as unittest


def my_module_suite():
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    return suite
