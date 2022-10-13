import time
from os import makedirs, listdir, remove
from os.path import exists
from solvers.RLE import RLE
from solvers.DIC import DIC


def single_experiment(solver, data_path, res_dir=None, 
                        additional_info=None, keep_files=True):

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
    solver.encode(data_path, res_dir)
    enc_end = time.time()
    enc_tot = enc_end - enc_start
    enc_str = f"Encoding time: {enc_tot}"
    print(enc_str)

    # decode and keep time
    dec_start = time.time()
    solver.decode(enc_f_name, res_dir)
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
        print(len(dec_lines))

    # keep track of compression rations
    with open(enc_f_name, 'r') as enc:
        enc_lines = enc.readlines()
    orig_len = len(orig_lines)
    enc_len = len(enc_lines)
    ratio = round(enc_len/orig_len * 100, 2)
    diff = round((1 - enc_len/orig_len) * 100, 2)
    ratio_str = f"orig len: {orig_len}, enc len: {enc_len}, ratio: {ratio}%, diff: {diff}%"
    print(ratio_str, "\n")

    # if keep_files is False discard generated files
    if not keep_files:
        remove(enc_f_name)
        remove(dec_f_name)

    # create result string
    res_table = f"{solver.name}\n{dataset}\n{result_match}\n\n{enc_str}\n{dec_str}\n\n{ratio_str}"
    if additional_info is not None:
        res_table += f"\n\nadditional info:{additional_info}"
    # write results to file
    with open(res_dir+dataset+".out", "w") as f:
        f.write(res_table)
    # print(res_table)


def bulk_experiment(files_dir, solvers, additional_info='', res_dir='results/', keep_files=True):
    """ Runs an experiment for each file in the files_dir directory
    """
    if res_dir[-1] != '/':
        res_dir += '/'

    files = listdir(files_dir)
    for solver in solvers:
        for f in files:
            print("curr:", f)
            single_experiment(solver, files_dir+f, res_dir+solver.name, additional_info, keep_files=keep_files)
            print()


if __name__ == "__main__":
    rle = RLE()
    dict_ = DIC()
    solvers = [RLE(), DIC()]
    
    # csv_path = 'ADM-2022-Assignment-2-data-T-SF-1/l_linenumber-int32.csv'
    csv_path = 'ADM-2022-Assignment-2-data-T-SF-1/'

    bulk_experiment(csv_path, solvers, res_dir='results/temp/', keep_files=False)
    # single_experiment(dict_, csv_path+'l_shipinstruct-string.csv', res_dir='temp_dict/', keep_files=False)
