from finance.wallet import Wallet
from finance import goal, stock
from finance.goal import Goal
from functools import reduce

from finance.owner import Owner


class Plan:

    def __init__(self, owner=Owner, wallets=set, goals=set):
        self.__owner = owner
        self.__wallets = wallets
        self.__goals = goals

    @ property
    def goals(self):
        return self.__goals

    @ property
    def plan_value(self):
        return reduce(lambda total_value, goal_value:
                      total_value + goal_value,
                      [self.goal_value(goal.name)
                       for goal in self.goals], 0)

    @ property
    def total_apportion(self):
        return reduce(lambda total_apportion, goal_apportion:
                      total_apportion + goal_apportion,
                      [goal.apportion for goal in self.goals], 0)

    def get_goal(self, goal_name=str) -> Goal:
        for goal in self.__goals:
            if goal.name == goal_name:
                return goal
        return None

    def get_wallet(self, wallet_name=str) -> Wallet:
        for wallet in self.__wallets:
            if wallet.name == wallet_name:
                return wallet
        return None

    def goal_stocks(self, goal_name) -> tuple:
        goal = self.get_goal(goal_name)
        if goal:
            return goal.stocks
        return None

    def goal_apportion(self, goal_name=str):
        goal = self.get_goal(goal_name)
        if goal:
            return goal.apportion
        return 0

    def number_of_goals(self):
        return len(self.__goals)

    # TODO Check if stock is not in other Goals
    def add_goal(self, new_goal=Goal):
        self.goals.add(new_goal)
        return True

    def remove_goal(self, goal_name=str) -> bool:
        goal = self.get_goal(goal_name)
        if goal:
            self.goals.remove(goal)
            return True
        return False

    def goal_value(self, goal_name):
        return reduce(lambda total_value, value: total_value+value,
                      [stock.total_value for stock
                       in self.goal_stocks(goal_name)], 0)

    def add_wallet(self, wallet):
        if wallet not in self.__wallets:
            self.__wallets.add(wallet)
            return True
        return False

    def add_stock_goal(self, wallet_name=str,
                       stock_name=str, goal_name=str) -> bool:
        stock = self.get_wallet(wallet_name).single_stock(stock_name)
        goal = self.get_goal(goal_name)
        if stock and goal:
            if stock not in goal.stocks:
                goal.stocks.add(stock)
                return True
        return False

    def remove_stock_goal(self, stock_name=str, goal_name=str):
        goal = self.get_goal(goal_name)
        if goal:
            stock = goal.single_stock(stock_name)
            if stock in goal.stocks:
                goal.stocks.remove(stock)
                return True
        return False
