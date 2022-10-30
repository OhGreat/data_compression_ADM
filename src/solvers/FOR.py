import numpy as np

# Local import
from solvers.encoder_decoder import EncoderDecoder


class FOR(EncoderDecoder):
  def __init__(self, name='FOR', extension='.for') -> None:
    super().__init__(name, extension)

  def encode(self, file_path, data_type='int8', res_dir='', **kwargs):
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

    if 'diff_thres' in kwargs:
      diff_thres = kwargs['diff_thres']
    else:
      diff_thres = (np.max(lines) - np.min(lines))
    frame = int(np.mean(lines))
    encoded = [frame]
    for index in range(len(lines)):
      diff = lines[index] - frame
      if diff <= diff_thres:
        encoded.append(diff)
      else:
        encoded.append(f'&{lines[index]}')

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
      lines = f.readlines()
    print(f'Decoding {len(lines)} lines.')

    frame = int(lines[0])
 
    decoded = []
    for index in range(1, len(lines)):
      curr_line = lines[index].rstrip()
      # if we reach special character
      if curr_line[0] == '&':
        decoded.append(int(curr_line[1:]))
      else:
        summation = int(curr_line) + frame
        decoded.append(summation)

    # define output file name
    res_f_name = res_dir+'dec_'+file_path.split('/')[-1]

    res_str = ''
    for line in decoded:
      res_str += str(line) + '\n'
      
    with open(res_f_name, 'w') as res:
      res.write(res_str)

    return res_str

  