from .. import dec
from .line import line
from .point import point

def intersect(A, B, /):
    '''Intersect of 2 lines.
    a₁x + b₁y + c₁ = 0
    a₂x + b₂y + c₂ = 0
        x' = (c₁b₂ - c₂b₁) / (a₁b₂ - a₂b₁)
        y' = (a₁c₂ - a₂c₁) / (a₁b₂ - a₂b₁)
    '''
    if type(A) == line == type(B):
        pass
    else:
        return None