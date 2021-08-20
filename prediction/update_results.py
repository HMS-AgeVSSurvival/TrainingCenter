import numpy as np

from utils.google_sheets_sdk import find_cell, find_all_cells, get_cell, update_cell


METRICS_COL_ORDER_AGE = {"elastic_net": 0, "light_gbm": 1}
N_HYPERPARAMETERS_COL_ORDER_AGE = {"elastic_net": 0, "light_gbm": 1}

METRICS_COL_ORDER_SURVIVAL = {"full_training": {"all": {"elastic_net": 0, "light_gbm": 1}, "cvd": {"elastic_net": 2, "light_gbm": 3}, "cancer": {"elastic_net": 4, "light_gbm": 5}}, "basic_training": {"all": {"elastic_net": 6, "light_gbm": 7}, "cvd": {"elastic_net": 8, "light_gbm": 9}, "cancer": {"elastic_net": 10, "light_gbm": 11}}}
N_HYPERPARAMETERS_COL_ORDER_SURVIVAL = {"full_training": {"all": {"elastic_net": 2, "light_gbm": 3}, "cvd": {"elastic_net": 4, "light_gbm": 5}, "cancer": {"elastic_net": 6, "light_gbm": 6}}, "basic_training": {"all": {"elastic_net": 8, "light_gbm": 9}, "cvd": {"elastic_net": 10, "light_gbm": 11}, "cancer": {"elastic_net": 12, "light_gbm": 13}}}


class UpdateResultsAge:
    def __init__(self):

        self.category_row = None
        self.test_r2_column = None

    def check_better_training(self, main_category, category, algorithm, metrics, random_state):
        self.category_row = find_cell(main_category + f" {random_state}", category).row
        self.test_r2_column = find_all_cells(main_category + f" {random_state}", "test r²")[METRICS_COL_ORDER_AGE[algorithm]].col

        previous_test_r2 = get_cell(main_category + f" {random_state}", self.category_row, self.test_r2_column).value
                
        print("Previous test score:", previous_test_r2)
        print("New test score:", metrics["test r²"])

        return previous_test_r2 is None or float(previous_test_r2) <= metrics["test r²"]

    def update_results(self, main_category, algorithm, metrics, random_state, n_inner_search):
        print(metrics, n_inner_search)

        n_inner_search_column = find_all_cells(main_category + f" {random_state}", "N hyperparameters")[N_HYPERPARAMETERS_COL_ORDER_AGE[algorithm]].col
        update_cell(main_category + f" {random_state}", self.category_row, n_inner_search_column, n_inner_search)

        for metric_name in list(metrics.keys()):
            if metric_name == "test r²":
                continue
            metric_column = find_all_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_AGE[algorithm]].col
            update_cell(main_category + f" {random_state}", self.category_row, metric_column, np.round(metrics[metric_name], 3))
        
        update_cell(main_category + f" {random_state}", self.category_row, self.test_r2_column, np.round(metrics["test r²"], 3))



class UpdateResultsSurvival:
    def __init__(self):
        self.category_row = None
        self.previous_test_c_index = None

    def check_better_training(self, main_category, category, algorithm, target, metrics, training_mode, random_state):
        self.category_row = find_cell(main_category + f" {random_state}", category).row
        self.test_c_index_column = find_all_cells(main_category + f" {random_state}", "test C-index")[METRICS_COL_ORDER_SURVIVAL[training_mode][target][algorithm]].col
        
        previous_test_c_index = get_cell(main_category + f" {random_state}", self.category_row, self.test_c_index_column).value

        print("Previous test score:", previous_test_c_index)
        print("New test score:", metrics["test C-index"])

        return previous_test_c_index is None or float(previous_test_c_index) <= metrics["test C-index"]

    def update_results(self, main_category, algorithm, target, metrics, training_mode, random_state, n_inner_search):
        print(metrics)

        n_inner_search_column = find_all_cells(main_category + f" {random_state}", "N hyperparameters")[N_HYPERPARAMETERS_COL_ORDER_SURVIVAL[training_mode][target][algorithm]].col
        update_cell(main_category + f" {random_state}", self.category_row, n_inner_search_column, n_inner_search)

        for metric_name in list(metrics.keys()):
            if metric_name == "test C-index":
                continue
            metric_column = find_all_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_SURVIVAL[training_mode][target][algorithm]].col
            update_cell(main_category + f" {random_state}", self.category_row, metric_column, np.round(metrics[metric_name], 3))
        
        update_cell(main_category + f" {random_state}", self.category_row, self.test_c_index_column, np.round(metrics["test C-index"], 3))
