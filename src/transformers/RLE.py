class RLE():
    def __init__(self):
        self.name = "RLE"
        self.extension = '.rle'

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
        # we encode everything as a big string
        res_str = ''
        i = 0  # start index
        data_len = len(lines)
        while i < data_len:
            pairs = 1
            j = i+1
            while j < data_len and lines[i] == lines[j]:
                pairs += 1
                j += 1
            # add curr data to string (and remove newline [:-1])
            res_str += f'{lines[i][:-1]}| {i}| {i+pairs}\n'
            # increment counter of visited lines
            i += pairs
        # write results to file
        with open(res_f_name, 'w') as res:
            res.write(res_str)


    def decode(self, file_path, res_f_name):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path + name to the output file
        """
        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        print(f'Decoding {len(lines)} lines.')
        # we encode everything as a big string
        res_str = ''
        for line in lines:
            # get elements
            elems = line.split(sep='|')
            # count occurrences
            reps = int(elems[-1].strip()) - int(elems[-2].strip())
            # append curr results to string
            res_str += (''.join(elems[:-2])+'\n')*reps
        # write our results to file
        with open(res_f_name, 'w') as res:
            res.write(res_str)

        



