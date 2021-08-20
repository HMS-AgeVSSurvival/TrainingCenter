import numpy as np

from utils.google_sheets_sdk import find_cell, find_all_cells, get_cell, update_cell


METRICS_COL_ORDER_AGE = {"elastic_net": 2, "light_gbm": 3}
N_HYPERPARAMETERS_COL_ORDER_AGE = {"elastic_net": 14, "light_gbm": 15}

METRICS_COL_ORDER_SURVIVAL = {"all": {"elastic_net": 12, "light_gbm": 13}, "cvd": {"elastic_net": 14, "light_gbm": 15}, "cancer": {"elastic_net": 16, "light_gbm": 17}}
N_HYPERPARAMETERS_COL_ORDER_SURVIVAL = {"all": {"elastic_net": 16, "light_gbm": 17}, "cvd": {"elastic_net": 18, "light_gbm": 19}, "cancer": {"elastic_net": 20, "light_gbm": 21}}


class UpdateResultsAge:
    def __init__(self):

        self.category_row = None
        self.train_r2_column = None

    def check_better_training(self, main_category, category, algorithm, metrics, random_state):
        self.category_row = find_cell(main_category + f" {random_state}", category).row
        self.train_r2_column = find_all_cells(main_category + f" {random_state}", "train r²")[METRICS_COL_ORDER_AGE[algorithm]].col

        previous_train_r2 = get_cell(main_category + f" {random_state}", self.category_row, self.train_r2_column).value
        
        print("Previous train score:", previous_train_r2)
        print("New train score:", metrics["train r²"])

        return previous_train_r2 is None or float(previous_train_r2) <= metrics["train r²"]

    def update_results(self, main_category, algorithm, metrics, random_state, n_inner_search):
        print(metrics)

        metric_column = find_all_cells(main_category + f" {random_state}", "N hyperparameters")[N_HYPERPARAMETERS_COL_ORDER_AGE[algorithm]].col
        update_cell(main_category + f" {random_state}", self.category_row, metric_column, n_inner_search)

        for metric_name in list(metrics.keys()):
            if metric_name == "train r²":
                continue
            metric_column = find_all_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_AGE[algorithm]].col
            update_cell(main_category + f" {random_state}", self.category_row, metric_column, np.round(metrics[metric_name], 3))
        
        update_cell(main_category + f" {random_state}", self.category_row, self.train_r2_column, np.round(metrics["train r²"], 3))



class UpdateResultsSurvival:
    def __init__(self):
        self.category_row = None
        self.train_c_index_column = None

    def check_better_training(self, main_category, category, algorithm, target, metrics, random_state):
        self.category_row = find_cell(main_category + f" {random_state}", category).row
        self.train_c_index_column = find_all_cells(main_category + f" {random_state}", "train C-index")[METRICS_COL_ORDER_SURVIVAL[target][algorithm]].col

        previous_train_c_index = get_cell(main_category + f" {random_state}", self.category_row, self.train_c_index_column).value
        
        print("Previous train score:", previous_train_c_index)
        print("New train score:", metrics["train C-index"])

        return previous_train_c_index is None or float(previous_train_c_index) <= metrics["train C-index"]

    def update_results(self, main_category, algorithm, target, metrics, random_state, n_inner_search):
        print(metrics)

        metric_column = find_all_cells(main_category + f" {random_state}", "N hyperparameters")[N_HYPERPARAMETERS_COL_ORDER_SURVIVAL[target][algorithm]].col
        update_cell(main_category + f" {random_state}", self.category_row, metric_column, n_inner_search)

        for metric_name in list(metrics.keys()):
            if metric_name == "train C-index":
                continue
            metric_column = find_all_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_SURVIVAL[target][algorithm]].col
            update_cell(main_category + f" {random_state}", self.category_row, metric_column, np.round(metrics[metric_name], 3))
        
        update_cell(main_category + f" {random_state}", self.category_row, self.train_c_index_column, np.round(metrics["train C-index"], 3))