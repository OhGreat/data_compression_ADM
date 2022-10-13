import argparse
import sys
from solvers.DIC import *
from solvers.RLE import *

def main(argv):
    # control argument correctness
    if len(argv) < 4:
        exit("Not all arguments were specified. Please specify 'function', 'compression', 'data type' and 'path to data'")
    # argv[0]
    fun = ['en', 'de']
    if argv[0] not in fun:
        exit("Argument 0 should be either 'en' or 'de'")
    # argv[1]
    solvers = { 'rle': RLE(), 'dic': DIC(),  }
    if argv[1] not in solvers.keys():
        exit("Argument 1 should be one between: 'bin', 'rle', 'dic', 'for', 'diff' ")
    # argv[2]
    dtypes = ['int8', 'int16', 'int32', 'int64', 'string']
    if argv[2] not in dtypes:
        exit("Argument 2 should be one between: 'int8', 'int16', 'int32', 'int64', 'string'")
    
    # argv[3] is the path with the data file

    solver = solvers[argv[1]]
    if argv[0] == 'en':
        ret = solver.encode(argv[3])
    elif argv[0] == 'de':
        ret = solver.decode(argv[3])

    return ret

if __name__ == "__main__":
    main(sys.argv[1:])