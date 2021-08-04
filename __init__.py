import decimal

DC = decimal.BasicContext
DC.prec = 16
decimal.setcontext(DC)
RD = 9 # round(number, RD)
SM = 1 # bezier curve step multiplier

def dec(obj='0', context=None, string=True):
    if type(obj) == tuple or type(obj) == list:
        lst = (decimal.Decimal(str(x) if string else x, context) for x in obj)
        return tuple(lst)
    if string:
        obj = str(obj)
    return decimal.Decimal(obj, context)
