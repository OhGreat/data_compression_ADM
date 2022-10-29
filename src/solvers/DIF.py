from base64 import encode
import math
import numpy as np

# Local import
from solvers.encoder_decoder import EncoderDecoder

def bin_array(num, m, dtype):
    """Convert a positive integer num into an m-bit bit vector"""
    return np.array(list(np.binary_repr(num).zfill(m))).astype(dtype=dtype)

class DIF(EncoderDecoder):
  def __init__(self, name='DIF', extension='.dif') -> None:
    super().__init__(name, extension)

  def encode(self, file_path, data_type='int8', res_dir=''):
    '''
    encoded strings are of type: string, start_idx, end_idx
    where start_idx represents the starting index (starting at 0)
    and end_idx represents the last index, (not to be included in the range)
    Params:
    - file_path: path of the file to encode
    - res_f_name: path + name to the output file
    '''
    # open file
    with open(file_path, 'r') as f:
      lines = np.fromfile(f, dtype=data_type, sep='\n')
    res_f_name = res_dir+file_path.split('/')[-1]+self.extension

    print(f'Encoding {len(lines)} lines.')
    print(lines)
    min, max = np.min(lines), np.max(lines)
    max_diff = max - min
    encoded = [lines[0]]
    first = True
    for index in range(1, len(lines)):
      diff = lines[index] - lines[index - 1]
      if diff <= max_diff:
        encoded.append(diff)
      else:
        encoded.append('&')
        encoded.append(lines[index])

    str_enc = ''
    for line in encoded:
      str_enc += str(line) + '\n'
    with open(res_f_name, 'w') as res:
      res.write(str_enc)


  def decode(self, file_path, data_type='int8', res_dir=''):
    """
    Description: This function decodes the file in file_path in the output file with name res_dir.

    Params:
        - file_path: path of the file to decode
        - res_dir: path to the output file
    """
    # open file
    with open(file_path, 'r') as f:
      lines = np.fromfile(f, dtype=data_type, sep='\n')
    print(f'Decoding {len(lines)} lines.')

    # define output file name
    res_f_name = res_dir+'dec_'+file_path.split('/')[-1]

    #####################################################################
    # TODO: decode everything in as a big string in res_str
    res_str = ""


    #####################################################################

    # write our results to file
    with open(res_f_name, 'w') as res:
      res.write(res_str)

    return res_str

  