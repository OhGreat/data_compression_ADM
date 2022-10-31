import numpy as np
from solvers.encoder_decoder import EncoderDecoder
class BIN(EncoderDecoder):
    def __init__(self, data_type: str) -> None:
        super().__init__("BIN", '.bin', data_type)

    def encode(self, file_path, res_dir=''):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)

            Params:
            - file_path: path of the file to encode
            - res_f_name: path + name to the output file
        """

        lines = np.fromfile(file_path, dtype=self.data_type, sep='\n')
        print(f'Encoding {len(lines)} lines.')
        file_out = open(self.enc_file_path(file_path, res_dir), 'wb')

        for line in lines:
            file_out.write(self.byte(int(line)))

        return 0

    def decode(self, file_path, res_dir=''):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path + name to the output file
        """

        file_in = open(file_path, 'rb')
        file_out = open(self.dec_file_path(file_path, res_dir), 'w')

        data_bytes = file_in.read(self.byte_len)
        data = ''
        while data_bytes:
            read_data = self.number(data_bytes)
            data += str(read_data)+'\n'
            file_out.write(str(read_data)+'\n')
            data_bytes = file_in.read(self.byte_len)

        return data