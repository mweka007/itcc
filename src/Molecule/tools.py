# $Id$
import Numeric

__revision__ = '$Rev$'

def distmat(mol):
    size = len(mol)
    result = Numeric.zeros((size, size), Numeric.Float)

    for i in range(size):
        for j in range(i):
            distance = (mol.coords[i] - mol.coords[j]).length()
            result[i, j] = distance
            result[j, i] = distance
    return result

def gettypes(mol):
    return [atom.type for atom in mol.atoms]

def calclooptor(mol, loop):
    doubleloop = loop * 2
    tors = [mol.calctor(*doubleloop[i:i+4]) for i in range(len(loop))]
    return tors
