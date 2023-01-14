""" unit test """
import unittest
from webapp.business_logic import add_defect, delete_defect, \
    add_car_count, delete_car_count
from webapp.stat.models import Defects, CarCounts


class TestUser(unittest.TestCase):
    """ test user """

    def setUp(self):
        """ Инит TestUser """
        self.max_len = 500

    def test_sum(self):
        """ summation юнит-тест """
        print("юнит-тест sum\n")
        self.assertEqual(sum([3, 2]), 5, "равен 5")

    def test_add_defect(self):
        """ add_defect юнит-тест """
        filename = "img12345678.jpg"
        y_pred = 1

        add_defect(filename, y_pred, "none")
        obj = Defects.query.filter(
            Defects.image == filename and
            Defects.object_class == y_pred).first()

        self.assertIsNotNone(obj, "not None")
        self.assertEqual(obj.image, "img12345678.jpg", "равен")
        self.assertEqual(obj.object_class, 1, "равен 1")
        delete_defect(filename, y_pred)

    def test_add_car_count(self):
        """ add_car_count юнит-тест """
        filename = "img12345678.jpg"
        count = 2

        add_car_count(filename, count)
        obj = CarCounts.query.filter(
            CarCounts.image == filename and
            CarCounts.car_count == count).first()

        self.assertIsNotNone(obj, "not None")
        self.assertEqual(obj.image, "img12345678.jpg", "равен")
        self.assertEqual(obj.car_count, 2, "равен 2")
        delete_car_count(filename, count)
