# $Id$

import unittest

test_in_dmddat_base64 = '''\
AgAAAA4AAAALAAAAQA0DAEANAwBADQMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAlgoDABYCAAA4BAAACQkDAFgHAACyAQAAYQ0DAIkLAADJAAAAOgwDAP4Q
AADz/v//tgwDACQCAAAjCAAACQ0DAD7///94AQAADAcDAGP///+eBQAAOAYDABwJAACKBAAAZQYD
AOwGAABt/v//QhADAKcJAABi/v//mg8DAKQMAADSBAAANA8DAPATAABN/v//SgoDALsQAAC4+v//
XwgDABwTAACpAAAAAAAAAAAA8D9GCgMA7AkDAEIDAAAwCQMA4Q4DACMHAAAcBgMAcRMDAKUEAAC6
AwMApRcDAPwHAABeDAMAiQsDAPv///8UBwMAtAcDADQCAACLDAMA9QYDALUFAABWDQMAKxADAAEJ
AABbBgMAOw0DAGMKAACEAgMA1hEDAAYCAACICAMArRQDANYAAAAfAQMAxxoDAGEGAACmAgMATRYD
AAcMAACRBwMAzBkDABkJAAAAAAAAAAAAQCABAAD3CAMATgkDAEv9///OCwMARAwDAIr8///mEQMA
tgsDAIX5//9xFAMAqw8DAJsFAADaCQMAmQkDAFUAAAB5CQMAxAQDAKoBAACLBAMAsgkDAKP+//+8
CgMAoBADAEb5//9zCQMAsQsDANT7//9/EgMAEwcDAIgAAAC6EwMAVAsDAFX5///VGAMA2w8DAJ/1
//97EwMAHA8DAEb6//+yEwMAxhMDAAAAAAAAAAhAhgkDAJIIAwAPBQMAsAwDAKcKAwCHCQMAdRAD
AA0PAwA4CQMA3RMDAD8RAwCpDQMA7gsDABMHAwBxAQMAywYDAFQLAwAhAwMAnQYDAFcFAwAEBgMA
VA8DAAkHAwCjCgMAbgoDAFsKAwCIDQMAig0DAKASAwB5CAMAvxIDAJgPAwBeBQMAChYDAI4UAwBO
DQMAwxEDADESAwC3EQMAeRYDAKwNAwA8DwMAAAAAAAAAEECuCgMAHwMDAA4NAwBSDQMACwYDAI8R
AwAGEAMAVAsDAMUQAwCYEgMAhQ4DAAQVAwABDQMAgQEDAJQJAwC0BwMAqAUDAOUKAwA/CAMAZ/8C
ALoNAwAUEAMAQQMDAMgTAwDoCQMAmQYDAK4UAwADDgMAPw4DAFAOAwBsEwMAiwoDAA4OAwDMFQMA
CxEDAPcUAwDODwMAHREDAJ0XAwBKFAMAvQsDAG0YAwAAAAAAAAAUQAUDAAA1AgMAawAAAG4FAAB0
BwMA6v3//1AEAACqDAMATAEAAGYHAACREQMAMP///5T+//+cAgMAoAAAAFQEAAC6AAMAEAQAACME
AADw/gIAy/3//6QEAABQCAMAzPn//wIKAADmBgMAof3//0AFAADCCwMAWQUAAP7///8aDQMATQEA
AJQGAABKFQMAOwEAAI0LAABvEQMADP///1AGAAABEgMAG/v//wAAAAAAABhA3wIAAL8KAwDTBAMA
AwUAADcOAwCbCAMAmgoAABwQAwBnCAMAIQ0AAEoSAwDIDQMAWgUAABAHAwBdBAMArgIAAKgLAwCD
AAMAZP7//1QJAwADBQMAtAMAAI4MAwCfDAMANQIAAJsRAwCjCAMAqQsAAMUSAwDWBAMAsQ0AAPIM
AwACBwMAUhEAAC8TAwDhDQMAbwsAABkWAwDlDgMAXwwAAMsPAwDGEAMAAAAAAAAAHECgBgAAiwkD
AM8HAwDKCAAAfA8DAJkIAwDBDgAA+A8DAOEJAwD3EAAAhhUDAHYKAwAvBwAAYAcDADoLAwD8BwAA
6QcDAJwDAwA3AgAAeQkDAGYHAwDjBgAAhhEDAO8LAwBmBwAA/REDABEFAwDeEAAAKA4DAAsHAwD8
DwAADA4DAJINAwD/FAAAbxYDAI4LAwCGEAAA9RcDAL0GAwCADgAA2RcDADQNAwAAAAAAAAAgQM4H
AAD0CAMAbwgDAM0LAADxDAMA9wUDAI4OAABkEAMAMAoDAJkSAACOFAMAAggDACMEAADoCgMAiAoD
ABwKAAAXBgMASQsDAKIFAACiBgMAQgUDAAoJAADlDwMArQMDAIIOAADtCgMAPgMDAI4QAADLDQMA
Tw0DAPcLAADDEgMA8AwDANEUAACAFgMAIQsDACoWAADWEgMA4AUDADoRAAC2FwMAcwUDAAAAAAAA
ACJAwwwAALMFAwArBwMAyREAALcIAwAnBwMAPBEAAO4OAwChCAMAABYAAF0SAwA4CAMAkgkAALYH
AwBpBAMAnwoAAJAFAwCOCgMAYQ0AAK8BAwD9BAMAYhQAAGAIAwByAwMAGhUAAI4HAwAsCgMAcw8A
AEgPAwD5DAMAAw4AAMkQAwBiBgMAgBUAAIMWAwDBCQMAlxkAAEIRAwCDCgMA4hYAAA4UAwDuAwMA
AAAAAAAAJECkFAAAzgUDANEIAwDDFAAArgsDAIwGAwBfEQAAvg8DAEsKAwAeEgAAmBUDAAQJAwBL
EAAArAQDAGYJAwBnFgAAywUDANsMAwDRFgAANQMDAFQGAwAcEwAAkwsDALcCAwCzGAAAOA0DAIwF
AwDsEgAA7A4DAJ8OAwAODQAADQ4DAE4KAwB8FgAAlxYDAPwHAwA3EAAA9xUDABYFAwCbEQAAcRgD
AEgMAwA=
'''

test_in_mol = '''\
14
     1  C    199.318699    0.534962    1.080453 1 2 5 6 7
     2  C    198.921838    1.880779    0.434551 1 1 3 8 9
     3  C      0.033116    2.953881    0.201488 1 2 4 10 11
     4  C    199.738076    4.350512  199.730046 1 3 12 13 14
     5  H    199.862691    0.548103    2.083873 5 1
     6  H    199.945374  199.805354    0.376219 5 1
     7  H    198.412289  199.842674    1.438399 5 1
     8  H    198.200027    2.332853    1.162691 5 2
     9  H    198.245745    1.772234  199.596753 5 2
    10  H      0.770568    2.471146  199.585294 5 3
    11  H      0.602407    3.236348    1.234511 5 3
    12  H      0.500022    5.104879  199.564016 5 4
    13  H    199.242587    4.283611  198.647429 5 4
    14  H    198.751512    4.892723    0.169340 5 4
'''

test_out = '''\
    14  frame: 1
     1  C    199.318000    0.534000    1.080000     1     2     5     6     7
     2  C    198.921000    1.880000    0.434000     1     1     3     8     9
     3  C    200.033000    2.953000    0.201000     1     2     4    10    11
     4  C    199.738000    4.350000   -0.269000     1     3    12    13    14
     5  H    199.862000    0.548000    2.083000     5     1
     6  H    199.945000   -0.194000    0.376000     5     1
     7  H    198.412000   -0.157000    1.438000     5     1
     8  H    198.200000    2.332000    1.162000     5     2
     9  H    198.245000    1.772000   -0.403000     5     2
    10  H    200.770000    2.471000   -0.414000     5     3
    11  H    200.602000    3.236000    1.234000     5     3
    12  H    200.500000    5.104000   -0.435000     5     4
    13  H    199.242000    4.283000   -1.352000     5     4
    14  H    198.751000    4.892000    0.169000     5     4
    14  frame: 3
     1  C      0.288000  198.903000  198.990000     1     2     5     6     7
     2  C     -0.693000  199.630000  199.748000     1     1     3     8     9
     3  C     -0.886000  201.190000  199.606000     1     2     4    10    11
     4  C     -1.659000  201.841000  200.619000     1     3    12    13    14
     5  H      1.435000  199.130000  199.065000     5     1
     6  H      0.085000  199.033000  197.828000     5     1
     7  H      0.426000  197.771000  199.090000     5     1
     8  H     -0.349000  199.356000  200.864000     5     2
     9  H     -1.722000  199.027000  199.601000     5     2
    10  H     -1.068000  201.343000  198.419000     5     3
    11  H      0.136000  201.658000  199.508000     5     3
    12  H     -1.707000  202.965000  200.667000     5     4
    13  H     -2.657000  201.595000  200.476000     5     4
    14  H     -1.466000  201.650000  201.670000     5     4
    14  frame: 4
     1  C    199.046000  198.802000  197.903000     1     2     5     6     7
     2  C    199.856000  199.335000  199.047000     1     1     3     8     9
     3  C    200.821000  200.461000  198.968000     1     2     4    10    11
     4  C    201.693000  201.023000  200.105000     1     3    12    13    14
     5  H    199.662000  198.419000  196.977000     5     1
     6  H    198.347000  199.508000  197.409000     5     1
     7  H    198.301000  197.975000  198.148000     5     1
     8  H    200.532000  198.409000  199.331000     5     2
     9  H    199.278000  199.259000  200.072000     5     2
    10  H    200.074000  201.376000  198.777000     5     3
    11  H    201.407000  200.600000  197.982000     5     3
    12  H    202.250000  201.870000  200.014000     5     4
    13  H    201.155000  201.265000  201.143000     5     4
    14  H    202.361000  200.108000  200.508000     5     4
    14  frame: 7
     1  C      0.735000  199.359000  197.843000     1     2     5     6     7
     2  C      1.283000  200.247000  198.811000     1     1     3     8     9
     3  C      2.714000  200.732000  198.759000     1     2     4    10    11
     4  C      3.361000  201.290000  200.136000     1     3    12    13    14
     5  H      1.370000  198.416000  197.725000     5     1
     6  H      0.686000  199.592000  196.739000     5     1
     7  H     -0.412000  198.996000  197.891000     5     1
     8  H      0.948000  199.822000  199.839000     5     2
     9  H      0.565000  201.115000  198.819000     5     2
    10  H      2.985000  201.413000  197.846000     5     3
    11  H      3.505000  199.922000  198.402000     5     3
    12  H      4.434000  201.519000  200.161000     5     4
    13  H      2.927000  202.265000  200.421000     5     4
    14  H      3.167000  200.651000  200.902000     5     4
'''

class Test(unittest.TestCase):
    def runTest(self):
        import base64
        import StringIO
        from itcc.tools import dmddat2mtxyz
        from itcc.core.frame import parseframe
        dmddatfile = \
            StringIO.StringIO(base64.decodestring(test_in_dmddat_base64))
        molfile = StringIO.StringIO(test_in_mol)
        ofile = StringIO.StringIO()
        frame = parseframe("1-3/2,4-8/3")
        dmddat2mtxyz.dmddat2mtxyz(dmddatfile, molfile, ofile, frame)
        self.assertEqual(ofile.getvalue(), test_out)

if __name__ == '__main__':
    unittest.main()

    
