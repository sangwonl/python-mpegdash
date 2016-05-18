try:
    import unittest2 as unittest
except:
    import unittest


def my_module_suite():
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    return suite
