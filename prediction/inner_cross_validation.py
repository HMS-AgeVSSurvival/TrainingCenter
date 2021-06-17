import pandas as pd
import numpy as np
from hyperopt import tpe, fmin, rand, Trials

from prediction import HYPERPARAMETERS


def cast_hyperparameters(hyperparameters):
    for hyperparameters_to_cast in ["num_leaves", "n_estimators", "min_child_samples"]:
        if hyperparameters_to_cast in hyperparameters.keys():
            hyperparameters[hyperparameters_to_cast] = int(hyperparameters[hyperparameters_to_cast])


def inner_cross_validation(data, algorithm, n_inner_search, random_state):
    def cross_validation(hyperparameters):
        cast_hyperparameters(hyperparameters)
        model.set(random_state, **hyperparameters)

        list_val_predictions = []

        for fold in data["fold"].drop_duplicates():
            train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
            val_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

            model.set(hyperparameters, random_state)
            model.fit(train_set)

            list_val_predictions.append(model.predict(val_set))

        return -model.score(pd.concat(list_val_predictions))

    best_params = fmin(
        fn=cross_validation,
        space=HYPERPARAMETERS[algorithm],
        trials=Trials(),
        algo=tpe.suggest,  # this is for bayesian search, rand.suggest for random search
        max_evals=n_inner_search,
        rstate=np.random.RandomState(seed=random_state),
    )

    cast_hyperparameters(best_params)
    return best_params