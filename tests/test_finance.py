import unittest
from finance import main


class TestStockManagement(unittest.TestCase):

    def setUp(self):
        self.stocks = {'stock1': {'value': 150, 'number': 3}}

    def test_total_stock_value(self):
        self.assertEqual(main.total(self.stocks), 450)

    def test_add_stock(self):
        stock2 = {'name': 'stock2', 'value': 100, 'number': 3}
        main.add(self.stocks, stock2)
        self.assertEqual(self.stocks['stock2'], {'value': 100, 'number': 3})
        self.assertEqual(main.total(self.stocks), 750)

    def test_remove_stock(self):
        stock = 'stock1'
        main.remove(self.stocks, stock)
        self.assertNotIn(stock, self.stocks)
        self.assertEqual(main.total(self.stocks), 0)


if __name__ == '__main__':
    unittest.main()
