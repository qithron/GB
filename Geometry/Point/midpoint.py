from .point import point

def midpoint(A, B, /):
    '''
    midpoint(A, B, /):
    '''
    if type(A) != point:
        point(*A)
    if type(B) != point:
        point(*B)
    return (A + B)/2
