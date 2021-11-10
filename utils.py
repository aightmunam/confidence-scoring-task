"""
Utils and helpers
"""

import csv
import logging
import math

log = logging.getLogger(__name__)


def sigmoid(value):
    """
    Return a high score (closer to 1) if the value is small and return a
    low score (closer to 0) if the value is big.

    Args:
        value (float): The value for which to find the score

    Returns:
        float: Score in the range 0-1
    """
    sig = (1 / (1 + math.exp(-value))) * 2 - 1
    return 1 - sig


def get_data_from_file(filename, key_name):
    """
    Return the data from the csv file as a dictionary

    Args:
        filename (str): Name of the file to parse
        key_name (str): Attribute to use as the key for a row

    Returns:
        dict: A dictionary containing the data from the file
    """
    with open(filename, mode='r') as csv_file:
        log.info(f'Processing {filename} for data')
        file_data = {}
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            file_data[row[key_name]] = row
            line_count += 1

        log.info(f'Loaded {line_count} rows from {filename}')
        return file_data


def write_data_to_file(data, fields_to_write, filename=None):
    """
    Write data from a list of dictionaries to the given filename

    Args:
        data (list): A list of dicts to write to the file
        filename (str): Filename for the output file
        fields_to_write (list): Fields to include in the output file
    """
    filename = 'output.csv' if not filename else filename
    output_path = f'output/{filename}'
    with open(output_path, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields_to_write, delimiter=';')
        writer.writeheader()
        writer.writerows(data)
        log.info(f'Writing POI scores to file: {filename}')

