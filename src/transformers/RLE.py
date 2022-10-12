from os import makedirs

class RLE():
    def __init__(self):
        pass

    def encode(self,data_path, res_f_name):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)

            Params:
            - file_path: path of the file to decode
            - res_f_name: path to the output file
        """
        # open file
        with open(data_path, 'r') as f:
            lines = f.readlines()
        print(f'Encoding {len(lines)} lines.')

        # reset output file
        with open(res_f_name, 'w') as res:
            pass

        res_str = ''  # we encode everything as a big string
        i = 0  # start index
        data_len = len(lines)
        while i < data_len:
            pairs = 1
            j = i+1
            while j < data_len and lines[i] == lines[j]:
                pairs += 1
                j += 1

            # add curr data to string
            res_str += f'{lines[i].strip()}, {i}, {i+pairs}\n'
            
            # increment counter of visited lines
            i += pairs

        # write results to file
        with open(res_f_name, 'a') as res:
            res.write(res_str)



    def decode(self, file_path, res_f_name):
        """ Params:
            - file_path: path of the file to decode
            - res_f_name: path to the output file
        """
        
        # reset output file
        with open(res_f_name, 'w') as res:
            pass

        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        print(f'Decoding {len(lines)} lines.')

        res_str = ''  # we encode everything as a big string
        for line in lines:
            # get elements
            elems = line.strip().split(sep=',')
            # count occurrences
            reps = int(elems[2]) - int(elems[1])
            
            res_str += (elems[0]+'\n')*reps

        with open(res_f_name, 'a') as res:
            res.write(res_str)

        



