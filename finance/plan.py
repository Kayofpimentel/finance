from functools import reduce
from finance.owner import Owner
from finance.wallet import Wallet


class Plan:

    def __init__(self, owner):
        self.__owner = owner
        self.__wallets = {}
        self.__goals = {}

    @property
    def goals(self):
        return [tuple(goal.values()) for goal in self.__goals.values()]

    @property
    def goal(self, name):
        return [tuple(goal.values()) for goal in self.__goals.values()]

    def goal_stocks(self, name):
        return tuple(self.__goals[name]['stocks'])

    def goal_apportion(self, name):
        if name not in self.__goals:
            return 0
        return self.__goals[name]['apportion']

    def create_plan(self, wallets=dict, goals=dict):
        self.__wallets = wallets
        self.__goals = goals

    def number_of_goals(self):
        return len(self.__goals)

    # TODO Check if stock is in wallet
    def add_goal(self, new_goal=tuple, new_apportion=tuple):
        if new_goal[0] in self.__goals:
            return False
        remaining_apportion = 1 - reduce(
            lambda apportion_slice, apportion: apportion_slice+apportion,
            (list_apportion for list_apportion in new_apportion), 0)
        goals = list(self.__goals.keys())
        for goal_index in range(len(new_apportion)):
            self.__goals[goals[goal_index]
                         ]['apportion'] = new_apportion[goal_index]
        self.__goals[new_goal[0]] = {
            'stocks': new_goal[1], 'apportion': remaining_apportion}
        return True

    # TODO Add parameter new apportion
    def remove_goal(self, goal_name=str):
        if goal_name not in self.__goals:
            return False

        reparted_apportion = self.__goals[goal_name]['apportion']
        del self.__goals[goal_name]
        if len(self.__goals) > 0:
            reparted_apportion = reparted_apportion / len(self.__goals)

            new_apportion = {k: {ak: av+reparted_apportion}
                             for k, v in self.__goals.items()
                             for ak, av in v.items() if ak == 'apportion'}

            for goal_name, goal in self.__goals.items():
                goal.update(
                    {'apportion': new_apportion[goal_name]['apportion']})

        return True
