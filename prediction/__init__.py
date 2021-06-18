from hyperopt import hp
import numpy as np


HYPERPARAMETERS_AGE = {
    "elastic_net": {
        "alpha": hp.loguniform("alpha", np.log(1e-6), np.log(2e1)),
        "l1_ratio": hp.uniform("l1_ratio", 0, 1),
    },
    "light_gbm": {
        "num_leaves": hp.uniform("num_leaves", low=10, high=200),
        "learning_rate": hp.loguniform(
            "learning_rate", low=np.log(1e-4), high=np.log(1e-1)
        ),
        "n_estimators": hp.uniform("n_estimators", low=80, high=400),
        "min_child_samples": hp.uniform("min_child_samples", low=5, high=30),
        "subsample": hp.uniform("subsample", low=0.2, high=1),
        "colsample_bytree": hp.uniform("colsample_bytree", low=0.2, high=1),
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
            "alpha": hp.loguniform("alpha", np.log(1e-1), np.log(1e0)),
            "l1_ratio": hp.uniform("l1_ratio", low=0.00001, high=0.1),
        },
        "forest": {
            "max_leaf_nodes": hp.uniform("max_leaf_nodes", low=20, high=200),
            "learning_rate": hp.loguniform("learning_rate", low=np.log(1e-4), high=np.log(1e-1)),
            "n_estimators": hp.uniform("n_estimators", low=80, high=250),
            "min_samples_leaf": hp.uniform("min_samples_leaf", low=5, high=30),
            "subsample": hp.uniform("subsample", low=0.2, high=1),
        },
}


COLUMNS_TO_DROP_FOR_SCALE = [
    "mortstat",
    "follow_up_time",
    "survival_type_alive",
    "survival_type_cancer",
    "survival_type_cvd",
    "survival_type_other",
    "fold",
]
COLUMNS_TO_ADD_AFTER_SCALE = ["mortstat", "follow_up_time"]

AGE_COLUMN = "RIDAGEEX_extended; Best age in months at date of examination for individuals under 85 years of age at screening."
DEATH_COLUMN = "mortstat"
FOLLOW_UP_TIME_COLUMN = "follow_up_time"