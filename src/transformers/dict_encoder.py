class dict_enc():
    def __init__(self):
        self.name = "dict"
        self.extension = '.dic'

    def encode(self, data_path, res_f_name):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)

            Params:
            - file_path: path of the file to encode
            - res_f_name: path + name to the output file
        """
        # open file
        with open(data_path, 'r') as f:
            lines = f.readlines()
        print(f'Encoding {len(lines)} lines.')

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
                res.write(f"{key.strip()}|{item}\n")
            res.write(idxes)


    def decode(self, file_path, res_f_name):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path + name to the output file
        """
        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        print(f'Decoding {len(lines)} lines.')
        
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
