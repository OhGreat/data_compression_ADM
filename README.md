# Data compression with Python
The following repository is a benchmarking tool for encoding/decoding files.

## Installation and requirements
To use the following repository a `Python >= 3.7` environment is required, together with the packages defined in the `requirements.txt` file. 
To install the required packages you can use the following comamnd:
```
pip install requirements.txt
```

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

A single experiment consists in an encoding and decoding routine of a given file, collecting statistics of the run. The function is available under the name *single_experiment* and is defined as below:
``` python
single_experiment(solver, data_path, res_dir=None, additional_info=None, keep_files=True, data_type='int8', **kwargs)
```
where:
- solver: defines the method to use for the encoding/decoding part.
- data_path: defines the path of tthe file to use.
- res_dir: directory where to save results.
- additional_info: string containing additional notes we want to include in our result report.
- keep_files: when set to False the generated files of the experiment will be discarded.
- data_type: defines the files of the directory to use in the experiment.
- kwargs: additional keyword arguments that should be passed to the encode and decode functions

The output of the *single_experiment* function can be found in the defined results folder. In addition to the encoded and decoded files, a *.out* file is created containing the statistics collected.

To run a bulk experiment for various solvers and datasets, the function *bulk_experiment* can be used as follows:
``` python 
bulk_experiment(files_dir, solvers, additional_info='', res_dir='results/', keep_files=True, data_type='int8', **kwargs)
```
where:
- files_dir: (str) directory containing all the files to experiment with.
- solvers: (list) list of methods to use for encoding/decoding
- additional_info: (str) additional information to be logged with each experiment
- res_dir: (str) directory to save results
- keep_files: when set to False the generated files of the experiment will be discarded.
- data_type: defines the files of the directory to use in the experiment.
- kwargs: additional keyword arguments that should be passed to the encode and decode functions

The bulk experimenter is simply a generalization of the single experiment defined above.

Example calls of the above functions can be found at the end of the *src/experimenter.py* file.


### Implementing new methods
All encoders/decoders can be found under the `src/solvers` directory. A template of the structure can be found in the *ExampleEncoderDecoder.py* file. Each new method needs to meet the following requirements to work properly:
- *self.name* and *self.extension* values must be defined.
- *encode* and *decode* methods must be defined.
- the *decode* method must return the plain decoded text, while *encode* should return 0.

Once a new solver has been implemented, it can be imported and added in line 27 of the *src/main.py* file to be usable. For the experimenter file just import it in the beginning of the file.