# $Id$

__revision__ = '$Rev$'

'''
http://www-iphicles.rcsb.org/pdb/docs/format/pdbguide2.2/guide2.2_frame.html

COLUMNS        DATA TYPE       FIELD          DEFINITION
--------------------------------------------------------------------------------
 1 -  6        Record name     "HETATM"
 7 - 11        Integer         serial         Atom serial number.
13 - 16        Atom            name           Atom name.
17             Character       altLoc         Alternate location indicator.
18 - 20        Residue name    resName        Residue name.
22             Character       chainID        Chain identifier.
23 - 26        Integer         resSeq         Residue sequence number.
27             AChar           iCode          Code for insertion of residues.
31 - 38        Real(8.3)       x              Orthogonal coordinates for X.
39 - 46        Real(8.3)       y              Orthogonal coordinates for Y.
47 - 54        Real(8.3)       z              Orthogonal coordinates for Z.
55 - 60        Real(6.2)       occupancy      Occupancy.
61 - 66        Real(6.2)       tempFactor     Temperature factor.
73 - 76        LString(4)      segID          Segment identifier;
                                              left-justified.
77 - 78        LString(2)      element        Element symbol; right-justified.
79 - 80        LString(2)      charge         Charge on the atom.
'''

import sys

def write(mol, ofile=sys.stdout, comment = None):
    if comment is None:
        comment = 'generated by itcc'
    if comment:
        ofile.write('HEADER %s\n' % comment)
    for i in range(len(mol)):
        atom, coord = mol[i]
        ofile.write('%-6s%5i %4s %3s  %4i    %8.3f%8.3f%8.3f%6.2f%6.2f\n' %
                    ('HETATM', i+1, atom.symbol, 'UNK', 1, coord.x(), coord.y(), coord.z(), 1.0, 0.0))
    ofile.write('END\n')
