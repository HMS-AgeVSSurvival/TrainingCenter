import argparse
import sys

import pandas as pd
from prediction.inner_cross_validation import inner_cross_validation
from sklearn.metrics import r2_score, mean_squared_error

from prediction.model import Model
from prediction.scale import scale
from prediction import AGE_COLUMN


def prediction_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Pipeline to train and output the predictions for the datasets")
    parser.add_argument("-mc", "--main_category", help="Name of the main category.", choices=["examination", "laboratory", "questionnaire"], required=True)
    parser.add_argument("-c", "--category", help="Name of the category.", required=True)
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

    args = parser.parse_args(argvs)
    print(args)

    prediction(args.main_category, args.category, args.algorithm, args.random_state, args.n_inner_search)


def prediction(main_category, category, algorithm, random_state, n_inner_search):
    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")

    list_train_r2 = []
    list_train_rmse = []
    list_test_prediction = []

    model = Model(algorithm, random_state)

    for fold in data["fold"].drop_duplicates():
        train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
        test_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

        hyperparameters = inner_cross_validation(train_set, algorithm, random_state, n_inner_search)

        model.set(**hyperparameters)

        scaled_train_set, age_mean, age_std = scale(train_set)
        scaled_test_set, _, _ = scale(test_set)

        model.fit(scaled_train_set)
        train_prediction = model.predict(scaled_train_set) * age_std + age_mean
        test_prediction = model.predict(scaled_test_set) * age_std + age_mean

        list_train_r2.append(r2_score(train_set.loc[train_prediction.index, AGE_COLUMN], train_prediction))
        list_train_rmse.append(mean_squared_error(train_set.loc[train_prediction.index, AGE_COLUMN], train_prediction, squared=False))
        list_test_prediction.append(test_prediction)

    train_r2, train_r2_std = pd.Series(list_train_r2).mean() , pd.Series(list_train_r2).std()
    train_rmse, train_rmse_std = pd.Series(list_train_rmse).mean() , pd.Series(list_train_rmse).std()
    
    every_test_prediction = pd.concat(list_test_prediction)
    test_r2 = r2_score(data.loc[every_test_prediction.index, AGE_COLUMN], every_test_prediction)
    test_rmse = mean_squared_error(data.loc[every_test_prediction.index, AGE_COLUMN], every_test_prediction, squared=False)
    
    # update_google_sheet(main_category, category, algorithm, train_r2, train_r2_std, train_rmse, train_rmse_std, test_r2, test_rmse, n_inner_search, random_state)

    print("train_r2:", train_r2, "train_r2_std:", train_r2_std)
    print("train_rmse:", train_rmse, "train_rmse_std:", train_rmse_std)
    print("test_r2:", test_r2)
    print("test_rmse:", test_rmse)