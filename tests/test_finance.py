import unittest
from functools import reduce
from finance import stock
from finance import wallet

from finance.owner import Owner
from finance.plan import Plan
from finance.stock import Stock
from finance.wallet import Wallet
from finance.goal import Goal


class TestWalletManagement(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet(name='wallet1', stocks={Stock(
            'stock1', 3, 150)}, balance=0)
        self.stock2 = Stock('stock2', 3, 100)

    def test_add_stock(self):
        self.assertTrue(self.wallet.add_stock(self.stock2))
        self.assertEqual(self.wallet.total_shares_value, 750)
        self.assertIsNotNone(self.wallet.single_stock(self.stock2.name))
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
        self.assertIn(stock1, self.wallet.stocks)
        self.assertNotIn(stock3, self.wallet.stocks)
        self.assertEqual(self.wallet.total_shares_value, 450)

        self.wallet.add_stock(self.stock2)
        self.assertIn(self.stock2, self.wallet.stocks)
        self.assertEqual(self.wallet.total_shares_value, 750)

        self.wallet.remove_stock('stock1')
        self.assertNotIn(stock1, self.wallet.stocks)
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
        self.wallet = Wallet(name='wallet1', stocks={Stock(
            'stock1', 5, 50)}, balance=0)
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

        self.owner = Owner(name='User1')
        self.stock1 = Stock(name='stock1', share=3, value=150)
        self.stock2 = Stock(name='stock2', share=3, value=100)
        self.stock3 = Stock(name='stock3', share=10, value=12)
        self.stock4 = Stock(name='stock4', share=5, value=150)
        self.wallet1 = Wallet(name='wallet1',
                              stocks={self.stock1, self.stock2, self.stock3}, balance=1000)
        self.wallet2 = Wallet(name='wallet2', stocks={
                              self.stock4}, balance=0)
        self.goal1 = Goal(name='B&H',
                          stocks={self.stock1},
                          apportion=0.6)
        self.goal2 = Goal(name='REIT',
                          stocks={self.stock2},
                          apportion=0.4)
        self.plan = Plan(owner=self.owner,
                         wallets={self.wallet1},
                         goals={self.goal1, self.goal2})

    def test_create_plan(self):
        self.assertEqual(self.plan.number_of_goals(), 2)
        self.assertEqual(self.plan.plan_value, 750)
        self.assertEqual(self.plan.total_apportion, 1)

    def test_add_goal(self):
        goal3 = Goal(name='Unicorn', stocks={
                     self.wallet1.single_stock('stock3')}, apportion=0.2)
        self.assertTrue(self.plan.add_goal(goal3))
        self.assertEqual(self.plan.number_of_goals(), 3)
        self.assertEqual(self.plan.plan_value, 870)
        self.assertNotEqual(self.plan.total_apportion, 1)
        self.assertAlmostEqual(self.plan.goal_apportion('REIT'), 0.4)
        self.assertAlmostEqual(self.plan.goal_apportion('B&H'), 0.6)
        self.assertAlmostEqual(self.plan.goal_apportion('Unicorn'), 0.2)
        self.assertAlmostEqual(self.plan.goal_apportion('Gamble'), 0)

    def test_remove_goal(self):
        self.assertTrue(self.plan.remove_goal('REIT'))
        self.assertEqual(self.plan.number_of_goals(), 1)
        self.assertEqual(self.plan.plan_value, 450)
        self.assertNotEqual(self.plan.total_apportion, 1)
        self.assertAlmostEqual(self.plan.goal_apportion('REIT'), 0)
        self.assertNotEqual(self.plan.goal_apportion('B&H'), 1)
        self.assertAlmostEqual(self.plan.goal_apportion('Cash'), 0)
        self.assertTrue(self.plan.remove_goal('B&H'))
        self.assertAlmostEqual(self.plan.goal_apportion('B&H'), 0)

    def test_add_stock_goal(self):
        self.assertTrue(self.plan.add_stock_goal(
            goal_name='REIT', wallet_name='wallet1', stock_name='stock3'))
        self.assertEqual(self.plan.goal_value('REIT'), 420)
        self.assertEqual(self.plan.plan_value, 870)
        self.assertFalse(self.plan.add_stock_goal(
            goal_name='REIT', wallet_name='wallet1', stock_name='stock4'))
        self.assertFalse(self.plan.add_stock_goal(
            goal_name='ZERO', wallet_name='wallet1', stock_name='stock3'))
        self.assertFalse(self.plan.add_stock_goal(
            goal_name='ZERO', wallet_name='wallet1', stock_name='stock3'))
        self.assertFalse(self.plan.add_stock_goal(
            goal_name='REIT', wallet_name='wallet1', stock_name='stock3'))

    def test_remove_stock_goal(self):
        self.assertTrue(self.plan.remove_stock_goal('stock2', 'REIT'))
        self.assertEqual(self.plan.goal_value('REIT'), 0)
        self.assertEqual(self.plan.plan_value, 450)
        self.assertFalse(self.plan.remove_stock_goal('stock4', 'REIT'))
        self.assertFalse(self.plan.remove_stock_goal('stock3', 'ZERO'))
        self.assertFalse(self.plan.remove_stock_goal('stock4', 'ZERO'))
        self.assertFalse(self.plan.remove_stock_goal('stock2', 'REIT'))
        self.assertTrue(self.plan.add_stock_goal(
            wallet_name='wallet1', stock_name='stock3', goal_name='REIT'))
        self.assertTrue(self.plan.remove_stock_goal('stock3', 'REIT'))

    def test_add_wallet_plan(self):
        self.assertTrue(self.plan.add_wallet(self.wallet2))
        self.assertFalse(self.plan.add_wallet(self.wallet1))


if __name__ == '__main__':
    unittest.main()
