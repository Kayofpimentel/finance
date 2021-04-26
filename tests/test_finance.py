import unittest
from finance import main
from finance import wallet
from finance.wallet import Wallet
from finance.plan import Plan
from finance.stock import Stock


class TestWalletManagement(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet({'stock1': Stock('stock1', 3, 150)})
        self.stock2 = Stock('stock2', 3, 100)

    def test_add_stock(self):
        self.assertTrue(self.wallet.add_stock(self.stock2))
        self.assertEqual(self.wallet.total_shares_value, 750)
        self.assertFalse(self.wallet.add_stock(self.stock2))
        self.assertIsNotNone(self.wallet.single_stock(self.stock2.name))

    def test_remove_stock(self):
        stock1 = self.wallet.single_stock('stock1')
        self.assertTrue(self.wallet.remove_stock(stock1.name))
        self.assertIsNone(self.wallet.single_stock(stock1.name))
        self.assertEqual(self.wallet.total_shares_value, 0)
        self.assertFalse(self.wallet.remove_stock('abc'))
        self.assertFalse(self.wallet.remove_stock(''))
        self.assertFalse(self.wallet.remove_stock(None))

    def test_show_stocks(self):
        stock3 = Stock('stock1', 3, 150)
        stock1 = self.wallet.single_stock('stock1')
        self.assertIn(stock1, self.wallet.all_stocks)
        self.assertNotIn(stock3, self.wallet.all_stocks)
        self.assertEqual(self.wallet.total_shares_value, 450)

        self.wallet.add_stock(self.stock2)
        self.assertIn(self.stock2, self.wallet.all_stocks)
        self.assertEqual(self.wallet.total_shares_value, 750)

        self.wallet.remove_stock('stock1')
        self.assertNotIn(stock1, self.wallet.all_stocks)
        self.assertEqual(self.wallet.total_shares_value, 300)

    def test_add_balance(self):
        self.assertEqual(self.wallet.balance, 0)
        self.assertTrue(self.wallet.add_balance(200))
        self.assertEqual(self.wallet.balance, 200)
        self.assertFalse(self.wallet.add_balance(-1200))
        self.assertEqual(self.wallet.balance, 200)
        self.assertFalse(self.wallet.add_balance(-200))
        self.assertEqual(self.wallet.balance, 200)
        self.assertFalse(self.wallet.add_balance(0))

    def test_remove_balance(self):
        self.assertEqual(self.wallet.balance, 0)
        self.assertFalse(self.wallet.remove_balance(200))
        self.assertEqual(self.wallet.balance, 0)
        self.assertTrue(self.wallet.add_balance(200))
        self.assertFalse(self.wallet.remove_balance(-1200))
        self.assertEqual(self.wallet.balance, 200)
        self.assertFalse(self.wallet.remove_balance(-200))
        self.assertEqual(self.wallet.balance, 200)
        self.assertTrue(self.wallet.remove_balance(200))
        self.assertEqual(self.wallet.balance, 0)
        self.assertFalse(self.wallet.remove_balance(0))


class TestStockManagement(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet({'stock1': Stock('stock1', 5, 50)})
        self.stock2 = Stock('stock2', 3, 100)

    def test_stock_value(self):
        self.assertEqual(self.wallet.stock_shares_value('stock1'), 250)

    def test_add_share(self):
        self.assertTrue(self.wallet.add_stock_share('stock1', 5))
        self.assertEqual(self.wallet.stock_shares_value('stock1'), 500)
        self.assertFalse(self.wallet.add_stock_share('stock1', -5))
        self.assertFalse(self.wallet.add_stock_share('stock1', '-5'))
        self.assertFalse(self.wallet.add_stock_share('stock1', 0))
        self.assertEqual(self.wallet.stock_shares_value('stock1'), 500)
        self.assertFalse(self.wallet.add_stock_share('stock2', 5))
        self.assertFalse(self.wallet.add_stock_share('stock2', 0))
        self.assertFalse(self.wallet.stock_shares_value('stock2'))

    def test_remove_share(self):
        self.assertTrue(self.wallet.remove_stock_share('stock1', 5))
        self.assertEqual(self.wallet.stock_shares_value('stock1'), 0)
        self.assertFalse(self.wallet.remove_stock_share('stock1', -5))
        self.assertFalse(self.wallet.remove_stock_share('stock1', '-5'))
        self.assertFalse(self.wallet.remove_stock_share('stock1', 0))
        self.assertEqual(self.wallet.stock_shares_value('stock1'), 0)
        self.assertFalse(self.wallet.remove_stock_share('stock2', 5))
        self.assertFalse(self.wallet.remove_stock_share('stock2', 0))
        self.assertFalse(self.wallet.stock_shares_value('stock2'))


class TestPlanManagement(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
