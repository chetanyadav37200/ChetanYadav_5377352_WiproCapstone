import csv
from utils.logger import LogGen

logger = LogGen.loggen()


class CsvReader:
    @staticmethod
    def get_test_data(filepath, row_index):
        logger.info(f"Loading test data from CSV: {filepath} for row {row_index}")
        try:
            with open(filepath, mode='r', encoding='utf-8') as file:
                # DictReader automatically uses the first row as dictionary keys (headers)
                csv_reader = csv.DictReader(file)
                data_list = list(csv_reader)

                # Convert user-friendly row number (1, 2, 3) to Python index (0, 1, 2)
                actual_index = int(row_index) - 1

                if 0 <= actual_index < len(data_list):
                    data = data_list[actual_index]
                    logger.info(f"CSV Data successfully loaded: {data}")
                    return data
                else:
                    raise ValueError(f"Row index {row_index} out of bounds in CSV.")

        except Exception as e:
            logger.error(f"Failed to read CSV file: {str(e)}")
            raise