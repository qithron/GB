import decimal

DC = decimal.BasicContext
DC.prec = 16
decimal.setcontext(DC)

RD = 9 # round(number, RD)
SM = 1 # bezier curve step multiplier

def dec(value='0', context=None, string=True):
    if type(value) != str and hasattr(value, '__len__'):
        g = (decimal.Decimal(str(x) if string else x, context) for x in value)
        return tuple(g)
    if string:
        value = str(value)
    return decimal.Decimal(value, context)
