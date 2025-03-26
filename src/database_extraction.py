import os
import csv
import pyodbc
import sys
from config.db_config import DB_CONFIG
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class MSSQLDataExtractor:
    def __init__(self, db_config):
        self.server = db_config.get("server")
        self.database = db_config.get("database")
        self.username = db_config.get("username")
        self.password = db_config.get("password")
        self.table_name = db_config.get("table_name")
        self.connection = None

        logger.info("✅ Database configuration has been set up.")

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};"
                f"UID={self.username};PWD={self.password}"
            )
            logger.info("✅ Successfully connected to the database.")
        except Exception as e:
            raise CustomException(f"❌ Error while connecting to the database: {e}", sys)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("✅ Disconnected from the database.")

    def extract_to_csv(self, output_folder="./artifacts/raw"):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)

            rows = cursor.fetchall()
            if not rows:
                logger.warning("⚠️ No data found in the table.")
                return
            
            columns = [column[0] for column in cursor.description]
            logger.info(f"✅ Data fetched successfully! Rows: {len(rows)}")

            os.makedirs(output_folder, exist_ok=True)
            csv_file_path = os.path.join(output_folder, "data.csv")

            with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(rows)

            logger.info(f"✅ Data successfully saved to {csv_file_path}")

        except Exception as e:
            raise CustomException(f"❌ Error extracting data from DB: {e}", sys)

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            self.disconnect()

if __name__ == "__main__":
    try:
        extractor = MSSQLDataExtractor(DB_CONFIG)
        extractor.extract_to_csv()
    except CustomException as ce:
        logger.error(str(ce))
