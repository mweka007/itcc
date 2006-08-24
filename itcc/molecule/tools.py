# $Id$
import heapq
import sets
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

def connectatoms(mol, atmidx):
    connect = mol.connect[atmidx]
    return [idx for idx, data in enumerate(connect)
            if data]

def neighborlist(mol):
    '''return the neighborlist
    for example, for CH4, will return
    [[1, 2, 3, 4],
    [0],
    [0],
    [0],
    [0]]
    '''
    result = []
    for atmidx in range(len(mol.atoms)):
        result.append(connectatoms(mol, atmidx))
    return result

def _logic_distance_matrix_helper(connectmatrix, idx):
    result = [-1] * len(connectmatrix)
    queue = [(0, idx)]
    waited_idx = sets.Set(range(len(connectmatrix)))
    while waited_idx:
        try:
            dis, curidx = heapq.heappop(queue)
        except IndexError:
            break

        if curidx not in waited_idx:
            continue

        result[curidx] = dis
        waited_idx.remove(curidx)

        for j in waited_idx:
            if connectmatrix[curidx][j]:
                heapq.heappush(queue, (dis+1, j))
    return result

def logic_distance_matrix(mol_or_connectmatrix):
    if hasattr(mol_or_connectmatrix, 'connect'):
        connectmatrix = mol_or_connectmatrix.connect
    else:
        connectmatrix = mol_or_connectmatrix

    result = Numeric.zeros((len(connectmatrix), len(connectmatrix)),
                           Numeric.Int)
    for i in range(len(connectmatrix)):
        result[i] = _logic_distance_matrix_helper(connectmatrix, i)
    return result

def logic_distance(mol_or_connectmatrix, idx1, idx2):
    if hasattr(mol_or_connectmatrix, 'connect'):
        connectmatrix = mol_or_connectmatrix.connect
    else:
        connectmatrix = mol_or_connectmatrix

    return _logic_distance_matrix_helper(connectmatrix, idx1)[idx2]