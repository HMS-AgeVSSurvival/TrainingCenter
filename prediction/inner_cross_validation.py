import pandas as pd
import numpy as np
from hyperopt import tpe, fmin, rand, Trials
from sklearn.metrics import r2_score

from prediction.model import Model
from prediction.scale import scale
from prediction import HYPERPARAMETERS, AGE_COLUMN


def cast_hyperparameters(hyperparameters):
    for hyperparameters_to_cast in ["num_leaves", "n_estimators", "min_child_samples"]:
        if hyperparameters_to_cast in hyperparameters.keys():
            hyperparameters[hyperparameters_to_cast] = int(hyperparameters[hyperparameters_to_cast])


def inner_cross_validation(data, algorithm, random_state, n_inner_search):
    model = Model(algorithm, random_state)

    def cross_validation(hyperparameters):
        cast_hyperparameters(hyperparameters)
        model.set(**hyperparameters)

        list_val_prediction = []

        for fold in data["fold"].drop_duplicates():
            train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
            val_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

            scaled_train_set, age_mean, age_std = scale(train_set)
            scaled_val_set, _, _ = scale(val_set)

            model.fit(scaled_train_set)
            val_prediction = model.predict(scaled_val_set) * age_std + age_mean

            list_val_prediction.append(val_prediction)

        every_val_prediction = pd.concat(list_val_prediction)
        val_r2 = r2_score(data.loc[every_val_prediction.index, AGE_COLUMN], every_val_prediction)

        return -val_r2

    best_hyperparameters = fmin(
        fn=cross_validation,
        space=HYPERPARAMETERS[algorithm],
        trials=Trials(),
        algo=tpe.suggest,  # this is for bayesian search, rand.suggest for random search
        max_evals=n_inner_search,
        rstate=np.random.RandomState(seed=random_state),
    )

    cast_hyperparameters(best_hyperparameters)
    return best_hyperparameters