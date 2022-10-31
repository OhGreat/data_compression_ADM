import numpy as np
from math import ceil

class EncoderDecoder():
  def __init__(self, name:str, extension:str, data_type:str) -> None:
    self.name = name
    self.extension = extension
    self.data_type = data_type
    self.byte_len = self.get_byte_length(data_type)
    return

  def encode(self):
    pass

  def decode(self):
    pass
  
  def enc_file_path(self, file_path, res_dir):
    return res_dir+file_path.split('/')[-1]+self.extension
  
  def dec_file_path(self, file_path, res_dir):
    return res_dir+file_path.split('/')[-1]+'.csv'
  
  def get_byte_length(self, data_type):
    ''' returns bytes needed to store each type'''
    if data_type == 'int8':
      return 1
    elif data_type == 'int16':
      return 2
    elif data_type == 'int32':
      return 4
    elif data_type == 'int64':
      return 8
    elif data_type == 'string':
      return 1
      
  def min_bytes_for(self, number):
    if number == 0:
      return 1
    else:
      return ceil(number.bit_length() / 8.0)
      # return (number.bit_length() + 7) // 8
    # return int(np.ceil(
    #         int(np.log2(number+1)+1) / 8
    #     ))
    

  def byte(self, number, byte_len=None):
    if byte_len is None:
      byte_len = self.byte_len
      # byte_len = (8 + (number + (number < 0)).bit_length()) // 8
    
    return number.to_bytes(
                  length=byte_len,
                  byteorder='big',
                  signed=True
                )
  
  def number(self, byte):
    return int.from_bytes(
      byte,
      byteorder='big',
      signed=True
    )