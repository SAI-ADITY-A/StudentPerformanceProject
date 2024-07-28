import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

print("Current Working Directory:", os.getcwd())

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationCOnfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationCOnfig()
    
    def get_data_transformer_object(self):
        try:
            numerical_features = ['writing_score', 'reading_score']
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical columns Standard Scaling is completed.")

            categorical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info("Categorical columns Encoding is completed.")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", numerical_pipeline, numerical_features),
                    ("cat_pipeline", categorical_pipeline, categorical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test dataset is complete.")
            logging.info("Obtaining Preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_feature = 'math_score'
            numerical_features = ['writing_score', 'reading_score']
            
            input_feature_train = train_df.drop(columns=[target_feature], axis = 1)
            target_feature_train = train_df[target_feature]

            input_feature_test = test_df.drop(columns=[target_feature], axis = 1)
            target_feature_test = test_df[target_feature]

            logging.info("Applying preprocessing object on test and training dataframe.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test)]

            logging.info("Saving preprocessing object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)
    
