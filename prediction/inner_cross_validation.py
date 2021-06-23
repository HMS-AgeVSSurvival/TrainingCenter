import pandas as pd
import numpy as np
from hyperopt import tpe, fmin, rand, Trials


def cast_hyperparameters(hyperparameters):
    for hyperparameters_to_cast in ["num_leaves", "n_estimators", "min_child_samples", "subsample_freq"]:
        if hyperparameters_to_cast in hyperparameters.keys():
            hyperparameters[hyperparameters_to_cast] = int(hyperparameters[hyperparameters_to_cast])


def inner_cross_validation_age(data, algorithm, random_state, n_inner_search):
    from sklearn.metrics import r2_score

    from prediction.model import ModelAge
    from prediction.scale import scale_age
    from prediction import HYPERPARAMETERS_AGE, AGE_COLUMN

    model = ModelAge(algorithm, random_state)

    def cross_validation(hyperparameters):
        cast_hyperparameters(hyperparameters)
        print(hyperparameters)
        model.set(**hyperparameters)

        list_val_prediction = []

        for fold in data["fold"].drop_duplicates():
            train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
            val_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

            scaled_train_set, age_mean, age_std = scale_age(train_set)
            scaled_val_set, _, _ = scale_age(val_set)
            
            model.fit(scaled_train_set)
            val_prediction = model.predict(scaled_val_set) * age_std + age_mean

            list_val_prediction.append(val_prediction)

        every_val_prediction = pd.concat(list_val_prediction)
        val_r2 = r2_score(data.loc[every_val_prediction.index, AGE_COLUMN], every_val_prediction)

        return -val_r2

    best_hyperparameters = fmin(
        fn=cross_validation,
        space=HYPERPARAMETERS_AGE[algorithm],
        trials=Trials(),
        algo=tpe.suggest,  # this is for bayesian search, rand.suggest for random search
        max_evals=n_inner_search,
        rstate=np.random.RandomState(seed=random_state),
    )

    cast_hyperparameters(best_hyperparameters)
    return best_hyperparameters


def inner_cross_validation_survival(data, algorithm, random_state, n_inner_search):
    from sksurv.metrics import concordance_index_censored

    from prediction.model import ModelSurvival
    from prediction.scale import scale_survival
    from prediction import HYPERPARAMETERS_SURVIVAL, DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN

    model = ModelSurvival(algorithm, random_state)

    def cross_validation(hyperparameters):
        cast_hyperparameters(hyperparameters)
        print(hyperparameters)
        model.set(**hyperparameters)
        try:
            list_val_prediction = []

            for fold in data["fold"].drop_duplicates():
                train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
                val_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

                scaled_train_set = scale_survival(train_set)
                scaled_val_set = scale_survival(val_set)

                model.fit(scaled_train_set)
                val_prediction = model.predict(scaled_val_set)

                list_val_prediction.append(val_prediction)

            every_val_prediction = pd.concat(list_val_prediction)
            val_c_index = concordance_index_censored(data.loc[every_val_prediction.index, DEATH_COLUMN].astype(bool), data.loc[every_val_prediction.index, FOLLOW_UP_TIME_COLUMN], every_val_prediction)[0]
        
        except ArithmeticError:
            val_c_index = 0

        return -val_c_index

    best_hyperparameters = fmin(
        fn=cross_validation,
        space=HYPERPARAMETERS_SURVIVAL[algorithm],
        trials=Trials(),
        algo=tpe.suggest,  # this is for bayesian search, rand.suggest for random search
        max_evals=n_inner_search,
        rstate=np.random.RandomState(seed=random_state),
    )

    cast_hyperparameters(best_hyperparameters)
    return best_hyperparameters