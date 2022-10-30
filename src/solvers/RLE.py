import readline
from solvers.encoder_decoder import EncoderDecoder
import numpy as np

class RLE(EncoderDecoder):
    def __init__(self, data_type: str) -> None:
        super().__init__("RLE", '.rle', data_type)
        
    def encode(self, file_path, res_dir=''):
        
        if self.data_type == 'string':
            with open(file_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = np.fromfile(file_path, dtype=self.data_type, sep='\n')
        
        print(f'Encoding {len(lines)} lines.')
        max_length = np.log2(len(lines))
        run_length_bytes = self.min_bytes_for(max_length)
        
        file_out = open(self.enc_file_path(file_path, res_dir), 'wb')
        file_out.write(self.byte(run_length_bytes, 1))
        
        i = 0
        data_len = len(lines)
        while i < data_len:
            run_length = 1
            j = i+1
            while j < data_len and lines[i] == lines[j]:
                run_length += 1
                j += 1
            
            bytes_to_write = lines[i][:-1].encode('utf-8') if self.data_type == 'string' else self.byte(int(lines[i]))
            file_out.write(
                bytes_to_write + self.byte(int(run_length), run_length_bytes) +b'\n'
            )
            
            i += run_length
        return 0

    def decode(self, file_path, res_dir=''):
        """ Params:
            - file_path: path of the file to decode
            - res_dir: results directory
        """
        
        file_in = open(file_path, 'rb')
        file_out = open(self.dec_file_path(file_path, res_dir), 'w')
        
        byte = file_in.read(1)
        run_length_bytes = self.number(byte)
        data = ''
        if self.data_type == 'string':
            data_bytes = file_in.readline()[:-1]
        else:
            data_bytes = file_in.read(self.byte_len)
            
        while data_bytes:
            if self.data_type == 'string':
                read_data = data_bytes[:-run_length_bytes].decode('utf-8')
                reps_bytes = data_bytes[-run_length_bytes:]
                reps = self.number(reps_bytes)
            else:
                read_data = self.number(data_bytes)
                reps_byte = file_in.read(run_length_bytes)
                reps = self.number(reps_byte)
            # read_data = data_bytes.decode('utf-8') if self.data_type == 'string' else self.number(data_bytes)
            # read_data =
            # print(read_data)
            data += (str(read_data)+'\n')*reps
            file_out.write((str(read_data)+'\n')*reps)
            if self.data_type == 'string':
                data_bytes = file_in.readline()[:-1]
            else:
                data_bytes = file_in.read(self.byte_len)
            
        return data
