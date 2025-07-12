import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_obj
import pandas as pd

class PredictPipeline:
    def __init__(self) -> None:
        pass

    def predict(self, features):
        try:
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join('artifacts', 'model.pkl')

            preprocessor = load_obj(preprocessor_path)
            model = load_obj(model_path)

            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            return pred
        
        except Exception as e:
            logging.info('Error occured in predict function in prediction pipleine')
            raise CustomException(e,sys)
        

class CustomData:
    def __init__(self,Credit_Worthiness:object,
                 loan_amount:int,
                 term:int,
                 Neg_ammortization:object,
                 interest_only:object,
                 lump_sum_payment:float,
                 income:object,
                 credit_type:int,
                 Credit_Score:int):
        self.Credit_Worthiness=Credit_Worthiness
        self.loan_amount=loan_amount
        self.term=term
        self.Neg_ammortization=Neg_ammortization
        self.interest_only=interest_only
        self.lump_sum_payment=lump_sum_payment
        self.income=income
        self.credit_type=credit_type
        self.Credit_Score=Credit_Score

    
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Credit_Worthiness':[self.Credit_Worthiness],
                'loan_amount':[self.loan_amount],
                'term':[self.term],
                'Neg_ammortization':[self.Neg_ammortization],
                'interest_only':[self.interest_only],
                'lump_sum_payment':[self.lump_sum_payment],
                'income':[self.income],
                'credit_type':[self.credit_type],
                'Credit_Score':[self.Credit_Score]
                
            }

            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe created')
            return df
        
        except Exception as e:
            logging.info('Error occured in get data as dataframe function in prediction pipeline')
            raise CustomException(e,sys)