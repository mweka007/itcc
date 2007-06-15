# $Id$
'''calculate the torsion diff of two cycloalkane'''

import sys
import math
from itcc.tools import periodnumber
from itcc.molecule import read, molecule, tools
from itcc.ccs2 import detectloop

__revision__ = '$Rev$'
__all__ = ['catordiff']

debug = False

Angle = periodnumber.genPNclass(-math.pi, math.pi)

def catordiff(mol1, mol2, loop=None):
    assert isinstance(mol1, molecule.Molecule)
    assert isinstance(mol2, molecule.Molecule)
    tors1 = getlooptor(mol1, loop)
    tors2 = getlooptor(mol2, loop)
    return tordiff(tors1, tors2)

def getlooptor(mol, loop):
    if loop is None:
        loops = detectloop.loopdetect(mol)[1]
        assert len(loops) == 1
        loop = loops[0]
    return tools.calclooptor(mol, loop)

def tordiff(tors1, tors2):
    pi = math.pi
    assert len(tors1) == len(tors2)
    result = None
    results = []
    n = len(tors1)
    for newtors2 in varytors(tors2):
        diff = max([(tors1[i] - newtors2[i] - pi) % (pi*2) + pi for i in range(n)])
        if result is None or result > diff:
            result = diff
        if debug:
            results.append((diff, newtors2))
    if debug:
        results.sort()
        print 'Torsion of mol1: ', ['%6.1f' % math.degrees(float(tor)) for tor in tors1]
        print 'Torsion of mol2: ', ['%6.1f' % math.degrees(float(tor)) for tor in tors2]
        print 'Torsion of mol3: ', ['%6.1f' % math.degrees(float(tor)) for tor in results[0][1]]
        print ['%5.1f' % math.degrees(result[0]) for result in results]
    return result

def varytors(tors):
    negtors = [-tor for tor in tors]
    vartors = [tors * 2, tors[::-1]*2, negtors*2, negtors[::-1]*2]
    for subvartors in vartors:
        for idx in range(len(tors)):
            yield subvartors[idx:idx+len(tors)]

def main():
    if len(sys.argv) != 3:
        import os.path
        print 'Usage: %s xyzfname1 xyzfname2' % os.path.basename(sys.argv[0])
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))
    print math.degrees(catordiff(mol1, mol2))

if __name__ == '__main__':
    main()
