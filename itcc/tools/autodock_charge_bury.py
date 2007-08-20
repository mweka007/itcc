# $Id$

import sys
import math
from cStringIO import StringIO

from itcc.tools import dlg, pdbq_large_charge
from itcc.tools.pdb import Pdb
from itcc.tools import c60

def disq(coord1, coord2):
    return sum((coord1-coord2)**2)

def expose_area(protein, ligand, atoms):
    r1 = 4.8
    r2 = 2.8
    r2h = 2.5
    
    r2q = r2 * r2
    r2hq = r2h * r2h
    
    for atom in atoms:
        coord = ligand.coords[atom.idx]
        coords = [x for x in (c60.c60()* r1 + coord)]
        for i in range(len(ligand.atoms)):
            if i == atom.idx:
                continue
            for idx in range(len(coords))[::-1]:
                coord = coords[idx]
                try:
                    if (ligand.atoms[i] == 'H' and disq(coord, ligand.coords[i]) <= r2hq) \
                        or (ligand.atoms[i] != 'H' and disq(coord, ligand.coords[i]) <= r2q):
                        del coords[idx]
                except:
                    print i
                    raise
        
        for i in range(len(protein.atoms)):
            for idx in range(len(coords))[::-1]:
                coord = coords[idx]
                if (protein.atoms[i] == 'H' and disq(coord, protein.coords[i]) <= r2hq) \
                    or (protein.atoms[i] != 'H' and disq(coord, protein.coords[i]) <= r2q):
                    del coords[idx]
        
        print atom.idx+1, len(coords)

def main():
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s foo.pdbqs foo.dlg\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    
    ifile1 = sys.stdin
    if sys.argv[1] != '-':
        ifile1 = file(sys.argv[1])
        
    ifile2 = sys.stdin
    if sys.argv[2] != '-':
        ifile2 = file(sys.argv[2])
    
    sys.stdout.flush()
    aDlg = dlg.Dlg(ifile2)
    
    charges = None
    
    pdb = Pdb(ifile1)
    proccessed_rank = set()
    for x in aDlg:
        if x.rank in proccessed_rank:
            continue
        if charges is None:
            charges = pdbq_large_charge.pdbq_large_charge(StringIO(x.mol))
        x2 = Pdb(StringIO(x.mol))
        print x.rank
        expose_area(pdb, x2, charges)
        
    

if __name__ == '__main__':
    main()