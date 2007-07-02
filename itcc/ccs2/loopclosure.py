# $Id$
# pylint: disable-msg=E1101
# pylint: disable-msg=W0201
import sys
import os
import os.path
import bisect
import heapq
import pprint
import time
import random
import tempfile
import shutil
import cPickle
from cStringIO import StringIO
try:
    import threading
except ImportError:
    import dummy_threading as threading

import itcc
from itcc.tinker import tinker
from itcc.molecule import read, write, mtxyz, chiral, tools as moltools
from itcc.ccs2 import detectloop, base, peptide, sidechain
from itcc.ccs2 import mezeipro2, tordiff
from itcc.ccs2 import mezei as Mezei
from itcc.ccs2 import mezeipro as Mezeipro

__all__ = ['LoopClosure']
__revision__ = '$Rev$'

class LoopClosure(object):
    '''need a doc'''
    S_NONE = 0
    S_INITED = 1

    @classmethod
    def get_default_config(klass):
        from ConfigParser import RawConfigParser

        defaults = {
                'log_level': '1',
                'np': '1',
                # molecule type
                'forcefield': 'mm2',

                # loop type
                'is_chain': 'False',

                # dump
                'dump_steps': '100',

                # before minimization
                'check_energy_before_minimization': 'True',
                'minimal_invalid_energy_before_minimization': '100000', # unit: kcal/mol

                # minimization
                # 'minimization_method': 'newton',
                'minconverge': '0.001', # unit: ?
                # 'tinker_keep_chiral': 'true',

                # after minimization
                'legal_min_ene': '-100000', # unit: kcal/mol
                'check_minimal': 'False',

                # check
                'eneerror': '0.0001', # unit: kcal/mol
                'torerror': '10',     # unit: degree
                }
                
        return RawConfigParser(defaults)

    def __init__(self, config):
        self.config = config

        keys = {self.config.get: ['forcefield', 'moltypekey', 'solvate',
                    'cmptorsfile', 'loopfile', 'chiral_index_file',
                    'molfname', 'tinker_key_file'],
                self.config.getboolean: ['is_chain', 
                    'check_energy_before_minimization', 'is_achiral',
                    'check_minimal'
                    ],
                self.config.getint: ['maxsteps', 'dump_steps', 'np',
                    'head_tail', 'loopstep', 'log_level'],
                self.config.getfloat: ['keeprange', 'searchrange', 'eneerror',
                    'legal_min_ene', 'torerror', 'minconverge',
                    'minimal_invalid_energy_before_minimization']}

        for t in keys:
            for key in keys[t]:
                if self.config.has_option('DEFAULT', key):
                    setattr(self, key, t('DEFAULT', key))
                else:
                    setattr(self, key, None)

        self.cmptors = None

        self._step_count = 0
        self.seedmol = None
        self._tasks = []                # List of (coords, ene)
        self.taskheap = []              # Heap of (r6idx, ene, taskidx, r6)
        self.enes = []                  # Sorted List of (ene, taskidx)
        self.tmp_mtxyz_fname = None
        self.tmp_mtxyz_file = None
        self.lowestene = None
        self.shakedata = None
        self.start_time = None
        self.olddir = None
        self.newdir = None
        self.state = self.S_NONE

        self.chiral_idxs = None
        self._chirals = []

        self.multithread = False
        self.mutex = threading.Lock()
        self.loopatoms = None
        self.r6s = None

    def run(self):
        if not self.init():
            return

        if self.np > 1:
            self._run_multi_thread()
        else:
            self._run_single_thread()

    __cal__ = run

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['tmp_mtxyz_file']
        del odict['mutex']
        return odict

    def __setstate__(self, dicts):
        self.__dict__.update(dicts)
        self.olddir = os.getcwd()
        self.newdir = tempfile.mkdtemp('itcc')
        os.chdir(self.newdir)
        if self.tmp_mtxyz_fname is not None:
            self.tmp_mtxyz_fname = \
                os.path.join(self.olddir,
                             os.path.basename(self.tmp_mtxyz_fname))
            self.tmp_mtxyz_file = file(self.tmp_mtxyz_fname, 'ab+')
            for i in range(len(self._tasks)): #pylint: disable-msg=W0612
                read.readxyz(self.tmp_mtxyz_file)
            self.tmp_mtxyz_file.truncate()
        else:
            self.tmp_mtxyz_file = None
        self.mutex = threading.Lock()

    def getkeepbound(self):
        if self.keeprange is None:
            return None
        return self.lowestene + self.keeprange
    keepbound = property(getkeepbound)

    def getsearchbound(self):
        if self.searchrange is None:
            return None
        return self.lowestene + self.searchrange
    searchbound = property(getsearchbound)


    def _run_single_thread(self):
        self.multithread = False
        last_dump_step = self._step_count
        while self.maxsteps is None \
              or self._step_count < self.maxsteps:
            if self._step_count - last_dump_step >= self.dump_steps:
                self.dump()
                last_dump_step = self._step_count
                os.system("ps -p %s -o rss" % os.getpid())
            try:
                taskidx, r6 = self.taskqueue().next()
            except StopIteration:
                break
            self.runtask(taskidx, r6)
        self._cleanup()

    def _run_multi_thread(self):
        self.multithread = True

        threads = []
        last_dump_step = self._step_count

        def clear_threads():
            threads[:] = [x for x in threads if x.isAlive()]

        some_threads_finished_condition = \
            threading.Condition(self.mutex)

        class Task:
            def __init__(self, parent, taskidx, r6):
                self.parent = parent
                self.taskidx = taskidx
                self.r6 = r6
            def __call__(self):
                self.parent.runtask(self.taskidx, self.r6) 
                self.parent.mutex.acquire()
                some_threads_finished_condition.notify()
                self.parent.mutex.release()

        while True:
            some_threads_finished_condition.acquire()
            clear_threads()
            if (not threads and not self.taskheap) \
              or (self.maxsteps is not None
                  and self._step_count >= self.maxsteps) :
                some_threads_finished_condition.release()
                for thread in threads:
                    thread.join()
                break
            if self._step_count - last_dump_step >= self.dump_steps:
                some_threads_finished_condition.release()
                for thread in threads:
                    thread.join()
                self.dump()
                last_dump_step = self._step_count
                continue

            need_wait = False
            while len(threads) < self.np and self.taskheap:
                ene, taskidx, r6 = heapq.heappop(self.taskheap)[1:]
                if self.searchbound is not None and ene > self.searchbound:
                    continue
                task = Task(self, taskidx, r6)
                thread = threading.Thread(target = task)
                threads.append(thread)
                thread.start()
                need_wait = True

            if need_wait:
                some_threads_finished_condition.wait()

            some_threads_finished_condition.release()
        self._cleanup()

    def dump(self):
        self.tmp_mtxyz_file.flush()
        ofname = os.path.join(self.olddir, 'checkfile.part')
        ofile = file(ofname, 'w')
        cPickle.dump(self, ofile, 1)
        ofile.close()

        os.rename(ofname, os.path.join(self.olddir, 'checkfile'))

    def _get_tinker_key(self):
        res = ''
        if self.tinker_key_file is not None:
            res += file(os.path.join(self.olddir, self.tinker_key_file)).read()
        if res and res[-1] != '\n':
            res += '\n'
        if not self.is_achiral:
            res += 'ENFORCE-CHIRALITY\n'
        if self.solvate is not None:
            res += 'SOLVATE %s\n' % self.solvate
        return res
        
        
    def init_env(self):
        self.start_time = time.time()
        self.olddir = os.getcwd()
        self.newdir = tempfile.mkdtemp('itcc')
        os.chdir(self.newdir)
        fd, self.tmp_mtxyz_fname = tempfile.mkstemp(dir=self.olddir)
        self.tmp_mtxyz_file = os.fdopen(fd, 'wb+')
        return True

    def init_mol(self):
        self.seedmol = read.readxyz(file(os.path.join(self.olddir,
                                                      self.molfname)))
        return True

    def init_task(self):
        mol, ene = self._minimizemol(self.seedmol)
        if mol is None:
            self.log("weird input molecule\n")
            return False
        self._step_count += 1
        self.lowestene = ene
        self.addtask(mol, ene)
        return True

    def init_loop(self):
        if self.loopatoms is None:
            if self.loopfile is not None:
                self.loopatoms = sum([[int(x) - 1 \
                        for x in line.split()
                        if line.strip() and line[0] != '#']
                        for line in file(os.path.join(self.olddir, self.loopfile)).readlines()], [])
        if self.loopatoms is None:
            looptype, loops = detectloop.loopdetect(self.seedmol)
            if looptype == detectloop.SIMPLELOOPS \
                    and len(loops) == 1:
                self.loopatoms = loops[0]

        if self.loopatoms is None:
            self.log("this moleclue does not contain loop. exit.\n")
            return False

        if len(self.loopatoms) < 6:
            self.log("your ring is %s-member, "
                "we can't deal with ring less than 6-member.\n"
                % len(self.loopatoms))
            return False

        return self._check_loop_atoms(self.seedmol, self.loopatoms)

    def init_r6(self):
        typedmol = getmoltype(self.moltypekey)(self.seedmol)
        r6s = tuple(typedmol.getr6s(self.loopatoms, self.is_chain))
        self.r6s = {}
        for idx, x in enumerate(r6s):
            self.r6s[x] = idx
        return True

    def init_sidechain(self):
        self.shakedata = getshakedata(self.seedmol, self.loopatoms)
        return True

    def init_check(self):
        if self.chiral_idxs is None:
            if self.chiral_index_file is not None:
                self.chiral_idxs = sum([[int(x) - 1 \
                        for x in line.split()
                        if line.strip() and line[0] != '#']
                        for line in file(os.path.join(self.olddir,
			                              self.chiral_index_file)).readlines()], [])

        if self.chiral_idxs:
            self._chirals = tuple(chiral.chiral_types(self.seedmol, self.chiral_idxs))

        if self.head_tail is None:
            if self.moltypekey == 'peptide':
                self.head_tail = -1
            else:
                self.head_tail = 0
            
        if self.is_achiral is None:
            if self.moltypekey == 'peptide':
                self.is_achiral = False
            else:
                self.is_achiral = True
                
        if self.loopstep is None:
            if self.moltypekey == 'peptide' or self.is_chain:
                self.loopstep = 0
            else:
                self.loopstep = 1

        if self.cmptors is None:
            if self.cmptorsfile is not None:
                self.cmptors = [[int(x)-1 for x in line.split()
                    if line.strip() and line[0] != '#']
                    for line in file(self.cmptorsfile).readlines()]

        if self.cmptors is None:
            if self.is_chain:
                self.cmptors = \
                    [self.loopatoms[i:i+4] for i in range(len(self.loopatoms)-3)]
            else:
                self.cmptors = \
                    [(self.loopatoms*2)[i:i+4] for i in range(len(self.loopatoms))]

        for x in self.cmptors:
            assert len(x) == 4
        return True

    def init_tinker(self):
        content = self._get_tinker_key()
        if content:
            file('tinker.key', 'w').write(content)
        tinker.curdir = True
        return True

    def init(self):
        if self.state != self.S_NONE:
            return True

        self.print_copyright()
        self.print_config()
        if not (self.init_env()
                and self.init_mol()
                and self.init_loop()
                and self.init_r6()
                and self.init_sidechain()
                and self.init_check()
                and self.init_tinker()
                and self.init_task()
                ):
            return False
        self.print_params()

        self.state = self.S_INITED
        return True

    def _cleanup(self):
        os.chdir(self.olddir)
        shutil.rmtree(self.newdir)
        self.reorganizeresults()
        self.printend()

    def runtask(self, taskidx, r6):
        self.mutex.acquire() # r self.tasks
        ene = self._tasks[taskidx][1]
        mol = self.seedmol.copy()
        mol.coords[:] = self._tasks[taskidx][0]
        self.mutex.release()
        self.log('\n')
        head = ' CCS2 Local Search'
        self.log('%-31s Minimum %6i %21.4f\n\n'
              % (head, taskidx + 1, ene))

        for newmol, newene, logstr in self.findneighbor(mol, r6):
            validstr = self.is_valid(newmol, newene)
            if validstr != 'V':
                self.log('%s %s\n' % (logstr, validstr))
                continue
            idx = self.eneidx(newmol, newene)
            if idx >= 0:
                self.log(logstr + '(%i)\n' % (idx + 1))
            else:
                self.log(logstr + '\n')
            if idx == -1:
                self.addtask(newmol, newene)
            if newene < self.lowestene:
                self.mutex.acquire()
                self.lowestene = newene
                finished = self.searchbound is not None \
                    and ene >= self.searchbound
                self.mutex.release()
                if finished:
                    return

    def eneidx(self, mol, ene):
        '''return the taskidx
        if is new ene, return -1,
        if is out of range, return -2'''
        res = None
        self.mutex.acquire()
        if self.keeprange is not None and \
           self.searchrange is not None:
            if ene > max(self.keepbound, self.searchbound):
                res = -2

        # FIXME: remove duplicate codes
        if res is None:
            initidx = bisect.bisect(self.enes, (ene,))
            for idx in range(initidx-1, -1, -1):
                ene2 = self.enes[idx][0]
                if round(ene - ene2, 4) > self.eneerror:
                    break
                taskidx = self.enes[idx][1]
                coords2 = self._tasks[taskidx][0]
                mol2 = self.seedmol.copy()
                mol2.coords[:] = coords2
                if self._check_tor(mol, mol2):
                    res = taskidx

        if res is None:                
            for idx in range(initidx, len(self.enes)):
                ene2 = self.enes[idx][0]
                if round(ene2 - ene, 4) > self.eneerror:
                    break
                taskidx = self.enes[idx][1]
                coords2 = self._tasks[taskidx][0]
                mol2 = self.seedmol.copy()
                mol2.coords[:] = coords2
                if self._check_tor(mol, mol2):
                    res = taskidx

        if res is None:
            res = -1
        self.mutex.release()
        return res

    def addtask(self, mol, ene):
        self.mutex.acquire()
        self._tasks.append((mol.coords, ene))
        taskidx = len(self._tasks) - 1
        bisect.insort(self.enes, (ene, taskidx))
        self.log('    Potential Surface Map       Minimum '
              '%6i %21.4f\n' % (taskidx+1, ene))
        self.writemol(mol, ene)
        r6s = self.r6s.keys()
        random.shuffle(r6s)
        for r6idx, r6 in enumerate(r6s):
            heapq.heappush(self.taskheap, (r6idx, ene, taskidx, r6))
        self.mutex.release()

    def taskqueue(self):
        while self.taskheap:
            ene, taskidx, r6 = heapq.heappop(self.taskheap)[1:]
            if self.searchbound is not None and ene > self.searchbound:
                continue
            yield taskidx, r6

    # read self.loopfile
    def _check_loop_atoms(self, mol, loop):
        if self.is_chain:
            count = len(loop) - 1
        else:
            count = len(loop)
        for i in range(count):
            next = (i + 1) % len(loop)
            if not mol.is_connect(loop[i], loop[next]):
                return False
        return True

    def print_params(self):
        msg = 'starttime: %s\n' % time.ctime(self.start_time)
        msg += 'loop: %s\n' % ' '.join(str(x+1) for x in self.loopatoms)
        msg += 'r6s:\n'
        msg += r6s2str(self.r6s)
        if self.chiral_idxs:
            msg += 'Chiral: %s\n' % ' '.join(str(x+1) for x in self.chiral_idxs)
        msg += 'tinker.key:\n'
        msg += self._get_tinker_key()
        msg += '\n'
        self.log(msg)

    def printend(self):
        import datetime

        self.log('Starttime: %s\n' % time.ctime(self.start_time))
        end_time = time.time()
        self.log('Endtime: %s\n' % time.asctime())
        self.log('Total time: %s\n'
                 % datetime.timedelta(0, end_time - self.start_time))

        try:
            import resource
        except ImportError:
            pass
        else:
            res_c = resource.getrusage(resource.RUSAGE_CHILDREN)
            res_s = resource.getrusage(resource.RUSAGE_SELF)
            res_c_t = res_c[0] + res_c[1]
            res_s_t = res_s[0] + res_s[1]
            res_t = res_c_t + res_s_t
            self.log('Total CPU time: %s\n' % datetime.timedelta(0, res_t))
            self.log('Time used by   this   program: %.1fs(%.1f+%.1f)\n'
                     % (res_s_t, res_s[0], res_s[1]))
            self.log('Time used by external program: %.1fs(%.1f+%.1f)\n'
                     % (res_c_t, res_c[0], res_c[1]))

    def writemol(self, mol, ene):
        write.writexyz(mol, self.tmp_mtxyz_file, '%.4f' % ene)

    def findneighbor(self, mol, r6):
        coords = mol.coords
        dismat = moltools.distmat(mol)
        for molidx, molresult \
                in enumerate(getr6result(coords, r6, dismat, self.shakedata)):
            newmol = mol.copy()
            for idx, coord in molresult.items():
                newmol.coords[idx] = coord
            rmol, rene = self._minimizemol(newmol)
            if rmol is None:
                continue
            self.mutex.acquire() # r/w _step_count
            self._step_count += 1
            self.mutex.release()
            logstr = '  Step %5i   Comb %02i-%02i %42.4f ' \
                % (self._step_count, self.r6s[r6], molidx, rene)
            yield rmol, rene, logstr
            if self.maxsteps is not None and self._step_count >= self.maxsteps:
                return

    def reorganizeresults(self):
        self.tmp_mtxyz_file.seek(0)
        oldmols = mtxyz.Mtxyz(self.tmp_mtxyz_file)
        newidxs = [ene[1] for ene in self.enes 
                   if self.keeprange is None
                      or ene[0] <= self.keepbound]
        newmolnametmp = os.path.splitext(self.molfname)[0] \
                        + ".%0" + str(len(str(len(newidxs)))) + "i.xyz"

        self.log('\nOldidx Newidx Ene(sort by Oldidx)\n')
        for oldidx, oldmol in enumerate(oldmols.read_mol_as_string()):
            ene = self._tasks[oldidx][1]
            try:
                newidx = newidxs.index(oldidx)
            except ValueError:
                self.log('%6i %6s %.4f\n' % (oldidx+1, '', ene))
            else:
                newfname = newmolnametmp % (newidx + 1)
                file(newfname, 'w').write(oldmol)
                self.log('%6i %6i %.4f\n' % (oldidx+1, newidx+1, ene))

        self.log('\nOldidx Newidx Ene(sort by Newidx)\n')
        for newidx, oldidx in enumerate(newidxs):
            self.log('%6i %6i %.4f\n' % (oldidx+1, newidx+1, self._tasks[oldidx][1]))
        self.log('\n')

    def log(self, msg, lvl=None):
        if lvl is None or lvl <= self.log_level:
            sys.stdout.write(msg)
            sys.stdout.flush()

    def is_valid(self, mol, ene):
        if ene < self.legal_min_ene:
            return 'L'
        if self.chiral_idxs \
                and tuple(chiral.chiral_types(mol, self.chiral_idxs)) \
                != self._chirals:
            return 'C'
        if self.check_minimal and not tinker.isminimal(mol, self.forcefield):
            return 'M'
        return 'V'
    
    # FIXME: we only need write mol once
    def _minimizemol(self, newmol):
        if self.check_energy_before_minimization:
            ene = tinker.analyze(newmol, self.forcefield)
            if ene >= self.minimal_invalid_energy_before_minimization:
                return None, None
        return tinker.newton_mol(newmol,
                                  self.forcefield,
                                  self.minconverge,
                                  prefix=threading.currentThread().getName())
    
    # TODO: provide a fast algorithm if self.is_head_tail is false 
    # and self.is_achiral is false and self.loopstep is 0
    def _check_tor(self, mol1, mol2):
        tors1 = [mol1.calctor(x[0], x[1], x[2], x[3]) for x in self.cmptors]
        tors2 = [mol2.calctor(x[0], x[1], x[2], x[3]) for x in self.cmptors]
        return tordiff.torsdiff(tors1, tors2, 
                                self.is_achiral, 
                                self.head_tail, 
                                self.loopstep) < self.torerror

    def print_copyright(self):
        msg = 'CCS2 conformational search (itcc ' + itcc.__version__ + ')\n'
        self.log(msg)

    def print_config(self):
        msg = '# config file begin\n'
        ofile = StringIO()
        self.config.write(ofile)
        msg += ofile.getvalue()
        ofile.close()
        msg += '# config file end\n'
        self.log(msg)

def getr6result(coords, r6, dismat, shakedata):
    r6 = list(r6)
    r6[0] = r6[0][-1:]
    r6[-1] = r6[-1][:1]
    type_ = r6type(r6)
    if type_ == (1, 1, 1, 1, 1, 1, 1):
        idxs = tuple(sum(r6, tuple()))
        return Mezei.R6(coords, idxs, dismat, shakedata)
    elif type_ == (1, 1, 2, 1, 2, 1, 1):
        idxs = tuple(sum(r6, tuple()))
        return Mezeipro.R6(coords, idxs, dismat, shakedata)
    elif type_ == (1, 2, 1, 2, 1, 2, 1):
        idxs = tuple(sum(r6, tuple()))
        return mezeipro2.R6(coords, idxs, dismat, shakedata)
    assert False, r6type(r6)

def r6type(r6):
    return tuple([len(x) for x in r6])

_moltypedict = {'peptide': peptide.Peptide}
def getmoltype(key):
    return _moltypedict.get(key, base.Base)

# TODO: if it's a chain
def getshakedata(mol, loop):
    result = {}
    dloop = loop * 2
    for idx, atomidx in enumerate(loop):
        refidxs = [atomidx, dloop[idx-1], dloop[idx+1]]
        sidechain_ = sidechain.getsidechain(mol, loop, atomidx)
        result[atomidx] = (refidxs, sidechain_)
    return result

def r6s2str(r6s):
    res = "This loop has %i R6 blocks:\n" % len(r6s)
    ofile = StringIO()
    pprint.pprint(r6s, ofile)
    res += ofile.getvalue()
    res += '\n'
    return res
