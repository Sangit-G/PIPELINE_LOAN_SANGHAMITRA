import os
import sys 
from src.logger import logging
from src.exception import CustomException
from src.utils import ConnectDB
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Step 1: Create path variables to store the files as raw csv
@dataclass
class DataIngestionconfig:
    train_data_path:str = os.path.join('artifacts', 'train.csv')
    test_data_path:str = os.path.join('artifacts', 'test.csv')
    raw_data_path:str = os.path.join('artifacts', 'raw.csv')


# Create a class for Data Ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()

    
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion method started')
        try:
            connect_db = ConnectDB()
            connect_db.retrieve_data()
            df = pd.read_csv(os.path.join('DATA','Loan_Default.csv'))
            logging.info('Dataset read as pandas dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info('Train Test split')
            train_set, test_set = train_test_split(df, test_size=0.3, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of data is complete')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        

        except Exception as e:
            logging.info('Exception occured at Data Ingestion Stage')
            raise CustomException(e,sys)