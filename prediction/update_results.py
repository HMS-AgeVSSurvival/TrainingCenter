import numpy as np

from utils.google_sheets_sdk import find_cell, findall_cells, get_cell, update_cell, format_cell


METRICS_COL_ORDER_AGE = {"elastic_net": 0, "light_gbm": 1}
METRICS_COL_ORDER_SURVIVAL = {"full_training": {"all": {"elastic_net": 0, "light_gbm": 1}, "cvd": {"elastic_net": 2, "light_gbm": 3}, "cancer": {"elastic_net": 4, "light_gbm": 5}}, "basic_training": {"all": {"elastic_net": 6, "light_gbm": 7}, "cvd": {"elastic_net": 8, "light_gbm": 9}, "cancer": {"elastic_net": 10, "light_gbm": 11}}}
BEST_METRICS_COL_ORDER_SURVIVAL = {"all": 0, "cvd": 1, "cancer": 2}


def update_results_age(main_category, category, algorithm, metrics, random_state):
    results_updated = False

    category_row = find_cell(main_category + f" {random_state}", category).row
    test_r2_column = findall_cells(main_category + f" {random_state}", "test r²")[METRICS_COL_ORDER_AGE[algorithm]].col

    previous_test_r2 = get_cell(main_category + f" {random_state}", category_row, test_r2_column).value
    if previous_test_r2 is None or float(previous_test_r2) < metrics["test r²"]:
        print(metrics)
        results_updated = True
        for metric_name in list(metrics.keys()):
            metric_column = findall_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_AGE[algorithm]].col
            update_cell(main_category + f" {random_state}", category_row, metric_column, np.round(metrics[metric_name], 3))

    return results_updated


def update_results_survival(main_category, category, algorithm, target, metrics, training_mode, random_state):
    results_updated = False

    category_row = find_cell(main_category + f" {random_state}", category).row
    test_c_index_column = findall_cells(main_category + f" {random_state}", "test C-index")[METRICS_COL_ORDER_SURVIVAL[training_mode][target][algorithm]].col

    previous_test_c_index = get_cell(main_category + f" {random_state}", category_row, test_c_index_column).value
    if previous_test_c_index is None or float(previous_test_c_index) < metrics["test C-index"]:
        print(metrics)
        results_updated = True
        for metric_name in list(metrics.keys()):
            metric_column = findall_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_SURVIVAL[training_mode][target][algorithm]].col
            update_cell(main_category + f" {random_state}", category_row, metric_column, np.round(metrics[metric_name], 3))
        
    return results_updated
