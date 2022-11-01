from solvers.encoder_decoder import EncoderDecoder
import numpy as np

class RLE(EncoderDecoder):
    def __init__(self, data_type: str) -> None:
        super().__init__("RLE", '.rle', data_type)
        
        
    def encode(self, file_path, res_dir=''):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)

            Params:
            - file_path: path of the file to encode
            - res_f_name: path + name to the output file
        """
        if self.data_type == 'string':
            with open(file_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = np.fromfile(file_path, dtype=self.data_type, sep='\n')
        
        print(f'Encoding {len(lines)} lines.')
        max_length = len(lines)
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
            
            if self.data_type == 'string':
                file_out.write(
                    lines[i].encode('utf-8') + \
                        self.byte(int(run_length), run_length_bytes)
                )
            else:
                file_out.write(
                    self.byte(int(lines[i])) + \
                        self.byte(int(run_length), run_length_bytes)
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
        data_str = ''
        if self.data_type == 'string':
            data_bytes = file_in.readline()
            data_bytes = data_bytes[:-1]
        else:
            data_bytes = file_in.read(self.byte_len)

        while data_bytes:
            data = self.number(data_bytes) if self.data_type != 'string' else data_bytes.decode('utf-8')
            reps_byte = file_in.read(run_length_bytes)
            reps = self.number(reps_byte)
            data_str += (str(data)+'\n')*reps
            file_out.write((str(data)+'\n')*reps)
            if self.data_type == 'string':
                data_bytes = file_in.readline()
                data_bytes = data_bytes[:-1]
            else:
                data_bytes = file_in.read(self.byte_len)
            
        return data_str