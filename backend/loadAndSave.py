import os
from helpers import *
from consts import *
from components import Member, Joint
import argparse

class LoadAndSave:
    def __init__(self, dirPath):
        self.dirPath = dirPath

    def save(self, filename, results, mList, jList):
        if not os.path.exists(self.dirPath):
            os.makedirs(self.dirPath)
        if filename[-4:] != '.txt':
            f = open(filename+'.txt', 'w')
        else:
            f = open(filename, 'w')
        f.write('All failures are in Newtons of load force!\n\n'+results+'\n\n\n#### Member Specs ####\nEverything in SI units (i.e meters)\n\n')
        for m in mList:
            f.writelines(['---Member '+ifThen(m.l != 0,m.n,m.n+' (external force)')+'---','\nLength: '+str(m2mm(m.l)),' mm\nWidth: '+str(m2mm(m.w)),' mm\nThickness: '+str(m2mm(m.t)),\
            ' mm\nCompression or Tension: '+ifThen(m.comp, 'Compression', 'Tension'),'\nForce: '+str(m.f),' N\nHole distance from edge: '+str(m2mm(m.holeDist)),' mm\nVolume: '+str(mc2cmc(m.v)),\
            ' cm^3\nArea Moment of Inertia: '+str(mq2mmq(m.i)),' mm^4\nBox beam: '+ifThen(m.isBox,'Yes','No'),'\nNumber of hole supports: '+str(m.holeSup)+'\n\n\n'])
        f.write('### Joints ###\n')
        for j in jList:
            f.writelines(['\n\n---Joint '+j.n+'---','\nMembers: '])
            for mm in j.members:
                f.write(mm.n+' ')
        f.close()

    def load(self, filename):
        #os.chdir(self.dirPath)
        f = open(filename, 'r')
        # Skip past the results and to the member specs.
        for line in f:
            if line[0] == '#':
                break
        getNext = False
        num = -1
        data = []
        jData = []
        temp = ''
        lastWord = ''
        # First get the members loaded
        for line in f:
            # Another hash means we've hit the joint section
            if line[0] == '#':
                break
            for word in line.split():
                if getNext:
                    try:
                        # For some reason ifThen would throw exceptions here all the time...
                        if lastWord == 'supports:':
                            temp = int(word)
                        else:
                            temp = float(word)
                    except:
                        # Here, the first case takes care of the name of a member, second takes care of the name of
                        # an external force, the third takes care of box beams, and the else is compression or tension.
                        temp = ifThen([word[-3:]=='---', len(data[num])==0, (word=='Yes' or word=='Compression')],
                                          [word[0:2], word, True], False)
                    data[num].append(temp)
                    getNext = False
                if word[0:3] == '---':
                    num += 1
                    data.append([])
                    getNext = True
                elif word[-1] == ':':
                    getNext = True
                lastWord = word
        num = -1
        getNext = False
        # Time for joints
        for line in f:
            for word in line.split():
                if word[-3:] == '---':
                    num += 1
                    jData.append([])
                    jData[num].append(word[0])
                elif word[-1] == ':' or word[0:3] == '---':
                    pass
                else:
                    jData[num].append(word)
        f.close()
        return self.createLoadedMembers(data, jData)

    def createLoadedMembers(self, mDataArray, jDataArray):
        mems = []
        jays = []
        for Set in mDataArray:
            # Need to convert all numbers back into meters
            mems.append(Member(Set[0],mm2m(Set[1]),mm2m(Set[2]),mm2m(Set[3]),Set[4],Set[5],mm2m(Set[6]),cmc2mc(Set[7]),mmq2mq(Set[8]),Set[9],Set[10]))
        for Set in jDataArray:
            jayMems = []
            for m in Set:
                for M in mems:
                    if m == M.n:
                        jayMems.append(M)
                        break
            jays.append(Joint(Set[0], jayMems))
        # for m in mems:
        #     print m
        # for j in jays:
        #     print j
        return mems, jays

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load a specific file.')
    parser.add_argument('loadName', help='Name of file to be loaded (excluding extension).',
    metavar='filename', type=str)
    args = parser.parse_args()
    a = LoadAndSave(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+os.sep+'designs')
    a.load(args.loadName)
