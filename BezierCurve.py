from . import decimal, dec, RD, SM

def is_int(x):
    return True if type(x) == int else (x).is_integer()

def int_try(obj):
    if type(obj) == int:
        return obj
    elif type(obj) == float:
        return int(obj) if is_int(obj) else obj
    return tuple([int(x) if is_int(x) else x for x in obj])

def slope(A, B, /):
    x1, y1 = dec(A)
    x2, y2 = dec(B)
    if x1 == x2 and y1 == y2:
        return None
    with decimal.localcontext() as ctx:
        ctx.prec = decimal.RX
        ctx.traps[decimal.DivisionByZero] = False
        m = (y2 - y1)/(x2 - x1)
    return +m.normalize()

###############################################################################

def bcl_simple(P0, P1, step=100):
    return tuple([(
        round((1-n/step)*P0[0] + n/step*P1[0], RD),
        round((1-n/step)*P0[1] + n/step*P1[1], RD))
        for n in range(0, step+1)])

def bcl(P0, P1): # using formula
    if P0 == P1: return (P0,)
    s = abs(P1[0]-P0[0]), abs(P1[1]-P0[1])
    if s[0] >= s[1]:
        s, u = s[0], 1-P0[0]%1
    else: s, u = s[1], 1-P0[1]%1
    lst = [(round((1-(t+u)/s)*P0[0] + (t+u)/s*P1[0], RD),
            round((1-(t+u)/s)*P0[1] + (t+u)/s*P1[1], RD))
            for t in range(0, int(s+1-u))]
    if u: lst.insert(0,P0)
    if (s-u)%1: lst.append(P1)
    return tuple(lst)

def bcl_v4(P0, P1): # custom method
    if P0 == P1: return (int_try(P0),)
    slp = slope(P0, P1)
    # linear to which axis? x or y?
    m, n, s = (0, 1, False) if (slp == 0) or (slp and\
              (abs(slp) < 1 or (abs(slp) == 1 and P0[0]%1 <= P0[1]%1)))\
              else (1, 0, True)
    # directions? positive or negative?
    pd, pb = (0, 1) if P0[m]-P1[m] < 0 else (1, 0)
    # is start and end point int?
    ii = is_int(P0[m]), is_int(P1[m])
    # int of start and end point
    ip = int(P0[m]) if ii[0] else int(P0[m]//1) + pb,\
         int(P1[m]) if ii[1] else int(P1[m]//1) + pd
    # int is the best :v
    if not slp: w = int(a[pd][n]) if is_int(a[pd][n]) else a[pd][n]
    # recalculating slope if > 1
    elif abs(slp) > 1: slp = slope((P0[1],P0[0]), (P1[1],P1[0]))
    # creating list except start or end point if float
    if slp:
        lst = []
        o = True
        for v in range(ip[pd], ip[pb]+1):
            w = int_try(round(P0[n] + slp*v - slp*P0[m], RD))
            p = (w, v) if s else (v, w)
            if o: o, u = False, w//1
            else:
                if not is_int(w) and u != w//1:
                    t = int_try(round((w//1 + slp*P0[m] - P0[n])/slp, RD))
                    q = (u+1, t) if s else (t, u+1)
                    lst.append(q)
                u = w//1
            lst.append(p)
    else: lst = [(w, v) if s else (v, w) for v in range(ip[pd], ip[pb]+1)]
    if not ii[pd]: lst.insert(0, int_try(a[pd])) # if start point float
    if not ii[pb]: lst.append(int_try(a[pb])) # and if end point too
    return tuple(lst if pb else reversed(lst))

###############################################################################

def bcq_simple(P0, P1, P2, step=100):
    return tuple([(
        round((1-n/step)**2*P0[0]
        + 2*(1-n/step)*(n/step)*P1[0]
        + (n/step)**2*P2[0], RD),
        round((1-n/step)**2*P0[1]
        + 2*(1-n/step)*(n/step)*P1[1]
        + (n/step)**2*P2[1], RD))
        for n in range(0, step+1)])

def bcq(P0, P1, P2): # using formula
    # P0 == P1 == P2
    if a.count(P0) == 3: return (P0,)
    # P1 == P0/2+P2/2
    elif P1 == (P0[0]/2+P2[0]/2, P0[1]/2+P2[1]/2):
        s = abs(P2[0]-P0[0]), abs(P2[1]-P0[1])
        if s[0] >= s[1]: s, u = s[0], 1-P0[0]%1
        else:            s, u = s[1], 1-P0[1]%1
    # P0 == P2
    elif P0[0] == P0[1] == P2[0] == P2[1]:
        s = max(abs(P0[0] - P1[0])*2, abs(P0[1] - P1[1])*2)*SM
        return tuple([(round((1-t/s)**2*P0[0]
                       + 2*(1-t/s)*(t/s)*P1[0]
                       + (t/s)**2*P2[0], RD),
                       round((1-t/s)**2*P0[1]
                       + 2*(1-t/s)*(t/s)*P1[1]
                       + (t/s)**2*P2[1], RD))
                       for t in range(0, int(s+1))
                       if t/s <= 0.5])
    # P0x == P2x or P0y == P2y
    elif P0[0] == P2[0] or P0[1] == P2[1]:
        if P0[1] == P2[1]:
            m, n = 0, 1
        else: m, n = 1, 0
        # s = (Points, Control, Intersect)
        s = abs(P2[m] - P0[m]), abs(P1[n] - P0[n]),\
            abs(P1[m] - (P0[m]/2 + P2[m]/2))
        s = max(s[0], s[1]*2, (s[2]+s[0]/2)*2)
        u = 1-P0[m]%1
    # P0 != P2
    elif P0 != P2:
        if abs(P0[0] - P2[0]) >= abs(P0[1] - P2[1]):
            m, n = 0, 1
        else: m, n = 1, 0
        if abs(P0[n] - P1[n]) >= abs(P2[n] - P1[n]):
            o = 0
        else: o = 2
        # s = (Points, Control, Intersect)
        s = abs(P2[m] - P0[m]), abs(P1[n] - a[o][n]),\
            abs(P1[m] - (P0[m]/2 + P2[m]/2))
        s = max(s[0], s[1]*2, (s[2]+s[0]/2)*2)
        u = 1-P0[m]%1
    s *= SM
    lst = [(round((1-(t+u)/s)**2*P0[0]
            + 2*(1-(t+u)/s)*((t+u)/s)*P1[0]
            + ((t+u)/s)**2*P2[0], RD),
            round((1-(t+u)/s)**2*P0[1]
            + 2*(1-(t+u)/s)*((t+u)/s)*P1[1]
            + ((t+u)/s)**2*P2[1], RD))
            for t in range(0, int(s+1-u))]
    if u: lst.insert(0,P0)
    if (s-u)%1: lst.append(P2)
    return tuple(lst)

###############################################################################

def bcc_simple(P0, P1, P2, P3, step=100):
    return tuple([(
        round((1-n/step)**3*P0[0] + 3*(1-n/step)**2*(n/step)*P1[0]
        + 3*(1-n/step)*(n/step)**2*P2[0] + (n/step)**3*P3[0], RD),
        round((1-n/step)**3*P0[1] + 3*(1-n/step)**2*(n/step)*P1[1]
        + 3*(1-n/step)*(n/step)**2*P2[1] + (n/step)**3*P3[1], RD))
        for n in range(0, step+1)])

def bcc():
    pass

