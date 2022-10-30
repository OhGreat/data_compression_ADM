from statistics import mean

class FOR():

    def __init__(self):
        self.name = "for"
        self.extension = '.for_block'

    def encode(self, file_path, data_type='int8', res_dir='', **kwargs):
        """ 
        Description: This function encodes the file in file_path in the output file with name res_dir.

        Params:
            - file_path: path of the file to encode
            - res_dir: path to the output file
        """
        # define output file name
        res_f_name = res_dir+file_path.split('/')[-1]+self.extension

        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
            len_lines = len(lines)
        print(f'Encoding {len_lines} lines.')

        block_size = 256
        if 'block_size' in kwargs:
            block_size = kwargs['block_size']

        curr_l = 0
        encoded = ''
        while curr_l < len_lines:
            if curr_l % block_size == 0:
                terminator = curr_l + block_size
                if terminator > len_lines:
                    terminator = len_lines
                curr_ref = mean([int(line.strip()) for line in lines[curr_l: terminator]])
                encoded += str(curr_ref) + '\n'
            encoded += str(int(lines[curr_l].strip()) - curr_ref) + '\n'
            curr_l += 1
        
        with open(res_f_name, 'w') as res:
            res.write(encoded)
        

    def decode(self, file_path, data_type='int8', res_dir='', **kwargs):
        """
        Description: This function decodes the file in file_path in the output file with name res_dir.

        Params:
            - file_path: path of the file to decode
            - res_dir: path to the output file
        """

        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
            len_lines = len(lines)
        # print(f'Decoding {len_lines} lines.')

        # define output file name
        res_f_name = res_dir+'dec_'+file_path.split('/')[-1]

        # we need to offset the block size by 1
        block_size = 256 + 1
        if 'block_size' in kwargs:
            block_size = kwargs['block_size'] + 1

        # we encode everything as a big string
        # res_str = ''
        # for line in lines:
        #     new_l = str(ref_val+int(line.strip())) + '\n'
        #     res_str += new_l

        curr_l = 0
        res_str = ''
        while curr_l < len_lines:
            if curr_l % block_size == 0:
                curr_ref = int(lines[curr_l].strip())
            else:
                res_str += str(int(lines[curr_l].strip()) + curr_ref)+'\n'
            curr_l += 1

        # write our results to file
        with open(res_f_name, 'w') as res:
            res.write(res_str)

        return res_str