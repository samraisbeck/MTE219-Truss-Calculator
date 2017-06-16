from consts import *
from helpers import *

class StructAnalysis:
    def __init__(self, memberList, jointList):
        self.mems = memberList
        self.joints = jointList

    def calcNormal(self, mems):
        """Note if a member is under compression, hole size is 0"""
        # Max F = (UltNormStress*Area)/RelativeForce
        result = ''
        for i in range(len(mems)):
            res = 0
            if not mems[i].comp:
                middle = ifthen(mems[i].n == "AB", 0.004, 0.006)
                midFail = (beamUltNorm*(mems[i].t*middle)/mems[i].f)
                endFail = (beamUltNorm*(mems[i].holeSup*mems[i].t*(mems[i].w - dowelDiam))/mems[i].f)
                res = ifthen(midFail < endFail, midFail, endFail)
            elif mems[i].isBox:
                res = beamUltNorm*((mems[i].w**2) - (mems[i].w - 2*genThick)**2)/mems[i].f
            else:
                res = (beamUltNorm*(mems[i].t*mems[i].w)/mems[i].f)
            result += "Member "+mems[i].n+": "+str(round(res, 3))+'\n'
        return result

    def calcPinTear(self, mems):
        # Max F = (UltShearStress*2*Thickness*holeDistance)/RelativeForce
        """Only tension members"""
        result = ''
        for i in range(len(mems)):
            res = 0
            res = (beamUltShear*(2*mems[i].holeSup*mems[i].t*mems[i].holeDist)/mems[i].f)
            result += "Member "+mems[i].n+": "+str(round(res, 3))+'\n'
        return result

    def calcBear(self, mems):
        # Max F = (UltNormStress*ContactArea)/RelativeForce
        result = ''
        for i in range(len(mems)):
            res = 0
            res = ifthen(not mems[i].isBox, (beamUltNorm*dowelDiam*mems[i].t*mems[i].holeSup)/mems[i].f, (beamUltNorm*dowelDiam*genThick*2)/mems[i].f)
            result += "Member "+mems[i].n+": "+str(round(res, 3))+'\n'
        return result

    def calcPinShear3(self, joints):
        """Only does pin shear for 3 member joints so far """
        # Max F = (UltShearStress*Area)/RelativeForce
        result = ''
        for i in range(len(joints)):
            if len(joints[i].members) == 3:
                temp = []
                temp.append(pinUltShear*((dowelDiam)**2)*(pi/4)/joints[i].members[0].f)
                temp.append(pinUltShear*((dowelDiam)**2)*(pi/4)/joints[i].members[2].f)
                result += "Joint "+joints[i].n+"\nBetween members "+joints[i].members[0].n+" and "\
                    +joints[i].members[1].n+": "+str(round(temp[0], 3))\
                    +"\nBetween members "+joints[i].members[1].n+" and "\
                    +joints[i].members[2].n+": "+str(round(temp[1], 3))+"\n\n"
            else:
                pass
        return result

    def calcPinBend(self, joints):
        # (obtained from bending moment diagram):
        # 3 point: Max F = (maxMoment*4/Length)/RelativeForce
        # 4 point: Max F = (maxMoment/x)/RelativeForce
        # where x is the distance in from one support to the closest force.
        result = ''
        for i in range(len(joints)):
            res = 0
            res = ifthenelif([joints[i].n == "D", joints[i].n == "B"], [(pinMaxM*4/0.037), pinMaxM/(((4*genThick))*joints[i].members[-1].f)], res)
            if res != 0:
                result += "Joint "+joints[i].n+": "+str(round(res, 3))+'\n'
        return result

    def calcBuckle(self, mems):
        # Max F = ((Pi^2*E*I)/L^2)/RelativeForce
        """Only compression members"""
        result = ''
        for j in range(len(mems)):
            res = (((pi**2)*E*mems[j].i)/((mems[j].l**2)))/mems[j].f
            res = res / 4
            result += "Member "+mems[j].n+": "+str(round(res, 3))+'\n'
        return result

    def calcMass(self, mems, joints):
        # This is going to be off by a bit due to density inconsistencies and
        # glue weight. Also did not account for tapered beams.
        totMem = 0
        for i in range(len(mems)):
            totMem = totMem + mems[i].v
        totMem *= 2
        totJoint = ((dowelDiam**2) * (pi/4))*0.08*(len(joints)-1)
        totJoint += (dowelDiam**2) * (pi/4)*0.045
        return "\nApproximate mass is "+str(round((totMem*memDens + totJoint*jointDens)*1000, 3))+" g"

    def calcAll(self):
        tMems = []
        cMems = []
        externals = []
        internals = []
        for i in range(len(self.mems)):
            if self.mems[i].l == 0:
                externals.append(self.mems[i])
            elif self.mems[i].comp:
                cMems.append(self.mems[i])
            elif not self.mems[i].comp:
                tMems.append(self.mems[i])
        internals = tMems+cMems

        return "\n*****Failure due to Normal Stress***** \n"+self.calcNormal(internals)+"\n*****Failure due to Pin Tear-out***** \n"+\
        self.calcPinTear(tMems)+"\n*****Failure due to Bearing Stress***** \n"+self.calcBear(internals)+"\n*****Failure due to Pin Shear***** \n"+\
        self.calcPinShear3(self.joints)+"*****Failure due to Pin Bend***** \n"+self.calcPinBend(self.joints)+"\n*****Failure due to Buckling***** \n"+\
        self.calcBuckle(cMems)+"\n*****"+self.calcMass(internals, self.joints)+'\n\n'
        # One massive string...
