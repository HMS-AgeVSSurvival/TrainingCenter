from hyperopt import hp
import numpy as np


HYPERPARAMETERS_AGE = {
    "elastic_net": {
        "alpha": hp.loguniform("alpha", np.log(1e-6), np.log(2e1)),
        "l1_ratio": hp.uniform("l1_ratio", 0, 1),
    },
    "light_gbm": {
        "num_leaves": hp.uniform("num_leaves", low=10, high=1000),
        "learning_rate": hp.loguniform(
            "learning_rate", low=np.log(1e-4), high=np.log(1e-1)
        ),
        "n_estimators": hp.uniform("n_estimators", low=80, high=400),
        "min_child_samples": hp.uniform("min_child_samples", low=1, high=30),
        "subsample": hp.uniform("subsample", low=0.1, high=1),
        "subsample_freq": hp.uniform("subsample_freq", low=1, high=80),
        "colsample_bytree": hp.uniform("colsample_bytree", low=0.1, high=1),
        "reg_alpha": hp.loguniform(
            "reg_alpha", np.log(1e-6), np.log(1e0)
        ),  # L1 regularization
        "reg_lambda": hp.loguniform(
            "reg_lambda", np.log(1e-6), np.log(1e0)
        ),  # L2 regularization
    },
}
HYPERPARAMETERS_SURVIVAL = {
        "elastic_net": {
            "alpha": hp.loguniform("alpha", np.log(1e-3), np.log(5e-1)),
            "l1_ratio": hp.uniform("l1_ratio", low=0, high=1),
        },
        "light_gbm": {
            "max_leaf_nodes": hp.uniform("max_leaf_nodes", low=20, high=1000),
            "learning_rate": hp.loguniform("learning_rate", low=np.log(1e-4), high=np.log(5e-1)),
            "n_estimators": hp.uniform("n_estimators", low=80, high=250),
            "min_samples_leaf": hp.uniform("min_samples_leaf", low=1, high=30),
            "subsample": hp.uniform("subsample", low=0.1, high=1),
        },
}

AGE_COLUMN = "RIDAGEEX_extended; Best age in months at date of examination for individuals under 85 years of age at screening."
GENDER_COLUMN = 'RIAGENDR; Gender of the sample person'
DEATH_COLUMN = "mortstat"
FOLLOW_UP_TIME_COLUMN = "follow_up_time"
ETHNICITIES = ['RIDRETH1_Non-Hispanic Black; Recode of reported race and ethnicity information.', 'RIDRETH1_Non-Hispanic White; Recode of reported race and ethnicity information.', 'RIDRETH1_Other Hispanic; Recode of reported race and ethnicity information.', 'RIDRETH1_Other Race - Including Multi-Racial; Recode of reported race and ethnicity information.']
SURVIVAL_TYPES = ['survival_type_alive', 'survival_type_cancer', 'survival_type_cvd', 'survival_type_other']

BASIC_TRAINING_COLUMNS = [AGE_COLUMN, GENDER_COLUMN, DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN, 'fold'] + ETHNICITIES + SURVIVAL_TYPES


COLUMNS_TO_DROP_FOR_SCALE = [
    DEATH_COLUMN,
    FOLLOW_UP_TIME_COLUMN,
    "fold",
] + SURVIVAL_TYPES
COLUMNS_TO_ADD_AFTER_SCALE = [DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN]

COLOR_ALGORITHM = {"elastic_net":{"red": 0.5, "green": 0.5, "blue": 1.0}, "light_gbm":{"red": 0.5, "green": 1.0, "blue": 0.5}}
