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
    dtypes = ['int8', 'int16', 'int32', 'int64', 'string']
    if argv[2] not in dtypes:
        exit("Argument 2 should be one between: 'int8', 'int16', 'int32', 'int64', 'string'")
    if  argv[2] == 'string' and argv[1] in ['bin', 'for', 'dif']:
        exit("This encoding is for integer types only")
    dtype = argv[2]
    # print(dtype)
    solvers = {
        'rle': RLE(dtype),
        'dic': DIC(dtype),
        'bin': BIN(dtype),
        'for': FOR(dtype),
        'dif': DIF(dtype)
     }
    if argv[1] not in solvers.keys():
        exit("Argument 1 should be one between: 'bin', 'rle', 'dic', 'for', 'diff' ")
    # argv[2]
    # argv[3] is the path with the data file

    # check if results folder exists
    if len(argv) > 4:
        res_dir = argv[4]
    else:
        res_dir = './'

    # encode/decode
    solver = solvers[argv[1]]
    if argv[0] == 'en':
        ret = solver.encode(argv[3], res_dir)
    elif argv[0] == 'de':
        ret = solver.decode(argv[3], res_dir)

    return ret

if __name__ == "__main__":
    print(main(sys.argv[1:]), end='')