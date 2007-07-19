#!/usr/bin/env python2.4
# $Id$

import os
import sys
from setuptools import setup, find_packages
from distutils.core import Extension

__revision__ = '$Rev$'

name = 'itcc'
version = '0.8.2.dev'
description = 'collection of tools on computational chemistry'
author = 'LI Daobing'
author_email = 'lidaobing@gmail.com'
url = 'http://www.chemgen.szpku.edu.cn'
packages = [x for x in find_packages() if x.startswith('itcc')]

ext_modules = [Extension("itcc.core.ctools", ["ext/itcc-core-ctools.c"]),
               Extension("itcc.tools.cpptools",
                         ["ext/itcc-tools-cpptools.cpp"],
                         depends=['ext/vector.hpp']),
               Extension('itcc.molecule._rmsd',
                         ['ext/itcc-molecule-_rmsd.cpp'],
                         libraries=['lapack']),
#               Extension('itcc.mopac._mopac',
#                         ['itcc/mopac/_mopac.cpp'],
#                         libraries=['mopac7', 'g2c', 'boost_python-mt'])
               ]

py_modules = []
if sys.version_info[:2] == (2, 3):
    py_modules.append('subprocess')
test_suite = 'tests'
entry_points = {
    'console_scripts': [
        'itcc = itcc.itcc_main:main',
        'itcc-makecyclicalkane = itcc.tools.makecyclicalkane:main',
        'itcc-stats = itcc.tools.stats:main',
        'itcc-calcangle = itcc.tools.calcangle:main',
        'itcc-ene2agr = itcc.tools.ene2agr:main',
        'itcc-enestep2countstep = itcc.tools.enestep2countstep:main',
        'itcc-random-protein-input = itcc.tools.random_protein_input:main',
        'itcc-loopverify = itcc.tools.verifyloop:main',
        'itcc-count = itcc.tools.count:main',
        'itcc-mirrormol = itcc.molecule.utils:mirrormol',
        'itcc-printbonds = itcc.molecule.utils:printbonds',
        'itcc-detailcmp = itcc.molecule.utils:detailcmp',
        'itcc-rg = itcc.molecule.utils:rg',
        'itcc-pyramid-check = itcc.molecule.utils:pyramid_check',
        'itcc-loopdetect = itcc.ccs2.detectloop:main',
        'itcc-out2ene = itcc.tools.out2ene:main',
        'itcc-out2arch = itcc.tools.out2arch:main',
        'itcc-xyz2gjf = itcc.tools.xyz2gjf:main',
        'itcc-gjf2xyz = itcc.molecule.gjf2xyz:main',
        'itcc-optimizes = itcc.tinker.optimizes:main',
        'itcc-xyz2gro = itcc.tools.xyz2gro:main',
        'itcc-xyz2pdb = itcc.molecule.xyz2pdb:main',
        'itcc-chiral = itcc.molecule.chiral:main',
        'itcc-confsearch = itcc.ccs2.confsearch:main',
        'itcc-catordiff = itcc.ccs2.catordiff:main',
        'itcc-detectloop = itcc.ccs2.detectloop:main',
        'itcc-dmddummy = itcc.tools.dmddummy:main',
        'itcc-scalexyz = itcc.tools.scalexyz:main',
        'itcc-columnmean = itcc.tools.columnmean:main',
        'itcc-almostequaldiff = itcc.tools.almostequaldiff:main',
        'itcc-shake = itcc.tools.shake:main',
        'itcc-mtxyzstat = itcc.tools.mtxyzstat:main',
        'itcc-mol2top = itcc.molecule.mol2top:main',
        'itcc-mtxyzrg = itcc.tools.mtxyzrg:main',
        'itcc-sumxyz = itcc.tools.sumxyz:main',
        'itcc-parmeval = itcc.torsionfit.parmeval:main',
        'itcc-dmddat_fix = itcc.tools.dmddat_fix:main',
        'itcc-onecolumn = itcc.tools.onecolumn:main',
        'itcc-settype = itcc.molecule.settype:main',
        'itcc-sumparam = itcc.tools.sumparam:main',
        'itcc-removepbc = itcc.molecule.removepbc:main',
        'itcc-dmddat2dmddat = itcc.tools.dmddat2dmddat:main',
        'itcc-parmfit = itcc.torsionfit.parmfit:main',
        'itcc-cmpxyztop = itcc.molecule.cmpxyztop:main',
        'itcc-simpparam = itcc.tinker.simpparam:main',
        'itcc-tor2freeene = itcc.tools.tor2freeene:main',
        'itcc-rmsd = itcc.molecule.rmsd:main_rmsd',
        'itcc-rmsd2 = itcc.molecule.rmsd:main_rmsd2',
        'itcc-dmddat2mtxyz = itcc.tools.dmddat2mtxyz:main',
        'itcc-printefit = itcc.torsionfit.printefit:main',
        'itcc-constrain = itcc.tinker.constrain:main',
        'itcc-loop2looptor = itcc.tools.loop2looptor:main',
        'itcc-idx-verify = itcc.tools.idx_verify:main',
        'itcc-molcenter = itcc.tools.molcenter:main',
        'itcc-rotate-to = itcc.tools.rotate_to:main',
        'itcc-histogram = itcc.tools.histogram:main',
        'itcc-tordiff = itcc.tools.tordiff:main',
        'itcc-moldiff = itcc.tools.moldiff:main',
        'itcc-findneighbour = itcc.ccs2.confsearch2:main',
        'itcc-relative = itcc.tools.relative:main',
    ]
}
classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering :: Chemistry',
        ]
license_ = 'Other/Proprietary License'

def main():
    setup(
        name=name,
        version=version,
        description=description,
        author=author,
        author_email=author_email,
        url=url,
        packages = packages,
        ext_modules = ext_modules,
        py_modules = py_modules,
        test_suite = test_suite,
        entry_points = entry_points,
        include_package_data = False,
        classifiers = classifiers,
        license = license_,
    )

if __name__ == '__main__':
    main()

