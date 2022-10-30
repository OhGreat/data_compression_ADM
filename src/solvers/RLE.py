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
        
        lines = np.fromfile(f, dtype=self.data_type, sep='\n')
        max_diff = np.max(lines) - np.min(lines)
        
        print(f'Encoding {len(lines)} lines.')
        file_out = open(self.enc_file_path(file_path, res_dir), 'wb')

        i = 0
        data_len = len(lines)
        while i < data_len:
            run_length = 1
            j = i+1
            while j < data_len and lines[i] == lines[j]:
                run_length += 1
                j += 1
            
            file_out.write(
                self.byte(int(lines[i][:-1])) + self.byte(int(run_length))
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

        byte = file_in.read(self.byte_len)
        data = ''
        while byte:
            # start_pos_byte = file_in.read(self.byte_len)
            reps_byte = file_in.read(self.byte_len)
            reps = int.from_bytes(reps_byte, byteorder='big', signed=True)
            number = int.from_bytes(byte, byteorder='big', signed=True)
            file_out.write((str(number)+'\n')*reps)
            byte = file_in.read(self.byte_len)
            
        return data
