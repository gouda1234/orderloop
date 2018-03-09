
# book = (Buy/Sell :: Bool, Fee :: Double, Orders :: [(Double,Double)])

testData = [ (True, 0.998, [(0.07286665, 0.53483973),(0.07386665, 0.53483973)])
             , (False, 0.998, [(0.17100119, 0.53483978),(0.16100119, 0.33483978)])
             , (False, 0.998, [(0.01373397, 0.09145823), (0.01273397, 0.9145823)])
]


def loopPrice(books):
    # length all books > 0
    while all([b[2] for b in books ]):
        amount = 10000000
        price = 1
        # find the max amount for the best price of the loop/chain
        # and the overall price (roi when it is a loop)
        for buy, fee, orders in reversed(books):
            p,q = orders[0]
            if buy:
                price = price / p * fee
                if q * fee < amount:
                    amount = p * q
                else:
                    amount = p * amount / fee

            else:
                price = price * p * fee
                if p * q * fee < amount:
                    amount = q
                else:
                    amount = (amount / fee) / p

        def remove(orders, a):
            p,q = orders[0]
            # rounding error
            if abs(q - a) < 0.000001:
                orders= orders[1:]
            else:
                orders[0] = (p, q - a)
            return orders

        inc = []
        # go forward again with that amount and collect the amounts/prices
        # remove the amounts from the orderbooks and repeat
        for i,(buy, fee, orders) in enumerate(books):
            p,q = orders[0]
            if buy:
                amount /= p
                inc.append((p,amount))
                books[i]=(buy,fee, remove(orders, amount))
                amount *= fee

            else:
                inc.append((p, amount))
                books[i]=(buy,fee, remove(orders, amount))
                amount = amount * p * fee

        yield(price, inc)


def getAmounts(books, pMin = 1):
    amounts = []
    #collect the amounts for a min overall price (for example 1 for arb loops)
    for p,os in loopPrice(books):
        if p > pMin:
            amounts.append(os)
        else:
            break
    return(amounts)

def sumAmounts(x):
    s = []
    # sum up the amounts and take the worst price
    for i in range(0,len(x[0])):
        s.append((x[-1][i][0], sum([v[i][1] for v in x]) ))
    return s


a = getAmounts(testData, 0)
print(sumAmounts(a))
