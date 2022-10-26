import time
from os import makedirs, listdir, remove
from os.path import exists
from solvers.RLE import RLE
from solvers.DIC import DIC
from solvers.BIN import BIN
from solvers.FOR import FOR


def single_experiment(solver, data_path, res_dir=None, 
                        additional_info=None, keep_files=True, data_type='int8', **kwargs):

    # create results dir if non-existant
    if res_dir is None:
        res_dir = '.'
    # check path is correct
    if res_dir[-1] != '/':
        res_dir += '/'
    if not exists(res_dir):
        makedirs(res_dir)
    
    # take name of the dataset
    dataset = data_path.split('/')[-1]
    # generated file names
    enc_f_name = res_dir+dataset+solver.extension
    dec_f_name = res_dir+"dec_"+dataset+solver.extension

    # encode and keep time
    enc_start = time.time()
    solver.encode(data_path, data_type, res_dir, **kwargs)
    enc_end = time.time()
    enc_tot = enc_end - enc_start
    enc_str = f"Encoding time: {enc_tot}"
    print(enc_str)

    # decode and keep time
    dec_start = time.time()
    solver.decode(enc_f_name, data_type, res_dir, **kwargs)
    dec_end = time.time()
    dec_tot = dec_end - dec_start
    dec_str = f"Decoding time: {dec_tot}"
    print(dec_str)

    # check if results match
    with open(dec_f_name, 'r') as dec:
        dec_lines = dec.readlines()
    with open(data_path, 'r') as orig:
        orig_lines = orig.readlines()
    if dec_lines == orig_lines:
        result_match = "OK! Decoded file matches the original file."
        print(result_match)
    else:
        result_match = "ERROR! Decoded file does not match the original file."
        print(result_match)
        print("Decoded:",len(dec_lines), "lines.")

    # keep track of compression rations
    with open(enc_f_name, 'r') as enc:
        enc_lines = enc.readlines()
    orig_len = len(orig_lines)
    enc_len = len(enc_lines)
    len_ratio = round(enc_len/orig_len * 100, 2)
    len_diff = round((1 - enc_len/orig_len) * 100, 2)
    len_str = f"orig len: {orig_len}, enc len: {enc_len}, ratio: {len_ratio}%, diff: {len_diff}%"
    print(len_str)

    orig_chars = sum([len(line) for line in orig_lines])
    enc_chars = sum([len(line) for line in enc_lines])
    char_ratio = round(enc_chars/orig_chars * 100, 2)
    char_diff = round((1 - enc_chars/orig_chars) * 100, 2)
    char_str = f"orig chars: {orig_chars}, enc chars: {enc_chars}, ratio: {char_ratio}%, diff: {char_diff}%"
    print(char_str, "\n")

    # if keep_files is False discard generated files
    if not keep_files:
        remove(enc_f_name)
        remove(dec_f_name)

    # create result string
    res_table = f"{solver.name}\n{dataset}\n{result_match}\n\n{enc_str}\n{dec_str}\n\n{len_str}\n{char_str}"
    if additional_info is not None:
        res_table += f"\n\nadditional info:{additional_info}"
    # write results to file
    with open(res_dir+dataset+".out", "w") as f:
        f.write(res_table)
    # print(res_table)


def bulk_experiment(files_dir, solvers, additional_info='', res_dir='results/', keep_files=False, data_type='int8', **kwargs):
    """ Runs an experiment for each file in the files_dir directory
    """
    if res_dir[-1] != '/':
        res_dir += '/'

    print(kwargs)
    files = listdir(files_dir)
    for solver in solvers:
        for f in files:
            if data_type in f:
                print("Curr solver:", solver.name, "curr file:", f)
                single_experiment(solver, files_dir+f, res_dir+solver.name, additional_info, 
                                    keep_files=keep_files, data_type='int8', **kwargs)
                print()


if __name__ == "__main__":
    rle = RLE()
    dict_ = DIC()
    bin = BIN()
    for_ = FOR()
    
    # csv_path = 'ADM-2022-Assignment-2-data-T-SF-1/l_linenumber-int32.csv'
    csv_path = 'ADM-2022-Assignment-2-data-T-SF-1/'
    # l_extendedprice-int64.csv
    # l_discount-int8.csv
    # l_linenumber-int8.csv

    # Generic experiment
    solvers = [RLE(), DIC(), BIN(), FOR()]
    bulk_experiment(csv_path, solvers, res_dir='results/temp/', keep_files=False, data_type='int64')
    # single_experiment(bin, csv_path+'l_discount-int8.csv', res_dir='temp_dict/', keep_files=False, data_type='int8')
    

    # FOR experimentation
    # solvers = [FOR()]
    # kwargs = {'block_size': 1024}
    # single_experiment(for_, csv_path+'l_extendedprice-int32.csv', res_dir='temp_for/', 
    #                 keep_files=True, data_type='int64', **kwargs)
    # bulk_experiment(csv_path, solvers, res_dir='results/ubuntu/FOR/int8-4block', data_type='int64', **kwargs)