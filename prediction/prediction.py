import pandas as pd
import numpy as np

def prediction(main_category, category, algorithm, n_inner_cross_validation_search):
    data = pd.read_feather(f"data/{main_category}/{category}.feather")

    n_folds = int(data["fold"].max()) + 1
    list_train_scores = []
    list_test_predictions = []

    for fold in range(n_folds):
        train_set = data[data["fold"] != fold]
        test_set = data[data["fold"] == fold]

        hyperparameters = inner_cross_validation(train_set, algorithm, n_inner_cross_validation_search)

        model.set(hyperparameters)

        model.fit(train_set)
        list_train_scores.append(model.score(train_set))
        list_test_predictions.append(model.predict(test_set))

    train_score, train_score_std = list_train_scores.mean() , list_train_scores.std()
    test_score = model.score(pd.concat(list_test_prediction))
    update_google_sheet(main_category, category, algorithm, )