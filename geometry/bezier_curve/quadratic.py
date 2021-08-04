from ... import RD, SM

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