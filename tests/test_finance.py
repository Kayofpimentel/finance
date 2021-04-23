import unittest
from finance import main


class TestStockManagement(unittest.TestCase):

    def setUp(self):
        self.wallet = {'stock1': {'value': 150, 'number': 3}, 'balance': 0}
        self.stock2 = {'name': 'stock2', 'value': 100, 'number': 3}

    def test_total_stock_value(self):
        self.assertEqual(main.total(self.wallet), 450)

    def test_add_stock(self):
        main.add(self.wallet, self.stock2)
        self.assertEqual(self.wallet['stock2'], {'value': 100, 'number': 3})
        self.assertEqual(main.total(self.wallet), 750)

    def test_remove_stock(self):
        stock = 'stock1'
        main.remove(self.wallet, stock)
        self.assertNotIn(stock, self.wallet)
        self.assertEqual(main.total(self.wallet), 0)

    def test_show_stocks(self):
        stocks_string = main.show_stocks(self.wallet)
        self.assertIn('stock1', stocks_string)
        self.assertIn('value', stocks_string)
        self.assertIn('number', stocks_string)

        main.add(self.wallet, self.stock2)
        stocks_string = main.show_stocks(self.wallet)
        self.assertIn('stock2', stocks_string, f'\n{stocks_string}')
        self.assertIn('Total Wallet: 750', stocks_string, f'\n{stocks_string}')
        self.assertIn('Balance', stocks_string, f'\n{stocks_string}')

    def test_get_balance(self):
        balance = main.get_balance(self.wallet)
        self.assertEqual(balance, self.wallet['balance'])

    def test_add_balance(self):
        balance = main.add_balance(self.wallet, 0)
        self.assertEqual(balance, self.wallet['balance'])

        balance = main.add_balance(self.wallet, 350)
        self.assertNotEqual(balance, 0)
        self.assertEqual(balance, self.wallet['balance'])

        balance = main.add_balance(self.wallet, 500)
        self.assertEqual(balance, self.wallet['balance'])

        main.add_balance(self.wallet, -1000)
        self.assertEqual(850, self.wallet['balance'])

        main.add_balance(self.wallet, '100')
        self.assertEqual(850, self.wallet['balance'])

        main.add_balance(self.wallet, 'abc')
        self.assertEqual(850, self.wallet['balance'])


if __name__ == '__main__':
    unittest.main()
