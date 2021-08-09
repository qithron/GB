from .polygon import polygon

def area(POL, /):
    '''
    area(POL, /):
    '''
    if type(POL) != polygon:
        raise TypeError(
        f'argument expected a {polygon} but {type(POL)} where given')
