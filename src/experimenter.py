import time
import numpy as np
from os import makedirs, listdir
from os.path import exists
from transformers.RLE import RLE


def single_experiment(transformer, data_path, res_dir=None, additional_info='', keep_files=True):

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
    enc_f_name = res_dir+dataset+transformer.extension
    dec_f_name = res_dir+dataset+"_dec"+transformer.extension

    # TODO: encode and keep time
    enc_start = time.time()
    transformer.encode(data_path, enc_f_name)
    enc_end = time.time()
    enc_tot = enc_end - enc_start
    enc_str = f"Encoding time: {enc_tot}"
    print(enc_str)

    # TODO: decode and keep time
    dec_start = time.time()
    transformer.decode(enc_f_name, dec_f_name)
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
    ratio = np.round(enc_len/orig_len * 100, 2)
    diff = np.round((1 - enc_len/orig_len) * 100, 2)
    ratio_str = f"orig len: {orig_len}, enc len: {enc_len}, ratio: {ratio}%, diff: {diff}%"
    print(ratio_str, "\n")

    # TODO (optional): if keep_files is False discard generated files

    # write all results to file
    # create string
    res_table = f"{transformer.name}\n{dataset}\n{result_match}\n\n{enc_str}\n{dec_str}\n\n{ratio_str}"
    if additional_info != '':
        res_table += f"\n\nadditional info:{additional_info}"
    # write to experiment file
    with open(res_dir+dataset+".out", "w") as f:
        f.write(res_table)
    print(res_table)


def bulk_experiment(files_dir, transformer, additional_info='', res_dir='results/'):
    files = listdir(files_dir)
    for f in files:
        print("curr:", f)
        single_experiment(transformer, files_dir+f, res_dir, additional_info)
        print()


if __name__ == "__main__":
    transf = RLE()
    csv_path = 'ADM-2022-Assignment-2-data-T-SF-1/'
    bulk_experiment(csv_path, transf, res_dir='results/ubuntu/RLE/')
    # single_experiment(transf, csv_path+'l_shipinstruct-string.csv', res_dir='test/', additional_info="ubuntu pc")
    # single_experiment(transf, csv_path+'l_comment-string.csv', res_dir='test/', additional_info="lalala")
