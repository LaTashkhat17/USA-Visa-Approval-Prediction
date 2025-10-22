import sys
import pandas as pd
import numpy as np
from typing import Optional
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.configuration.db_connection import MySQLClient
from us_visa.constants import DATABASE_NAME


class USvisaData:
    """
    This class helps export a MySQL table as a pandas DataFrame.
    """

    def __init__(self, database_name: str = DATABASE_NAME):
        """
        Initializes a MySQL client connection.
        """
        try:
            self.mysql_client = MySQLClient(database_name=database_name)
            self.engine = self.mysql_client.get_engine()
            self.database_name = database_name
            logging.info(f"MySQL connection established for database: {self.database_name}")
        except Exception as e:
            raise USvisaException(e, sys)

    def export_table_as_dataframe(self, table_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports the entire MySQL table as a pandas DataFrame.
        Args:
            table_name (str): The table name to export.
            database_name (Optional[str]): Optional override for database name.
        Returns:
            pd.DataFrame: The table data as a pandas DataFrame.
        """
        try:
            db_to_use = database_name if database_name else self.database_name
            query = f"SELECT * FROM {db_to_use}.{table_name};"

            logging.info(f"Executing query: {query}")
            df = pd.read_sql(query, con=self.engine)

            # Optional data cleaning similar to MongoDB version
            df.replace({"na": np.nan, "NaN": np.nan, "None": np.nan}, inplace=True)

            logging.info(f"Data successfully exported from table '{table_name}' "
                         f"with {df.shape[0]} rows and {df.shape[1]} columns.")
            return df

        except Exception as e:
            logging.error(f" Error while exporting table '{table_name}' from MySQL: {e}")
            raise USvisaException(e, sys)
