from ... import RD

def bcc_simple(P0, P1, P2, P3, step=100):
    return tuple([(
        round((1-n/step)**3*P0[0] + 3*(1-n/step)**2*(n/step)*P1[0]
        + 3*(1-n/step)*(n/step)**2*P2[0] + (n/step)**3*P3[0], RD),
        round((1-n/step)**3*P0[1] + 3*(1-n/step)**2*(n/step)*P1[1]
        + 3*(1-n/step)*(n/step)**2*P2[1] + (n/step)**3*P3[1], RD))
        for n in range(0, step+1)])

def bcc():
    pass
