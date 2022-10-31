import time
from os import makedirs, listdir, remove
from os import path
from solvers.RLE import RLE
from solvers.DIC import DIC
from solvers.BIN import BIN
from solvers.FOR import FOR
from solvers.DIF import DIF


def single_experiment(solver, data_path, res_dir=None, 
                        additional_info=None, keep_files=True, data_type='int8', **kwargs):

    # create results dir if non-existant
    if data_type=='string' and solver.name in ['BIN', 'FOR', 'DIF']:
        return
    
    if res_dir is None:
        res_dir = '.'
    # check path is correct
    if res_dir[-1] != '/':
        res_dir += '/'
    if not path.exists(res_dir):
        makedirs(res_dir)
    
    # take name of the dataset
    dataset = data_path.split('/')[-1]
    # generated file names
    enc_f_name = res_dir+dataset+solver.extension
    dec_f_name = res_dir+dataset+solver.extension+'.csv'

    # encode and keep time
    enc_start = time.time()
    solver.encode(data_path, res_dir, **kwargs)
    enc_end = time.time()
    enc_tot = enc_end - enc_start
    enc_str = f"Encoding time: {enc_tot}"
    print(enc_str)

    # decode and keep time
    dec_start = time.time()
    solver.decode(enc_f_name, res_dir, **kwargs)
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

    if solver.name == 'BIN':
        with open(enc_f_name, 'rb') as enc:
            enc_lines = enc.readlines()
    else:
        # keep track of compression rations
        with open(enc_f_name, 'rb') as enc:
            enc_lines = enc.readlines()
    orig_len = len(orig_lines)
    enc_len = len(enc_lines)
    len_ratio = round(enc_len/orig_len * 100, 2)
    len_diff = round((1 - enc_len/orig_len) * 100, 2)
    len_str = f"orig len: {orig_len}, enc len: {enc_len}, ratio: {len_ratio}%, diff: {len_diff}%"
    print(len_str)

    orig_size = path.getsize(data_path) / (1024*1024)
    enc_size = path.getsize(enc_f_name) / (1024*1024)
    compression_ratio = round(enc_size/orig_size * 100, 2)
    compression_ratio_supplement = round((1 - enc_size/orig_size) * 100, 2)
    char_str = f"orig size: {orig_size}, enc size: {enc_size}, ratio: {compression_ratio}%, diff: {compression_ratio_supplement}%"
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
                                    keep_files=keep_files, data_type=data_type, **kwargs)
                print()


if __name__ == "__main__":
    csv_path = 'ADM-2022-Assignment-2-data-T-SF-1/'

    # Generic experiment
    data_types = [
        # 'string',
        'int8',
        'int16',
        'int32',
        'int64',
         ]
    for data_type in data_types:
        solvers = [
            # BIN(data_type),
            # RLE(data_type),
            # DIC(data_type),
            # FOR(data_type),
            DIF(data_type),
        ]
        
        for solver in solvers:
            bulk_experiment(csv_path, solvers, res_dir='results/new', keep_files=True, data_type=data_type)
    # single_experiment(bin, csv_path+'l_extendedprice-int64.csv', res_dir='temp_dict/', keep_files=False, data_type='int64')
    

    # FOR experimentation
    # solvers = [FOR()]
    # kwargs = {'block_size': 1024}
    # single_experiment(for_, csv_path+'l_extendedprice-int32.csv', res_dir='temp_for/', 
    #                 keep_files=True, data_type='int64', **kwargs)
    # bulk_experiment(csv_path, solvers, res_dir='results/ubuntu/FOR/int8-4block', data_type='int64', **kwargs)