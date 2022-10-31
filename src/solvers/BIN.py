import numpy as np

from solvers.encoder_decoder import EncoderDecoder

class BIN(EncoderDecoder):
    def __init__(self, data_type):
        super().__init__('BIN', '.bin', data_type)

    def encode(self, file_path, res_dir=''):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)

            Params:
            - file_path: path of the file to encode
            - res_f_name: path + name to the output file
        """
        with open(file_path, 'r') as f:
            lines = np.fromfile(f, dtype=self.data_type, sep='\n')
        print(f'Encoding {len(lines)} lines.')

        file_out = open(self.enc_file_path(file_path, res_dir), 'wb')

        max_num = int(abs(max(lines, key=abs)))
        byte_len = self.min_bytes_for(max_num)*2
        if byte_len > self.byte_len:
            byte_len = self.byte_len
        # print(byte_len)
        byte_len_enc = self.byte(byte_len, 1)

        file_out.write(
            byte_len_enc
        )
        for number in lines:
            file_out.write(self.byte(int(number), byte_len))

        file_out.close()
        return 0

    def decode(self, file_path, res_dir=''):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path + name to the output file
        """

        # data_length = self.get_data_length(data_type)

        file_in = open(file_path, 'rb')

        out_path = self.dec_file_path(file_path, res_dir)
        file_out = open(out_path, 'w')

        with open(file_path, "rb") as file:
            data = file.read(1)
            byte_len = self.number(data)
            while (data := file.read(byte_len)):
                # data = file.read(byte_len)
                write_out = self.number(data)
                file_out.write('{}\n'.format(write_out))

        file_in.close()
        file_out.close()
