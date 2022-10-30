from base64 import encode
import math
import numpy as np

# Local import
from solvers.encoder_decoder import EncoderDecoder


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

    min, max = np.min(lines), np.max(lines)
    max_diff = max - min
    encoded = [lines[0]]
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

    decoded = [lines[0]]
    for index in range(1, len(lines)):
      if lines[index] =='&':
        del lines[index]
        decoded.append(lines[index])
        
      else:
        sum = lines[index] + decoded[index - 1]
        decoded.append(sum)

    # define output file name
    res_f_name = res_dir+'dec_'+file_path.split('/')[-1]

    res_str = ''
    for line in decoded:
      res_str += str(line) + '\n'
    with open(res_f_name, 'w') as res:
      res.write(res_str)

    return res_str

  