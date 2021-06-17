from hyperopt import hp
import numpy as np


HYPERPARAMETERS = {
    "elastic_net": {
        "alpha": hp.loguniform("alpha", np.log(1e-6), np.log(1e0)),
        "l1_ratio": hp.uniform("l1_ratio", 0, 1),
    },
    "forest": {
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

COLUMNS_TO_DROP = [
    "RIDAGEEX_extended",
    "mortstat",
    "follow_up_time",
    "survival_type_alive",
    "survival_type_cancer",
    "survival_type_cvd",
    "survival_type_other",
    "fold",
]
