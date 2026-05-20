import csv
import os


class CSVReader:

    @staticmethod
    def read_csv(file_name):
        data = []
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "data", file_name)

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

        return data