import argparse
import sys

import pandas as pd
import numpy as np


def feature_importances_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Pipeline to train and output the feature importances from the datasets"
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
        "-t",
        "--target",
        help="The target of the algorithm.",
        choices=["age", "all", "cvd", "cancer"],
        required=True,
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        help="The name of the algorithm.",
        choices=["elastic_net", "light_gbm"],
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
    parser.add_argument(
        "-sa", "--save_anyways", help="Save the feature importances anyways", action="store_true", default=False
    )
    args = parser.parse_args(argvs)
    print(args)

    if args.target == "age":
        feature_importances_age(
            args.main_category,
            args.category,
            args.algorithm,
            args.random_state,
            args.n_inner_search,
            args.save_anyways
        )
    else:
        feature_importances_survival(
            args.main_category,
            args.category,
            args.target,
            args.algorithm,
            args.random_state,
            args.n_inner_search,
            args.save_anyways
        )


def feature_importances_age(main_category, category, algorithm, random_state, n_inner_search, save_anyways):
    from sklearn.metrics import r2_score, mean_squared_error

    from prediction.model import ModelAge
    from prediction.scale import scale_age
    from prediction.inner_cross_validation import inner_cross_validation_age
    from feature_importances.update_results import update_results_age
    from prediction import AGE_COLUMN

    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")
    raw_data = data.copy()

    data.drop(columns=data.columns[data.columns.str.startswith("prediction")], inplace=True)
    data.drop(index=data.index[data.index.astype(str).str.startswith("feature_importances")], inplace=True)

    model = ModelAge(algorithm, random_state)

    train_set = data.sample(frac=1, random_state=0)

    hyperparameters = inner_cross_validation_age(
        train_set, algorithm, random_state, n_inner_search
    )

    model.set(**hyperparameters)

    scaled_train_set, age_mean, age_std = scale_age(train_set)

    model.fit(scaled_train_set)
    
    train_prediction = model.predict(scaled_train_set) * age_std + age_mean

    train_r2 = r2_score(
            train_set.loc[train_prediction.index, AGE_COLUMN], train_prediction
    )
    train_rmse = mean_squared_error(
            train_set.loc[train_prediction.index, AGE_COLUMN],
            train_prediction,
            squared=False,
    ).astype(np.float64)

    metrics = {"train r²": train_r2, "train RMSE": train_rmse}

    results_updated = update_results_age(main_category, category, algorithm, metrics)

    if save_anyways or results_updated:
        index_feature_importances = f"feature_importances_age_{algorithm}_{random_state}"
        feature_importances = model.get_feature_importances(scaled_train_set.columns)
        feature_importances.index = [index_feature_importances]

        if index_feature_importances in raw_data.index:
            raw_data.loc[index_feature_importances] = feature_importances.loc[index_feature_importances]
        else:
            raw_data = raw_data.append(feature_importances)
            raw_data.index.name = "SEQN"
            raw_data.index = raw_data.index.astype(str, copy=False)
        
        raw_data.reset_index().to_feather(f"data/{main_category}/{category}.feather")


def feature_importances_survival(main_category, category, target, algorithm, random_state, n_inner_search, save_anyways):
    from sksurv.metrics import concordance_index_censored

    from prediction.model import ModelSurvival
    from prediction.scale import scale_survival
    from prediction.inner_cross_validation import inner_cross_validation_survival
    from feature_importances.update_results import update_results_survival
    from prediction import DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN


    def any_fold_all_cencored(data):
        for idx_fold in data["fold"].drop_duplicates():
            if (data.loc[data["fold"] == idx_fold, DEATH_COLUMN] == 1.0).sum() == 0:
                return True
        return False


    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")
    raw_data = data.copy()

    data.drop(columns=data.columns[data.columns.str.startswith("prediction")], inplace=True)
    data.drop(index=data.index[data.index.astype(str).str.startswith("feature_importances")], inplace=True)

    model = ModelSurvival(algorithm, random_state)

    if target == "all":
        data.drop(index=data.index[data["survival_type_alive"].isna()], inplace=True)
    elif target == "cvd":
        data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cvd"] == 1)]
    elif target == "cancer":
        data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cancer"] == 1)]

    if (not data.empty) and (not any_fold_all_cencored(data)):
        train_set = data.sample(frac=1, random_state=0)

        hyperparameters = inner_cross_validation_survival(
            train_set, algorithm, random_state, n_inner_search
        )

        model.set(**hyperparameters)

        scaled_train_set = scale_survival(train_set)

        model.fit(scaled_train_set)

        train_prediction = model.predict(scaled_train_set)

        train_c_index = concordance_index_censored(train_set.loc[train_prediction.index, DEATH_COLUMN].astype(bool), train_set.loc[train_prediction.index, FOLLOW_UP_TIME_COLUMN], train_prediction)[0]
             
        metrics = {"train C-index": train_c_index}
    else:
        metrics = {"train C-index": -1}

    results_updated = update_results_survival(main_category, category, algorithm, target, metrics)
    
    if metrics["train C-index"] != -1 and (save_anyways or results_updated):
        index_feature_importances = f"feature_importances_{target}_{algorithm}_{random_state}"
        feature_importances = model.get_feature_importances(scaled_train_set.columns)
        feature_importances.index = [index_feature_importances]

        if index_feature_importances in raw_data.index:
            raw_data.loc[index_feature_importances] = feature_importances.loc[index_feature_importances]
        else:
            raw_data = raw_data.append(feature_importances)
            raw_data.index.name = "SEQN"
            raw_data.index = raw_data.index.astype(str, copy=False)
        
        raw_data.reset_index().to_feather(f"data/{main_category}/{category}.feather")