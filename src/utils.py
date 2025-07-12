import os
import sys
import pickle
from sqlalchemy import create_engine
from dataclasses import dataclass
import pandas as pd
from src.exception import CustomException
from sklearn.metrics import classification_report
from src.logger import logging
from urllib.parse import quote_plus
from sqlalchemy import create_engine

@dataclass
class ConnectDBConfig():
    host = 'localhost'
    user = 'root'
    password = 'Sanghasql23@'
    database = 'loan_pipeline'
    table_name = 'loan_default'
    dataset_path:str = os.path.join('DATA',' Loan_Default.csv')

class ConnectDB():
    def __init__(self):
        self.connect_db_config = ConnectDBConfig()
#print(f"Connecting with URL: mysql+mysqlconnector://{self.connect_db_config.user}:{self.connect_db_config.password}@{self.connect_db_config.host}/{self.connect_db_config.database}")
    
    from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pandas as pd
import os

class ConnectDB:
    def __init__(self):
        self.connect_db_config = ConnectDBConfig()

    def retrieve_data(self):
        try:
            # Sanitize credentials
            user = self.connect_db_config.user.strip()
            password = quote_plus(self.connect_db_config.password.strip())
            host = self.connect_db_config.host.strip().lstrip('@')  # Remove accidental '@'
            database = self.connect_db_config.database.strip()

            # Build the safe connection string
            connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            print(f"Using connection string: {connection_string}")  # Optional debug line

            # Create the SQLAlchemy engine
            engine = create_engine(connection_string)

            # Fetch data and save to CSV
            query = "SELECT * FROM loan_default"
            df = pd.read_sql(query, con=engine)
            os.makedirs("DATA", exist_ok=True)
            df.to_csv(os.path.join("DATA", "Loan_Default.csv"), index=False)

        except Exception as e:
            raise CustomException(e, sys)



def save_function(file_path, obj):
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as file_obj:
        pickle.dump(obj, file_obj)


def model_performance(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            test_model_score = classification_report(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score
        
        return report
    
    except Exception as e:
        raise CustomException(e,sys)
    


def load_obj(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
        
    except Exception as e:
        logging.info('Error in load_object function in utils')
        raise CustomException(e,sys)