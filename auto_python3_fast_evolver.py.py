import random
import string
import os
import time
import datetime
import json
import shutil
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_int(min_value, max_value):
    return random.randint(min_value, max_value)

def generate_random_float(min_value, max_value):
    return random.uniform(min_value, max_value)

def generate_random_bool():
    return random.choice([True, False])

def generate_random_list(min_length, max_length, data_type):
    if data_type == 'int':
        return [generate_random_int(-1000000, 1000000) for _ in range(random.randint(min_length, max_length))]
    elif data_type == 'float':
        return [generate_random_float(-1000000.0, 1000000.0) for _ in range(random.randint(min_length, max_length))]
    elif data_type == 'bool':
        return [generate_random_bool() for _ in range(random.randint(min_length, max_length))]
    elif data_type == 'str':
        return [generate_random_string(10) for _ in range(random.randint(min_length, max_length))]
    else:
        raise ValueError('Invalid data type')

def generate_random_dict(min_keys, max_keys, data_type):
    keys = [generate_random_string(10) for _ in range(random.randint(min_keys, max_keys))]
    values = generate_random_list(min_keys, max_keys, data_type)
    return dict(zip(keys, values))

def generate_random_dataframe(rows, columns, data_type):
    data = np.random.rand(rows, columns)
    if data_type == 'int':
        return pd.DataFrame(np.round(data * 1000000)).astype(int)
    elif data_type == 'float':
        return pd.DataFrame(data)
    elif data_type == 'bool':
        return pd.DataFrame(np.random.randint(0, 2, size=(rows, columns)).astype(bool))
    elif data_type == 'str':
        return pd.DataFrame([generate_random_string(10) for _ in range(rows * columns)]).astype(str).reshape((rows, columns))
    else:
        raise ValueError('Invalid data type')

def plot_dataframe(df):
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar')
    plt.title('Random DataFrame')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.show()

def main():
    print('Fast Evolver v1.0')
    print('-------------------')
    print('Generating random data...')
    print('-------------------')

    data_type = input('Enter data type (int, float, bool, str): ')
    min_length = int(input('Enter minimum list length: '))
    max_length = int(input('Enter maximum list length: '))
    min_keys = int(input('Enter minimum dictionary keys: '))
    max_keys = int(input('Enter maximum dictionary keys: '))
    rows = int(input('Enter number of rows for dataframe: '))
    columns = int(input('Enter number of columns for dataframe: '))

    random_data = generate_random_list(min_length, max_length, data_type)
    random_dict = generate_random_dict(min_keys, max_keys, data_type)
    random_df = generate_random_dataframe(rows, columns, data_type)

    print('Random List:', random_data)
    print('Random Dictionary:', random_dict)
    print('Random DataFrame:')
    print(random_df)

    plot_dataframe(random_df)

if __name__ == '__main__':
    main()