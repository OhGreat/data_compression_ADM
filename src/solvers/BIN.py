class BIN():
    def __init__(self, data_type):
        self.name = "BIN"
        self.extension = '.bin'

    def get_data_length(self, data_type):
        ''' returns bytes needed to store each type'''
        if data_type == 'int8':
            return 1
        elif data_type == 'int16':
            return 2
        elif data_type == 'int32':
            return 4
        elif data_type == 'int64':
            return 8

    def encode(self, file_path, data_type, res_dir=''):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)

            Params:
            - file_path: path of the file to encode
            - res_f_name: path + name to the output file
        """
        data_length = self.get_data_length(data_type)

        file_in = open(file_path, 'r')
        file_out_path = res_dir+file_path.split('/')[-1]+self.extension
        file_out = open(file_out_path, 'wb')

        for i in file_in:
            file_out.write(int(i.replace('\n', '')).to_bytes(
                data_length, byteorder='big', signed=True))

        file_in.close()
        file_out.close()
        return 0

    def decode(self, file_path, data_type, res_dir=''):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path + name to the output file
        """

        data_length = self.get_data_length(data_type)

        file_in = open(file_path, 'rb')
        file_out_path = res_dir+file_path.split('/')[-1]+'.csv'
        file_out = open(file_out_path, 'w')

        bytes = file_in.read(data_length)
        while bytes:
            file_out.write('{}\n'.format(int.from_bytes(bytes, byteorder='big', signed=True)))
            bytes = file_in.read(data_length)

        file_in.close()
        file_out.close()

        with open(file_out_path, 'r') as f:
            lines = f.readlines()
            return ''.join(lines)