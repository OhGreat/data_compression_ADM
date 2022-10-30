class DIC():
    def __init__(self):
        self.name = "DIC"
        self.extension = '.dic'

    def encode(self, file_path, data_type='int8', res_dir=''):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)

            Params:
            - file_path: path of the file to encode
            - res_f_name: path + name to the output file
        """
        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        print(f'Encoding {len(lines)} lines.')

        # define output file name
        res_f_name = res_dir+file_path.split('/')[-1]+self.extension
        print(res_f_name)

        # create keys
        keys = {}
        counter = 0
        for line in lines:
            if line not in keys:
                keys[line] = counter
                counter += 1

        # create array of dictionary keys
        idxes = ''
        for line in lines:
            idxes+=str(keys[line])+','

        # write results to file
        with open(res_f_name, 'w') as res:
            for key, item in keys.items():
                res.write(f"{key[:-1]}|{item}\n")
            res.write(idxes)
        
        return 0


    def decode(self, file_path, data_type='int8', res_dir=''):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path + name to the output file
        """
        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        # print(f'Decoding {len(lines)} lines.')

        # define output file name
        res_f_name = res_dir+'dec_'+file_path.split('/')[-1]
        
        # create dict
        keys = {}
        for line in lines[:-1]:
            elem = line.split('|')
            item = ''.join(elem[:-1])
            key = int(elem[-1])
            if key not in keys:
                keys[key] = item
        
        # create my idxes
        idxes = lines[-1].strip().split(',')
        idxes = [int(i) for i in idxes[:-1]]
        
        # create output string
        res_str = ''
        for i in idxes:
            res_str += keys[i]+'\n'

        # write our results to file
        with open(res_f_name, 'w') as res:
            res.write(res_str)

        return res_str
