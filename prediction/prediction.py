import pandas as pd
from prediction.inner_cross_validation import inner_cross_validation


def prediction(main_category, category, algorithm, n_inner_search, random_state):
    data = pd.read_feather(f"data/{main_category}/{category}.feather")

    list_train_scores = []
    list_test_predictions = []

    for fold in data["fold"].drop_duplicates():
        train_set = data[data["fold"] != fold].sample(frac=1, random_state=0)
        test_set = data[data["fold"] == fold].sample(frac=1, random_state=0)

        hyperparameters = inner_cross_validation(train_set, algorithm, n_inner_search, random_state)

        model.set(random_state, hyperparameters)

        model.fit(train_set)
        list_train_scores.append(model.score(model.predict(train_set)))
        list_test_predictions.append(model.predict(test_set))

    train_score, train_score_std = pd.Index(list_train_scores).mean() , pd.Index(list_train_scores).std()
    test_score = model.score(pd.concat(list_test_predictions))
    
    update_google_sheet(main_category, category, algorithm, n_inner_search, random_state, train_score, train_score_std, test_score)