import time
import argparse
from os import makedirs
from os.path import exists
from transformers.RLE import RLE


def experiment(exp_name, transformer, data_path, exp_details=None, keep_files=False):

    # create results dir if non-existant
    res_dir = 'results/'
    if not exists(res_dir):
        makedirs(res_dir)
    
    # generated file names
    enc_f_name = res_dir+'_enc'+exp_name
    dec_f_name = res_dir+'_dec'+exp_name

    # TODO: encode and keep time
    enc_start = time.time()
    transformer.encode(data_path, enc_f_name)
    enc_end = time.time()
    enc_tot = enc_end - enc_start
    print(f"Encoding with RLE time: {enc_tot}")

    # TODO: decode and keep time
    dec_start = time.time()
    transformer.decode(enc_f_name, dec_f_name)
    dec_end = time.time()
    dec_tot = dec_end - dec_start
    print(f"Encoding with RLE time: {dec_tot}")

    # TODO: make sure results match

    # TODO: if keep_files is False discard generated files

    # TODO: write all results to file with exp_details (string with info we may wanna add)


if __name__ == "__main__":
    transf = RLE()
    experiment("test.rle", transf, 'ADM-2022-Assignment-2-data-T-SF-1/l_shipinstruct-string.csv')