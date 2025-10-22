import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME

class MySQLClient:
    """
    Class Name :   MySQLClient
    Description :  This class handles connection to the MySQL database and
                   provides a reusable SQLAlchemy engine for data operations.

    Output      :  Connection to MySQL database
    On Failure  :  Raises USvisaException
    """
    client = None

    def __init__(self, database_name: str = DATABASE_NAME,
                 username: str = "root",
                 password: str = "",
                 host: str = "localhost",
                 port: int = 3306) -> None:
        """
        Initialize the MySQL client with connection parameters.
        Args:
            database_name (str): MySQL database name
            username (str): MySQL username (default: root)
            password (str): MySQL password (default: empty)
            host (str): Database host (default: localhost)
            port (int): MySQL port (default: 3306)
        """
        try:
            if MySQLClient.client is None:
                connection_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}"
                MySQLClient.client = create_engine(connection_url)
                logging.info(f"MySQL connection established to database: {database_name}")

            self.client: Engine = MySQLClient.client
            self.database_name = database_name
        except Exception as e:
            raise USvisaException(e, sys)

    def get_engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine instance for database operations.
        """
        try:
            return self.client
        except Exception as e:
            raise USvisaException(e, sys)

    def test_connection(self) -> bool:
        """
        Tests the connection to the MySQL database.
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            with self.client.connect() as connection:
                connection.execute("SELECT 1")
                logging.info("MySQL connection test successful.")
            return True
        except Exception as e:
            logging.error(f" MySQL connection test failed: {e}")
            raise USvisaException(e, sys)
