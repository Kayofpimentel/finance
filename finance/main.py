def add(stocks, stock):
    stock_name = stock.pop('name')
    stocks[stock_name] = stock


def remove(stocks, stock):
    return stocks.pop(stock)


def total(stocks):
    totalValue = 0
    for stock in stocks.values():
        totalValue += stock['value'] * stock['number']
    return totalValue
