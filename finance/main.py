from .wallet import Wallet
from .plan import Plan


def add(wallet, stock):
    wallet[stock.name] = stock


def remove(wallet, stock):
    return wallet.pop(stock)


def total(wallet):
    totalValue = 0
    for stock in wallet:
        if 'balance' not in stock:
            totalValue += wallet[stock]['value'] * wallet[stock]['number']
    return totalValue


def show_stocks(wallet):
    stocks_string = ''
    for stock in wallet.keys():
        if stock != 'balance':
            stock_value = wallet[stock]["value"]
            stock_number = wallet[stock]["number"]
            stock_total = stock_value * stock_number
            stocks_string += f'{stock}: value: {stock_value} number: {stock_number} total: {stock_total}\n'
    stocks_string += f'Total Wallet: {total(wallet)}'
    stocks_string += f'Balance: {wallet["balance"]}'
    return stocks_string


def add_balance(wallet, value):
    balance = wallet['balance']
    if not isinstance(value, int):
        return balance
    elif value < 0:
        return balance
    wallet['balance'] += value
    return wallet['balance']


def remove_balance(wallet, value):
    balance = wallet['balance']
    if not isinstance(value, int):
        return balance
    elif value < 0 or value > balance:
        return balance
    wallet['balance'] -= value
    return wallet['balance']


def get_balance(wallet):
    return wallet['balance']
