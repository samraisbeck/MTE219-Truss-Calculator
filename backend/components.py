from consts import *
from helpers import ifThen, ifthenelif

class Member:
    def __init__(self, name, l, w, t, comp, f, holeDist, v = 0, i = 0, box = False, holeSupport = 1):
        """ Note that l is length from hole to hole """
        # also, treat reactions as members for the sake of pin shear
        self.n = name # AB, BC, CD, etc
        self.l = l #length
        self.w = w #width
        self.t = t #thickness
        self.comp = comp #is it a compression member?
        self.f = f #force
        self.holeDist = holeDist #distance from edge to hole
        self.v = v #volume
        self.i = i #area moment of inertia
        self.isBox = box #is it a box beam?
        self.holeSup = holeSupport #number hole supports (no extras is considered 1!)
        if self.isBox != 0:
            self.i = ifThen(self.i == 0, (self.w**4)/12 - ((self.w-2*genThick)**4)/12, self.i)
            self.v = ifThen(self.v == 0, (2*self.holeDist+self.l)*((self.w**2)-(self.w-2*genThick)**2)-((dowelDiam**2)*(pi/4)*genThick*4), self.v)
        else:
            self.i = ifThen(self.i == 0, self.w*(self.t**3)/12, self.i)
            if self.v == 0:
                self.v = ((self.l + self.holeDist*2 - 2*(dowelDiam**2) * (pi/4))*self.w*self.t)\
                        + ifThen([self.n == 'CD', self.n == 'BC'], [(self.holeDist*self.w - (dowelDiam**2) * (pi/4)) * self.t, 2*((self.holeDist*self.w - (dowelDiam**2) * (pi/4)) * self.t)], 0)

    def __str__(self):
        return '['+self.n+', '+str(self.l)+', '+str(self.w)+', '+str(self.t)+', '+str(self.comp)+', '+str(self.f)+', '+\
        str(self.holeDist)+', '+str(self.v)+', '+str(self.i)+', '+str(self.isBox)+', '+str(self.holeSup)+']'

class Joint:
    def __init__(self, name, members):
        """ Put the members in order they appear from viewing it from the side.
            Stay consistent which side you view from. """
        self.n = name # A, B, C, etc
        self.members = members

    def getMemberNames(self):
        names = ''
        for m in self.members:
            names += ' '+m.n
        return names

    def __str__(self):
        return '['+self.n+','+self.getMemberNames()+']'
