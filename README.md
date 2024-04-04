# Vodafone Exercise

## Project overview
The main goal of this project is to extract data from a sample CSV file, save it to an output CSV file with masked data, without using any dependencies.


## Features
* **csv writer/reader**: Added a CSV reader and writer.
* **data masking**: Added a masking logic for specified characters in the data, which can be configured.
* **statistics calculator**: Added a function to calculate the maximum, minimum, and average values of a given list of values and display them.

## Requirements
- The project has been created and tested on macOS M2 setup.
- Python 3.6 or higher is required to run project.
- The following requirements are needed to run the additional pytest cases, which can be installed using the provided requirements.txt file.

## Installation
1. Clone the repository:
```bash
git clone <repository_url>
```
2. If you want to run the test cases, create a virtual environment with the following command:
```bash
python3 -m venv <your_env_file>
```

Activate the virtual environment and install the requirements:
```bash
source <your_env_file>/bin/activate
pip install -r reqs/requirements.txt
```

**Note**: Check the [documentation](https://docs.python.org/3/library/venv.html) for other operating systems.

3. Make sure the there is the sample CSV file in assets folder for the demo.

## Usage

### Running the Program

1. To run the program:
```bash
python3 csv_processor.py
```
2. After the program has successfully run, you will see the result as:

```bash
Name: Max. 18, Min. 9, Avg. 12.4
Billing: Max. 53000.0, Min. 12400.27, Avg. 25100.1
```

### Running Test Cases

1. To run the test cases:
```bash
pytest test_csv_processor.py
```
**Note**: Make sure you have successfully installed pytest in order to run the test cases. You can check by running:
```bash
pytest --version
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
