import numpy as np

# Local import
from solvers.encoder_decoder import EncoderDecoder

class FOR(EncoderDecoder):
  def __init__(self, data_type:str, **kwargs) -> None:
    if 'diff_thres' in kwargs:
      self.diff_thres = kwargs['diff_thres']
      name = f'FOR{self.diff_thres}'
    else: 
      self.diff_thres = None
      name = 'FOR'
    super().__init__(name, '.for', data_type)

  def encode(self, file_path, res_dir=''):
    '''
    encoded strings are of type: string, start_idx, end_idx
    where start_idx represents the starting index (starting at 0)
    and end_idx represents the last index, (not to be included in the range)
    Params:
    - file_path: path of the file to encode
    - res_f_name: path + name to the output file
    '''
    with open(file_path, 'r') as f:
      lines = np.fromfile(f, dtype=self.data_type, sep='\n')
    print(f'Encoding {len(lines)} lines.')

    if self.diff_thres == None:
      diff_thres = int(abs(max(np.diff(lines),key=abs)))+1
    else:
      diff_thres = self.diff_thres

    frame = int(np.mean(lines))
    max_min_diff = int(np.max(lines) - np.min(lines))*2
    byte_len = self.min_bytes_for(max_min_diff)
    separator = int(-(2**(byte_len*8)-2)/2)
    max_num = int(abs(max(lines, key=abs)))
 
    if max_num == separator:
      byte_len += 1
      separator = int(-(2**(byte_len*8)-2)/2)

    max_separator = self.byte(separator, byte_len)
    encoding_len = self.byte(byte_len, 1)
    frame_enc = self.byte(int(frame), byte_len)

    file_out = open(self.enc_file_path(file_path, res_dir), 'wb')

    file_out.write(
        encoding_len
    )
    file_out.write(
        max_separator
    )
    file_out.write(
        frame_enc
    )

    for index in range(len(lines)):
      diff = lines[index] - frame
      if abs(diff) <= diff_thres:       
        bytes_to_write = self.byte(int(diff), byte_len)
      else:
        bytes_to_write = self.byte(separator, byte_len) + self.byte(int(lines[index]), byte_len)
      file_out.write(
          bytes_to_write 
      )
    
    return 0



  def decode(self, file_path, res_dir=''):
    """
    Description: This function decodes the file in file_path in the output file with name res_dir.

    Params:
        - file_path: path of the file to decode
        - res_dir: path to the output file
    """

    with open(file_path, "rb") as file:
      data = file.read(1)
      byte_len = self.number(data)
      data = file.read(byte_len)
      separator = int(self.number(data))
      data = file.read(byte_len)
      frame = self.number(data)
      decoded = []
      while (data := file.read(byte_len)):
        # if special character simulation found
        if self.number(data) == separator:
          decoded.append(self.number(file.read(byte_len)))
        else:
          summation = self.number(data) + frame
          decoded.append(summation)
    res_f_name = self.dec_file_path(file_path, res_dir)

    res_str = ''
    for line in decoded:
      res_str += str(line) + '\n'
      
    with open(res_f_name, 'w') as res:
      res.write(res_str)

    return res_str

  