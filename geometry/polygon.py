from .. import dec
from .bezier_curve import bcl
from .distance import distance
from .point import point
from .slope import slope
from math import acos, cos, sin, degrees, radians

class polygon:
    __slots__ = 'points', '__len'
    def __init__(self, P0, P1, P2, *Pn):
        # self.points = tuple([P0,P1,P2] + list(Pn))
        self.points = tuple([e if type(e) == point else point(*e)
                             for e in [P0,P1,P2] + list(Pn)])
        self.__len = len(self.points)

    def __call__(self):
        return self.points

    def __str__(self):
        return f'polygon{self.points}'

    def __repr__(self):
        return f'polygon{self.points}'
    
    def __iter__(self):
        for v in self.points:
            yield v
    
    def __len__(self):
        return self.__len

    def get_points(self):
        return tuple(
            [bcl((self.points[v-1], self.points[v]))
            for v in range(1, len(self.points))]
            + list(bcl((self.points[-1], self.points[0]))))

    # def area(self):
        # return None

    # def perimeter(self):
        # return None

    # def geogebra(self, d=0.3):
        # c = f'Circle({self.points[0]}, {d})'
        # p = str(self.points)[1:-1]
        # v = ', '.join([f'Vector({self.points[i-1]}, {self.points[i]})'
              # for i in range(1,len(self.points))]
              # + [f'Vector({self.points[-1]},{self.points[0]})'])
        # return 'PyPolygon = {' + f'{c}, {p}, {v}' + '}'

    @staticmethod
    def polygon_from_2_point(P0, P1, width=1): # width in pixel
        if P0 == P1: return None
        slp = slope(P0, P1)
        wid = dec(width)/2
        P0x, P0y = dec(P0)
        P1x, P1y = dec(P1)
        if not slp:
            m, n, s = (0, 1, False) if slp == 0 else (1, 0, True)
            v = False if P0[m] - P1[m] > 0 else True
            q1, q2, q3, q4 = P0[n]-wid, P1[n]-wid, P1[n]+wid, P0[n]+wid
            if s:
                if v: a,b,c,d = (q4,P0y), (q3,P1y), (q2,P1y), (q1,P0y)
                else: a,b,c,d = (q1,P0y), (q2,P1y), (q3,P1y), (q4,P0y)
            else:
                if v: a,b,c,d = (P0x,q1), (P1x,q2), (P1x,q3), (P0x,q4)
                else: a,b,c,d = (P0x,q4), (P1x,q3), (P1x,q2), (P0x,q1)
        else:
            if None: pass
            elif P1x > 0 and P1y > 0: # quadrant 1
                PA=(P1x,P0y); E0x,E0y=P0x+wid,P0y; E1x,E1y=P1x-wid,P1y
            elif P1x < 0 and P1y > 0: # quadrant 2
                PA=(P0x,P1y); E0x,E0y=P0x,P0y+wid; E1x,E1y=P1x,P1y-wid
            elif P1x < 0 and P1y < 0: # quadrant 3
                PA=(P1x,P0y); E0x,E0y=P0x-wid,P0y; E1x,E1y=P1x+wid,P1y
            elif P1x > 0 and P1y < 0: # quadrant 4
                PA=(P0x,P1y); E0x,E0y=P0x,P0y-wid; E1x,E1y=P1x,P1y+wid
            # rotating (x,y) with center point (a,b) and v° rotating angle:
            #   x' = a + (x-a) * cos(v°) – (y-b) * sin(v°)
            #   y' = b + (x-a) * sin(v°) + (y-b) * cos(v°)
            ang = degrees(acos(distance(P0,PA)/distance(P0,P1)))
            an0, an1 = radians(ang-90), radians(ang+90)
            a = P0x + (E0x-P0x) * cos(an0) - (E0y-P0y) * sin(an0),\
                P0y + (E0x-P0x) * sin(an0) + (E0y-P0y) * cos(an0)
            b = P1x + (E1x-P1x) * cos(an1) - (E1y-P1y) * sin(an1),\
                P1y + (E1x-P1x) * sin(an1) + (E1y-P1y) * cos(an1)
            c = P1x + (E1x-P1x) * cos(an0) - (E1y-P1y) * sin(an0),\
                P1y + (E1x-P1x) * sin(an0) + (E1y-P1y) * cos(an0)
            d = P0x + (E0x-P0x) * cos(an1) - (E0y-P0y) * sin(an1),\
                P0y + (E0x-P0x) * sin(an1) + (E0y-P0y) * cos(an1)
        return polygon(a, b, c, d)

    @staticmethod
    def polygon_from_points(width=1, *args): # width in pixel
        '''Create new polygon object from 2 points or more with given width.
        Used formula:
            rotating (x,y) with center point (a,b) and v° rotating angle:
                x' = a + (x-a) * cos(v°) – (y-b) * sin(v°)
                y' = b + (x-a) * sin(v°) + (y-b) * cos(v°)
        '''
        if len(args) < 2:
            return None
        def points(S, E):
            slp = slope(S, E)
            Sx, Sy = dec(S)
            Ex, Ey = dec(E)
            if not slp:
                m, n, s = (0, 1, False) if slp == 0 else (1, 0, True)
                v = False if S[m] - E[m] > 0 else True
                q1, q2, q3, q4 = S[n]-wid, E[n]-wid, E[n]+wid, S[n]+wid
                if s:
                    if v: a,b,c,d = (q4,Sy), (q3,Ey), (q2,Ey), (q1,Sy)
                    else: a,b,c,d = (q1,Sy), (q2,Ey), (q3,Ey), (q4,Sy)
                else:
                    if v: a,b,c,d = (Sx,q1), (Ex,q2), (Ex,q3), (Sx,q4)
                    else: a,b,c,d = (Sx,q4), (Ex,q3), (Ex,q2), (Sx,q1)
            else:
                if None: pass
                elif Ex > 0 and Ey > 0: # quadrant 1
                    PA=(Ex,Sy); E0x,E0y=Sx+wid,Sy; E1x,E1y=Ex-wid,Ey
                elif Ex < 0 and Ey > 0: # quadrant 2
                    PA=(Sx,Ey); E0x,E0y=Sx,Sy+wid; E1x,E1y=Ex,Ey-wid
                elif Ex < 0 and Ey < 0: # quadrant 3
                    PA=(Ex,Sy); E0x,E0y=Sx-wid,Sy; E1x,E1y=Ex+wid,Ey
                elif Ex > 0 and Ey < 0: # quadrant 4
                    PA=(Sx,Ey); E0x,E0y=Sx,Sy-wid; E1x,E1y=Ex,Ey+wid
                ang = degrees(acos(distance(S,PA)/distance(S,E)))
                an0, an1 = radians(ang-90), radians(ang+90)
                a = Sx + (E0x-Sx) * cos(an0) - (E0y-Sy) * sin(an0),\
                    Sy + (E0x-Sx) * sin(an0) + (E0y-Sy) * cos(an0)
                b = Ex + (E1x-Ex) * cos(an1) - (E1y-Ey) * sin(an1),\
                    Ey + (E1x-Ex) * sin(an1) + (E1y-Ey) * cos(an1)
                c = Ex + (E1x-Ex) * cos(an0) - (E1y-Ey) * sin(an0),\
                    Ey + (E1x-Ex) * sin(an0) + (E1y-Ey) * cos(an0)
                d = Sx + (E0x-Sx) * cos(an1) - (E0y-Sy) * sin(an1),\
                    Sy + (E0x-Sx) * sin(an1) + (E0y-Sy) * cos(an1)
        lst = [], []
        wid = dec(width)/2
        for i in range(2, len(args)):
            S, E = args[i-2:i]
            if S == E:
                continue
        
        if len(lst) < 3:
            return None
        return polygon(*lst)
