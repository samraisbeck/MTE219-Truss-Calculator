from consts import *
from helpers import ifThen, ifthenelif

class Member:
    def __init__(self, name, l, w, t, comp, f, holeDist, v = 0, i = 0, box = False, holeSupport = 0):
        """
        name        : Name of the member, usually corresponds to the joints it's connected to.
        l           : Length from hole center to hole center of the member
        w           : Width of the member
        t           : Thickness of the member
        comp        : Is it a compressive member? boolean
        f           : Force relative to the applied load P
        holeDist    : Distance from the center of the joint hole to the end edge of the member
        v           : Volume (NOTE: only provide if the member is not a normal one, and isn't a box)
        i           : Area moment of inertia (only provide if member is not normal or a box)
        box         : Is it a box beam? boolean
        holeSupport : Number of additional hole supports

        NOTE: All distance measurements are in meters, volume in m^3,
        inertia in m^4, for easy calculations.
        Once saved, it converts to mm for easy reading.

        Also, for a box beam, thickness and width are the two side lengths.
        """
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
        self.holeSup = holeSupport+1 #number of extra hole supports
        if self.isBox != 0:
            self.i = ifThen(self.i == 0, (self.w*(self.t**3))/12 - ((self.w-2*genThick)*((self.t-2*genThick)**3))/12, self.i)
            self.v = ifThen(self.v == 0, (2*self.holeDist+self.l)*((self.w**2)-(self.w-2*genThick)**2)-((dowelDiam**2)*(pi/4)*genThick*4), self.v)
        else:
            self.i = ifThen(self.i == 0, self.w*(self.t**3)/12, self.i)
            if self.v == 0:
                self.v = ((self.l + self.holeDist*2 - 2*(dowelDiam**2) * (pi/4))*self.w*self.t)\
                        + ifThen([self.n == 'CD', self.n == 'BC'], [(self.holeDist*self.w - (dowelDiam**2) * (pi/4)) * self.t, 2*((self.holeDist*self.w - (dowelDiam**2) * (pi/4)) * self.t)], 0)

    def __str__(self):
        return '['+self.n+', '+str(self.l)+', '+str(self.w)+', '+str(self.t)+', '+str(self.f)+', '+\
        str(self.holeDist)+', '+str(self.v)+', '+str(self.i)+', '+str(self.holeSup-1)+', '+str(self.comp)+', '+str(self.isBox)+']'

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
