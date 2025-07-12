import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_function

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    
    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation Initiated')
            #Define which columns should be ordinal encoded and which should be scaled
            categorical_cols = ['Credit_Worthiness','Neg_ammortization','interest_only','lump_sum_payment','credit_type']
            numerical_cols = ['loan_amount','term','income','Credit_Score']

            #Define the custom ranking for each ordinal variable
            credit_wor_categories = ['l1','l2']
            neg_ammor_categories = ['not_neg','neg_amm']
            interest_categories=['not_int','int_only']
            lump_sum_categories=['not_lpsm','lpsm']
            credit_type_categories=['EXP', 'EQUI', 'CRIF', 'CIB']
            

            logging.info('Pipeline Initiated')

            #Numerical pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='mean')),
    
                    ('scaler', StandardScaler())
                ]
            )

            #Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy="most_frequent")),
                    ('ordinalencoder', OrdinalEncoder(categories=[credit_wor_categories, neg_ammor_categories, interest_categories,
                                                                  lump_sum_categories,credit_type_categories])),
                    ('scaler', StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipeline', cat_pipeline, categorical_cols)
            ])

            logging.info('Pipeline Completed')
            return preprocessor


        except Exception as e:
            logging.info('Error in Data Transformation')
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):
        try:
            #Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head: \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head: \n{test_df.head().to_string()}')
            
            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'Status'
            drop_columns = [target_column_name, 'ID', 'year', 'loan_limit', 'Gender', 'approv_in_adv', 'loan_type',
              'loan_purpose',  'open_credit', 'business_or_commercial', 'rate_of_interest',
                       'Interest_rate_spread', 'Upfront_charges', 'property_value',
                   'construction_type', 'occupancy_type', 'Secured_by', 'total_units',
                       'co-applicant_credit_type',
                   'age', 'submission_of_application', 'LTV', 'Region', 'Security_Type',
                 'dtir1']

            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df = test_df[target_column_name]

            #Transforming using preprocessor obj
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info('Applying preprocessing object on training and testing datasets')

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_function(
                
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            logging.info('Preprocessor pickle file saved')

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        

        except Exception as e:
            logging.info('Exception occured in the Intitiate Data Transformation stage')
            raise CustomException(e,sys)