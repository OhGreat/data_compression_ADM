import numpy as np
from solvers.encoder_decoder import EncoderDecoder
class DIC(EncoderDecoder):
    def __init__(self, data_type: str) -> None:
        super().__init__("DIC", '.dic', data_type)

    def encode(self, file_path, data_type='int8', res_dir=''):
        
        if self.data_type == 'string':
            with open(file_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = np.fromfile(file_path, dtype=self.data_type, sep='\n')
        
        print(f'Encoding {len(lines)} lines.')

        file_out = open(self.enc_file_path(file_path, res_dir), 'wb')

        # create keys
        keys = {}
        counter = 0
        for line in lines:
            if line not in keys:
                keys[line] = counter
                counter += 1

        max_length = int(np.max(len(lines)))
        max_length_bytes = int(np.max([self.min_bytes_for(max_length), self.min_bytes_for(counter)]))

        # write dict size
        file_out.write(self.byte(int(max_length_bytes)))
        file_out.write(self.byte(counter, max_length_bytes))
        # write dict items to file
        for key, value in keys.items():
            if self.data_type == 'string':
                file_out.write(key.encode('utf-8'))
                file_out.write(self.byte(int(value), max_length_bytes))
            else:
                file_out.write(self.byte(int(key)))
                file_out.write(self.byte(int(value)))

        new_lines = [keys[line] for line in lines]
        # write new values to file
        for line in new_lines:
                file_out.write(self.byte(int(line), max_length_bytes))
        
        return 0


    def decode(self, file_path, data_type='int8', res_dir=''):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path + name to the output file
        """

        file_in = open(file_path, 'rb')
        file_out = open(self.dec_file_path(file_path, res_dir), 'w')

        max_length_bytes = self.number(file_in.read(self.byte_len))
        dict_size = self.number(file_in.read(max_length_bytes))
        keys = {}
        for _ in range(dict_size):
            if self.data_type == 'string':
                key_bytes = file_in.readline()[:-1]
                key = key_bytes.decode('utf-8')
                value_bytes = file_in.read(max_length_bytes)
                value = self.number(value_bytes)
            else:
                key_bytes = file_in.read(self.byte_len)
                key = self.number(key_bytes)
                value_bytes = file_in.read(self.byte_len)
                value = self.number(value_bytes)
            keys[value] = key

        data_bytes = file_in.read(max_length_bytes)
        lines = []
        while data_bytes:
            lines.append(self.number(data_bytes))
            data_bytes = file_in.read(max_length_bytes)

        data = ''
        for line in lines:
            if self.data_type == 'string':
                original_line_value = keys[line]+'\n'
            else:
                original_line_value = str(keys[line])+'\n'
            data += original_line_value
            file_out.write(original_line_value)
            
        return data
