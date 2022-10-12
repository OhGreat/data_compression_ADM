from os import makedirs

class RLE():
    def __init__(self):
        pass

    def encode(self,data_path, res_f_name):
        """ encoded strings are of type: string, start_idx, end_idx
            where start_idx represents the starting index (starting at 0)
            and end_idx represents the last index, (not to be included in the range)
        """
        # open file
        with open(data_path, 'r') as f:
            lines = f.readlines()
        print(f'Encoding {len(lines)} lines.')

        # reset output file
        with open(res_f_name, 'w') as res:
            pass

        i = 0  # start index
        while i < len(lines):
            pairs = 1
            for j in lines[i+1:]:
                if lines[i] == j:
                    pairs += 1
                else:
                    break
            
            # write current res
            res_str = f'{lines[i].strip()}, {i}, {i+pairs}\n'
            with open(res_f_name, 'a') as res:
                res.write(res_str)
            
            # increment counter and break if done
            i += pairs

        # return number of lines
        with open(res_f_name, 'r') as res:
            res_len = len(res.readlines())
        return res_len


    def decode(self, file_path, res_f_name):
        
        # reset output file
        with open(res_f_name, 'w') as res:
            pass

        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        print(f'Decoding {len(lines)} lines.')

        for line in lines:
            elems = line.strip().split(sep=',')
            reps = int(elems[2]) - int(elems[1])
            # for _ in range(reps):
            with open(res_f_name, 'a') as res:
                res.write((elems[0]+'\n')*reps)

        # read length of output file
        with open(res_f_name, 'r') as res:
            res_len = len(res.readlines())

        return res_len
        



