def quadrant(A, /):
    '''
    quadrant(A, /)

    Return a value representing Quadrant of a point, see below:

    0 = origin
    -1 = x-axis
    -2 = y-axis
    1-4 = the four quadrants
    '''
    if len(A) != 2:
        raise IndexError \
        (f'argument take 2 items but {len(A)} were given')
    x, y = A
    if x == 0 == y:
        return 0
    else:
        if x != 0 != y:
            if x > 0:
                if y > 0:
                    return 1
                else:
                    return 4
            else:
                if y > 0:
                    return 2
                else:
                    return 3
        else:
            if x == 0:
                return -1
            else:
                return -2
