class ExampleEncoderDecoder():

    def __init__(self):
        self.name = "Remember to assign a name to your solver."
        self.extension = 'Remember to assign a file extension for your solver.'


    def encode(self, file_path, data_type='int8', res_dir=''):
        """ 
        Description: This function encodes the file in file_path in the output file with name res_dir.

        Params:
            - file_path: path of the file to encode
            - res_dir: path to the output file
        """
        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        print(f'Encoding {len(lines)} lines.')

        # how to define output file name
        res_f_name = res_dir+file_path.split('/')[-1]+self.extension

        #####################################################################
        # TODO: encode everything in as a big string in res_str
        res_str = ""
        

        #####################################################################
        
        # write results to file
        with open(res_f_name, 'w') as res:
            res.write(res_str)

        return 0


    def decode(self, file_path, data_type='int8', res_dir=''):
        """
        Description: This function decodes the file in file_path in the output file with name res_dir.

        Params:
            - file_path: path of the file to decode
            - res_dir: path to the output file
        """
        # open file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        print(f'Decoding {len(lines)} lines.')

        # define output file name
        res_f_name = res_dir+'dec_'+file_path.split('/')[-1]

        #####################################################################
        # TODO: decode everything in as a big string in res_str
        res_str = ""


        #####################################################################

        # write our results to file
        with open(res_f_name, 'w') as res:
            res.write(res_str)

        return res_str