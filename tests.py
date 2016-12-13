import csv
import os

from util import export_to_csv

FILE_NAME = 'test.csv'


def setup_function(function):
    '''
    setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    '''
    pass


def teardown_function(function):
    '''
    Teardown any state that was previously setup with a setup_function call
    '''
    os.remove(FILE_NAME)


def test_export_to_csv():
    df = [
        {"col1": 1, "col2": 2},
        {"col1": 5, "col2": 5}
    ]

    rows = [
        ['col1', 'col2'],
        ['1', '2'],
        ['5', '5']
    ]

    export_to_csv(df, FILE_NAME)

    assert os.path.isfile(FILE_NAME)
    reader = csv.reader(open(FILE_NAME))

    for expected, found in zip(rows, reader):
        for item in found:
            assert item in expected


if __name__ == '__main__':
    test_export_to_csv()
