from difflib import diff_bytes
import numpy as np

# Local import
from solvers.encoder_decoder import EncoderDecoder


class DIF(EncoderDecoder):
  def __init__(self, data_type) -> None:
    super().__init__('DIF', '.dif', data_type)

  def encode(self, file_path, res_dir='', **kwargs):
    '''
    encoded strings are of type: string, start_idx, end_idx
    where start_idx represents the starting index (starting at 0)
    and end_idx represents the last index, (not to be included in the range)
    Params:
    - file_path: path of the file to encode
    - res_f_name: path + name to the output file
    '''
    # open file
    # print(self.data_type)
    with open(file_path, 'r') as f:
      lines = np.fromfile(f, dtype=self.data_type, sep='\n')
    print(lines[:25])
    res_f_name = self.enc_file_path(file_path, res_dir)
    print(f'Encoding {len(lines)} lines.')

    if 'diff_thres' in kwargs:
      diff_thres = kwargs['diff_thres']
    else:
      diff_thres = int(abs(max(np.diff(lines),key=abs)))+1
    diff_thres = 10
    print(diff_thres)
    max_min_diff = int(np.max(lines) - np.min(lines))*2
    print(max_min_diff)
    # print(max(lines, key=abs))
    byte_len = self.min_bytes_for(max_min_diff)
    # byte_len = int(self.min_bytes_for(int(max(lines, key=abs))))
    print(byte_len)
    file_out = open(self.enc_file_path(file_path, res_dir), 'wb')

    encoding_len = self.byte(byte_len, self.byte_len)
    max_diff_enc = self.byte(diff_thres, byte_len)
    first = self.byte(int(lines[0]), byte_len)

    file_out.write(
        encoding_len
    )
    file_out.write(
        max_diff_enc
    )
    file_out.write(
        first
    )

    for index in range(1, len(lines)):
      diff = lines[index] - lines[index - 1]
      # print(int(diff), diff_thres)
      if abs(diff) < diff_thres:       
        bytes_to_write = self.byte(int(diff), byte_len)
      else:
        bytes_to_write = self.byte(int(lines[index]), byte_len)
      file_out.write(
          bytes_to_write 
      )
    



  def decode(self, file_path, res_dir=''):
    """
    Description: This function decodes the file in file_path in the output file with name res_dir.

    Params:
        - file_path: path of the file to decode
        - res_dir: path to the output file
    """

    with open(file_path, "rb") as file:
      print(self.byte_len)
      data = file.read(self.byte_len)
      byte_len = self.number(data)
      print(byte_len)
      data = file.read(byte_len)
      max_diff = int(self.number(data))

      data = file.read(byte_len)
      first = self.number(data)
      decoded = [first]
      while (data := file.read(byte_len)):
        # if difference exceeds threshold (special character simulation)
        if abs(self.number(data)) >= max_diff:
          # print('here')
          decoded.append(self.number(data))
        else:
          summation = self.number(data) + decoded[-1] 
          decoded.append(summation)

    res_f_name = self.dec_file_path(file_path, res_dir)

    res_str = ''
    for line in decoded:
      res_str += str(line) + '\n'
      
    with open(res_f_name, 'w') as res:
      res.write(res_str)

    return res_str

  