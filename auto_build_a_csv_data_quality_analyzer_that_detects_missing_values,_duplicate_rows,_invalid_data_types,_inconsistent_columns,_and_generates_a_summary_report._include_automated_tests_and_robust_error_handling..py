import csv
import pandas as pd
import numpy as np
import unittest
from datetime import datetime

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"File {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing file {file_path}.")
        return None

def detect_missing_values(df):
    missing_values = df.isnull().sum()
    return missing_values

def detect_duplicate_rows(df):
    duplicate_rows = df.duplicated().sum()
    return duplicate_rows

def detect_invalid_data_types(df):
    invalid_types = df.apply(lambda x: x.dtype != np.number if x.dtype != object else True).sum()
    return invalid_types

def detect_inconsistent_columns(df):
    inconsistent_columns = df.apply(lambda x: len(set(x)) != len(x)).sum()
    return inconsistent_columns

def generate_summary_report(df, missing_values, duplicate_rows, invalid_types, inconsistent_columns):
    report = {
        "Missing Values": missing_values.to_dict(),
        "Duplicate Rows": duplicate_rows,
        "Invalid Data Types": invalid_types,
        "Inconsistent Columns": inconsistent_columns
    }
    return report

def save_report_to_csv(report, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Metric", "Value"])
        for metric, value in report.items():
            if isinstance(value, dict):
                for column, count in value.items():
                    writer.writerow([f"{metric} in {column}", count])
            else:
                writer.writerow([metric, value])

def main():
    file_path = input("Enter the CSV file path: ")
    df = load_csv(file_path)
    if df is not None:
        missing_values = detect_missing_values(df)
        duplicate_rows = detect_duplicate_rows(df)
        invalid_types = detect_invalid_data_types(df)
        inconsistent_columns = detect_inconsistent_columns(df)
        report = generate_summary_report(df, missing_values, duplicate_rows, invalid_types, inconsistent_columns)
        save_report_to_csv(report, "data_quality_report.csv")
        print("Data quality report saved to data_quality_report.csv")

class TestDataQualityAnalyzer(unittest.TestCase):
    def test_load_csv(self):
        file_path = "test.csv"
        df = load_csv(file_path)
        self.assertIsNotNone(df)

    def test_detect_missing_values(self):
        df = pd.DataFrame({"A": [1, 2, np.nan]})
        missing_values = detect_missing_values(df)
        self.assertEqual(missing_values["A"], 1)

    def test_detect_duplicate_rows(self):
        df = pd.DataFrame({"A": [1, 2, 2]})
        duplicate_rows = detect_duplicate_rows(df)
        self.assertEqual(duplicate_rows, 1)

    def test_detect_invalid_data_types(self):
        df = pd.DataFrame({"A": [1, 2, "a"]})
        invalid_types = detect_invalid_data_types(df)
        self.assertEqual(invalid_types, 1)

    def test_detect_inconsistent_columns(self):
        df = pd.DataFrame({"A": [1, 2, 2]})
        inconsistent_columns = detect_inconsistent_columns(df)
        self.assertEqual(inconsistent_columns, 0)

    def test_generate_summary_report(self):
        df = pd.DataFrame({"A": [1, 2, np.nan]})
        missing_values = detect_missing_values(df)
        duplicate_rows = detect_duplicate_rows(df)
        invalid_types = detect_invalid_data_types(df)
        inconsistent_columns = detect_inconsistent_columns(df)
        report = generate_summary_report(df, missing_values, duplicate_rows, invalid_types, inconsistent_columns)
        self.assertIn("Missing Values", report)

if __name__ == "__main__":
    start_time = datetime.now()
    main()
    unittest.main(argv=[sys.argv[0]])
    end_time = datetime.now()
    print(f"Total execution time: {end_time - start_time}")