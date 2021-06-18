import argparse
import sys

import pandas as pd
import numpy as np


def prediction_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Pipeline to train and output the predictions for the datasets"
    )
    parser.add_argument(
        "-mc",
        "--main_category",
        help="Name of the main category.",
        choices=["examination", "laboratory", "questionnaire"],
        required=True,
    )
    parser.add_argument("-c", "--category", help="Name of the category.", required=True)
    parser.add_argument(
        "-a",
        "--algorithm",
        help="The name of the algorithm.",
        choices=["elastic_net", "light_gbm"],
        required=True,
    )
    parser.add_argument(
        "-t",
        "--target",
        help="The target of the algorithm.",
        choices=["age", "all", "cvd", "cancer"],
        required=True,
    )
    parser.add_argument(
        "-rs",
        "--random_state",
        type=int,
        help="Random state during the training.",
        choices=[1, 2],
        required=True,
    )
    parser.add_argument(
        "-nis",
        "--n_inner_search",
        default=1,
        type=int,
        help="The number of evaluation in the hyperparameters space",
    )

    args = parser.parse_args(argvs)
    print(args)

    if args.target == "age":
        prediction_age(
            args.main_category,
            args.category,
            args.algorithm,
            args.random_state,
            args.n_inner_search,
        )
    else:
        prediction_survival(
            args.main_category,
            args.category,
            args.algorithm,
            args.target,
            args.random_state,
            args.n_inner_search,
        )


def prediction_age(main_category, category, algorithm, random_state, n_inner_search):
    from sklearn.metrics import r2_score, mean_squared_error

    from prediction.model import ModelAge
    from prediction.scale import scale_age
    from prediction.inner_cross_validation import inner_cross_validation_age
    from prediction.utils import update_results_age
    from prediction import AGE_COLUMN

    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")

    list_train_r2 = []
    list_train_rmse = []
    list_test_prediction = []

    model = ModelAge(algorithm, random_state)

    for fold in data["fold"].drop_duplicates():
        train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
        test_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

        hyperparameters = inner_cross_validation_age(
            train_set, algorithm, random_state, n_inner_search
        )

        model.set(**hyperparameters)

        scaled_train_set, age_mean, age_std = scale_age(train_set)
        scaled_test_set, _, _ = scale_age(test_set)

        model.fit(scaled_train_set)
        
        train_prediction = model.predict(scaled_train_set) * age_std + age_mean
        test_prediction = model.predict(scaled_test_set) * age_std + age_mean

        list_train_r2.append(
            r2_score(
                train_set.loc[train_prediction.index, AGE_COLUMN], train_prediction
            )
        )
        list_train_rmse.append(
            mean_squared_error(
                train_set.loc[train_prediction.index, AGE_COLUMN],
                train_prediction,
                squared=False,
            )
        )
        list_test_prediction.append(test_prediction)
    
    train_r2, train_r2_std = (
        pd.Series(list_train_r2).mean(),
        pd.Series(list_train_r2).std(),
    )
    train_rmse, train_rmse_std = (
        pd.Series(list_train_rmse).mean(),
        pd.Series(list_train_rmse).std(),
    )

    every_test_prediction = pd.concat(list_test_prediction)
    test_r2 = r2_score(
        data.loc[every_test_prediction.index, AGE_COLUMN], every_test_prediction
    )
    test_rmse = mean_squared_error(
        data.loc[every_test_prediction.index, AGE_COLUMN],
        every_test_prediction,
        squared=False,
    ).astype(np.float64)

    metrics = {
        "train r²": train_r2,
        "train r² std": train_r2_std,
        "train RMSE": train_rmse,
        "train RMSE std": train_rmse_std,
        "test r²": test_r2,
        "test RMSE": test_rmse,
    }

    update_results_age(main_category, category, algorithm, metrics)


def prediction_survival(main_category, category, algorithm, target, random_state, n_inner_search):
    from sksurv.metrics import concordance_index_censored

    from prediction.model import ModelSurvival
    from prediction.scale import scale_survival
    from prediction.inner_cross_validation import inner_cross_validation_survival
    from prediction.utils import update_results_survival
    from prediction import DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN

    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")

    list_train_c_index = []
    list_test_prediction = []

    model = ModelSurvival(algorithm, random_state)

    if target == "all":
        data.drop(index=data.index[data["survival_type_alive"].isna()], inplace=True)
    elif target == "cvd":
        data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cvd"] == 1)]
    elif target == "cancer":
        data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cancer"] == 1)]


    for fold in data["fold"].drop_duplicates():
        train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
        test_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

        hyperparameters = inner_cross_validation_survival(
            train_set, algorithm, random_state, n_inner_search
        )

        model.set(**hyperparameters)

        scaled_train_set = scale_survival(train_set)
        scaled_test_set = scale_survival(test_set)

        model.fit(scaled_train_set)

        train_prediction = model.predict(scaled_train_set)
        test_prediction = model.predict(scaled_test_set)

        list_train_c_index.append(
            concordance_index_censored(train_set.loc[train_prediction.index, DEATH_COLUMN].astype(bool), train_set.loc[train_prediction.index, FOLLOW_UP_TIME_COLUMN], train_prediction)[0]
        )
        list_test_prediction.append(test_prediction)
    
    train_c_index, train_c_index_std = (
        pd.Series(list_train_c_index).mean(),
        pd.Series(list_train_c_index).std(),
    )
    every_test_prediction = pd.concat(list_test_prediction)
    test_c_index = concordance_index_censored(data.loc[every_test_prediction.index, DEATH_COLUMN].astype(bool), data.loc[every_test_prediction.index, FOLLOW_UP_TIME_COLUMN], every_test_prediction)[0]

    metrics = {
        "train C-index": train_c_index,
        "train C-index std": train_c_index_std,
        "test C-index": test_c_index,
    }

    update_results_survival(main_category, category, algorithm, target, metrics)