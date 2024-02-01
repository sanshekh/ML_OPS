import os
from ml_ops import logger
import pandas as pd
from ml_ops.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config:DataValidationConfig):
        self.config = config

    def validate_all_columns(self)->bool : 
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            # all_schema = self.config.all_schema.keys()
            all_schema = self.config.all_schema

            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                    break # No need to continue checking if a column is missing in the schema
                else:
                    expected_dtype = all_schema[col]
                    actual_dtype = data[col].dtype
                    # print(f"Expected dtype is {expected_dtype} & Actual dtype is {actual_dtype}")

                    if expected_dtype != actual_dtype:
                        validation_status = False
                        with open(self.config.STATUS_FILE, 'w') as f:
                            f.write(f"Validation status: {validation_status}, "f"Column '{col}' has incorrect datatype. " f"Expected: {expected_dtype}, Actual: {actual_dtype}")
                        break  # No need to continue checking if a datatype is incorrect

                    else:
                        validation_status = True

                    
            if validation_status is None:
                validation_status = True  # If all columns are present and have correct datatypes

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

    
        except Exception as e:
            raise e 