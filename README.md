# Data compression with Python
The following repository is a benchmarking tool for encoding/decoding files.

## Installation and requirements
To use the following repository a Python >= 3.7 environment is required.

## Usage

### Running a single function
The `main.py` file in the src folder can be used to encode/decode a file. To run it you can use the following command with arguments:

```python 
python src/main.py <function> <method> <data_type> <file_path> <res_dir>
```
where:
- function: (str) can be *'en'* for encoding or *'de'* for decoding
- method: (str) can be one between *'bin', 'rle', 'dic', 'for', 'diff'* and represents the encoding/decoding method to use
- data_type: (str) represents the data type and should be one between: 'int8', 'int16', 'int32', 'int64', 'string'
- data_path: (str) string defining the path of the file to encode/decode
- res_dir: (str) defines the folder to save the results. If undefined, results will be saved in the current directory.


### Running experiments
Two main experimenter function have been created under `src/experimenter.py`. 

To run a single experiment the function *single_experiment* is available and is defined as below:
``` python
single_experiment(solver, data_path, res_dir=None, additional_info=None, keep_files=True)
```
where:
- solver: defines the method to use for the encoding/decoding part.
- data_path: defines the path of tthe file to use.
- res_dir: directory where to save results.
- additional_info: string containing additional notes we want to include in our result report.
- keep_files: when set to False the generated files of the experiment will be discarded.

To run a bulk experiment for various solvers and datasets, the function *bulk_experiment* can be used as follows:
``` python 
bulk_experiment(files_dir, solvers, additional_info='', res_dir='results/', keep_files=True)
```
where:
- files_dir: (str) directory containing all the files to experiment with.
- solvers: (list) list of methods to use for encoding/decoding
- additional_info: (str) additional information to be logged with each experiment
- res_dir: (str) directory to save results
- keep_files: when set to False the generated files of the experiment will be discarded.

Example calls of the above functions can be found at the end of the *src/experimenter.py* file.


### Implementing new methods
All encoders/decoders can be found under the `src/solvers` directory. A template of the structure can be found in the *ExampleEncoderDecoder.py* file. In general the rules that each new method needs to follow to work properly are the following:
- *self.name* and *self.extension* values must be defined.
- *encode* and *decode* methods must be defined.
- the *decode* method must return the plain decoded text, while *encode* should return 0.

Once a new solver has been implemented, it can be added in line 16 of the *src/main.py* file to be usable.