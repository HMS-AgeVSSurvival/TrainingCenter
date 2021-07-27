import numpy as np

from utils.google_sheets_sdk import find_cell, findall_cells, get_cell, update_cell


METRICS_COL_ORDER_AGE = {"elastic_net": 2, "light_gbm": 3}
METRICS_COL_ORDER_SURVIVAL = {"all": {"elastic_net": 12, "light_gbm": 13}, "cvd": {"elastic_net": 14, "light_gbm": 15}, "cancer": {"elastic_net": 16, "light_gbm": 17}}


def update_results_age(main_category, category, algorithm, metrics, random_state):
    results_updated = False

    category_row = find_cell(main_category + f" {random_state}", category).row
    train_r2_column = findall_cells(main_category + f" {random_state}", "train r²")[METRICS_COL_ORDER_AGE[algorithm]].col

    previous_train_r2 = get_cell(main_category + f" {random_state}", category_row, train_r2_column).value
    if previous_train_r2 is None or float(previous_train_r2) <= metrics["train r²"]:
        print(metrics)
        results_updated = True
        for metric_name in list(metrics.keys()):
            metric_column = findall_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_AGE[algorithm]].col
            update_cell(main_category + f" {random_state}", category_row, metric_column, np.round(metrics[metric_name], 3))

    return results_updated


def update_results_survival(main_category, category, algorithm, target, metrics, random_state):
    results_updated = False
    category_row = find_cell(main_category + f" {random_state}", category).row
    train_c_index_column = findall_cells(main_category + f" {random_state}", "train C-index")[METRICS_COL_ORDER_SURVIVAL[target][algorithm]].col

    previous_train_c_index = get_cell(main_category + f" {random_state}", category_row, train_c_index_column).value
    if previous_train_c_index is None or float(previous_train_c_index) <= metrics["train C-index"]:
        print(metrics)
        results_updated = True
        for metric_name in list(metrics.keys()):
            metric_column = findall_cells(main_category + f" {random_state}", metric_name)[METRICS_COL_ORDER_SURVIVAL[target][algorithm]].col
            update_cell(main_category + f" {random_state}", category_row, metric_column, np.round(metrics[metric_name], 3))

    return results_updated
