# $Id$
from itcc.ccs2 import loopclosure

__revision__ = '$Rev$'

def testcyc(ifname, options):
    loopc = loopclosure.LoopClosure()
    loopc.forcefield = options.forcefield
    loopc.keeprange = options.keepbound
    loopc.searchrange = options.searchbound
    loopc.maxsteps = options.maxsteps
    loopc.moltypekey = options.moltype
    if options.legal_min_ene is not None:
        loopc.legal_min_ene = options.legal_min_ene
    loopc(ifname)

def main():
    from optparse import OptionParser

    usage = "usage: %prog [-h|options] xyzfile"
    parser = OptionParser(usage)
    parser.add_option("-f", "--forcefield", dest='forcefield',
                      default='mm2', help="default is mm2")
    parser.add_option('-k', "--keep", dest="keepbound",
                      default=None, type='float',
                      help='keep boundary(kcal/mol), default is no boundary')
    parser.add_option('-s', "--search", dest="searchbound",
                      default=None, type='float',
                      help='search boundary(kcal/mol), default is no boundary')
    parser.add_option('-m', "--maxsteps", dest="maxsteps",
                      default=None, type='int',
                      help='max optimization steps, default is '
                           'infinite')
    parser.add_option('-t', "--moltype", dest="moltype",
                      default=None, help='you can set it to peptide')
    parser.add_option('-l', '--legal-min-ene', dest='legal_min_ene',
                      default=None, help='in some forcefield (e.g. OPLSAA), '
                      'there some illegal structure with extremely '
                      'low energy (e.g. -13960945.7658 kcal/mol), so '
                      'we treat all structure with energy lower than '
                      'LEGAL_MIN_ENE is illegal, default is %f kcal/mol'
                      % loopclosure.LoopClosure.legal_min_ene)

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    testcyc(args[0], options)

if __name__ == '__main__':
    main()

