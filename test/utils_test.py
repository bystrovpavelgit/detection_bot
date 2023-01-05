""" unit test """
import unittest


class TestUser(unittest.TestCase):
    """ test user """

    def setUp(self):
        """ Инит TestUser """
        self.max_len = 500

    def test_sum(self):
        """ summation юнит-тест """
        print("юнит-тест sum\n")
        self.assertEqual(sum([3, 2]), 5, "равен 5")

