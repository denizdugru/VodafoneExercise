import pytest
import os
from csv_processor import CsvProcessor

INPUT_FILE = "test_input.csv"
OUTPUT_FILE = "test_output.csv"
MODE = "character_matching"

# defining test data
TEST_DATA = [
    {"Name": "Deniz Duğru", "Email": "deniz.dugru@gmail.com", "Billing": "100.50"},
    {"Name": "Test User", "Email": "test_user@example.com", "Billing": "200.75"},
]


# defining expected outputs
EXPECTED_OUTPUT = [
    {"Name": "XXXXX XXXXX", "Email": "XXXXX.XXXXX@XXXXX.XXX", "Billing": "150.6"},
    {"Name": "XXXX XXXX", "Email": "XXXX_XXXX@XXXXXXX.XXX", "Billing": "150.6"},
]


# creating and removing the required files
@pytest.fixture(scope="function")
def setup_teardown_encode():
    # writing sample csv file
    with open(INPUT_FILE, mode="w", newline="") as file:
        file.write("Name,Email,Billing\n")
        for row in TEST_DATA:
            file.write(f"{row['Name']},{row['Email']},{row['Billing']}\n")

    yield INPUT_FILE, OUTPUT_FILE, MODE

    os.remove(INPUT_FILE)
    os.remove(OUTPUT_FILE)


# creating and removing the required files
@pytest.fixture(scope="function")
def setup_teardown_mask_data():
    # writing sample csv file
    with open(INPUT_FILE, mode="w", newline="") as file:
        file.write("Name,Email,Billing\n")
        for row in TEST_DATA:
            file.write(f"{row['Name']},{row['Email']},{row['Billing']}\n")

    yield INPUT_FILE, MODE

    os.remove(INPUT_FILE)


def test_encode(setup_teardown_encode):
    input_file, output_file, mode = setup_teardown_encode
    processor = CsvProcessor()
    processor.encode(input_file=input_file, output_file=output_file, mode=mode)

    # check if output file exists
    assert os.path.exists(OUTPUT_FILE)

    # check if output matches expected output
    with open(OUTPUT_FILE, mode="r") as file:
        lines = file.readlines()
        # check if expected number of data exists
        assert len(lines) == len(EXPECTED_OUTPUT) + 1  # +1 for header
        for i, line in enumerate(lines[1:]):  # skip header line
            values = line.strip().split(",")
            assert values[0] == EXPECTED_OUTPUT[i]["Name"]
            assert values[1] == EXPECTED_OUTPUT[i]["Email"]
            assert values[2] == EXPECTED_OUTPUT[i]["Billing"]


def test_mask_sensitive_data(setup_teardown_mask_data):
    input_file, mode = setup_teardown_mask_data
    processor = CsvProcessor()
    processor.load_csv(input_file)
    processor.mask_sensitive_data(mode=mode)

    # check if Name and Email are masked
    for row in processor.data:
        assert row["Name"] == EXPECTED_OUTPUT[processor.data.index(row)]["Name"]
        assert row["Email"] == EXPECTED_OUTPUT[processor.data.index(row)]["Email"]


def test_calculate_and_display_stats():
    processor = CsvProcessor()

    # test with empty values
    column_name = "Test"
    values = []
    assert processor.calculate_and_display_stats(column_name, values) == (0, 0, 0)

    # test with non-empty values
    column_name = "Billing"
    values = [100.50, 200.75]
    assert processor.calculate_and_display_stats(column_name, values) == (
        200.75,
        100.50,
        150.6,
    )
