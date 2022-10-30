import sys
from os import makedirs
from os.path import exists
from solvers.DIC import *
from solvers.RLE import *
from solvers.BIN import *
from solvers.FOR import FOR
from solvers.DIF import DIF


def main(argv):
    # control argument correctness
    if len(argv) < 4:
        exit("Not all arguments were specified. Please specify 'function', 'compression', 'data type' and 'path to data' args.")
    # argv[0]
    fun = ['en', 'de']
    if argv[0] not in fun:
        exit("Argument 0 should be either 'en' or 'de'")
    # argv[1]
    solvers = {'rle': RLE(), 'dic': DIC(), 'bin': BIN(), 'for': FOR(), 'dif': DIF()}
    if argv[1] not in solvers.keys():
        exit("Argument 1 should be one between: 'bin', 'rle', 'dic', 'for', 'diff' ")
    # argv[2]
    dtypes = ['int8', 'int16', 'int32', 'int64', 'string']
    if argv[2] not in dtypes:
        exit("Argument 2 should be one between: 'int8', 'int16', 'int32', 'int64', 'string'")
    if  argv[2] == 'string' and argv[1] in ['bin', 'for', 'dif']:
        exit("This encoding is for integer types only")
    # argv[3] is the path with the data file

    # check if results folder exists
    if len(argv) > 4:
        res_dir = argv[4]
    else:
        res_dir = 'results/temp'
    if not exists(res_dir):
        makedirs(res_dir)
    if res_dir[-1] != '/':
        res_dir += '/'

    # encode/decode
    solver = solvers[argv[1]]
    if argv[0] == 'en':
        ret = solver.encode(argv[3], argv[2], res_dir)
    elif argv[0] == 'de':
        ret = solver.decode(argv[3], argv[2], res_dir)

    return ret

if __name__ == "__main__":
    print(main(sys.argv[1:]), end='')