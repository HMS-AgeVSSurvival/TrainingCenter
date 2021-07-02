import numpy as np

from prediction.utils import find_cell, findall_cells, get_cell, update_cell, format_cell


METRICS_COL_ORDER_AGE = {"elastic_net": 2, "light_gbm": 3}
METRICS_COL_ORDER_SURVIVAL = {"full_training": {"all": {"elastic_net": 12, "light_gbm": 13}, "cvd": {"elastic_net": 14, "light_gbm": 15}, "cancer": {"elastic_net": 16, "light_gbm": 17}}, "basic_training": {"all": {"elastic_net": 18, "light_gbm": 19}, "cvd": {"elastic_net": 20, "light_gbm": 21}, "cancer": {"elastic_net": 22, "light_gbm": 23}}}

BEST_METRICS_COL_ORDER_SURVIVAL = {"all": 0, "cvd": 1, "cancer": 2}


def update_results_age(main_category, category, algorithm, metrics):
    results_updated = False

    category_row = find_cell(main_category, category).row
    train_r2_column = findall_cells(main_category, "train r²")[METRICS_COL_ORDER_AGE[algorithm]].col

    previous_train_r2 = get_cell(main_category, category_row, train_r2_column).value
    if previous_train_r2 is None or float(previous_train_r2) < metrics["train r²"]:
        print(metrics)
        results_updated = True
        for metric_name in list(metrics.keys()):
            metric_column = findall_cells(main_category, metric_name)[METRICS_COL_ORDER_AGE[algorithm]].col
            update_cell(main_category, category_row, metric_column, np.round(metrics[metric_name], 3))

    summary_main_category = "summary " + main_category
    summary_category_row = find_cell(summary_main_category, category).row
    best_train_r2_column = find_cell(summary_main_category, "best train r²").col

    previous_best_train_r2 = get_cell(summary_main_category, summary_category_row, best_train_r2_column).value
    if previous_best_train_r2 is None or float(previous_best_train_r2) < metrics["train r²"]:
        update_cell(summary_main_category, summary_category_row, best_train_r2_column, np.round(metrics["train r²"], 3))
        format_cell(summary_main_category, summary_category_row, best_train_r2_column, algorithm)

    return results_updated


def update_results_survival(main_category, category, algorithm, target, metrics, training_type):
    results_updated = False
    category_row = find_cell(main_category, category).row
    train_c_index_column = findall_cells(main_category, "train C-index")[METRICS_COL_ORDER_SURVIVAL[training_type][target][algorithm]].col

    previous_train_c_index = get_cell(main_category, category_row, train_c_index_column).value
    if previous_train_c_index is None or float(previous_train_c_index) < metrics["train C-index"]:
        print(metrics)
        results_updated = True
        for metric_name in list(metrics.keys()):
            metric_column = findall_cells(main_category, metric_name)[METRICS_COL_ORDER_SURVIVAL[training_type][target][algorithm]].col
            update_cell(main_category, category_row, metric_column, np.round(metrics[metric_name], 3))

    summary_main_category = "summary " + main_category
    summary_category_row = find_cell(summary_main_category, category).row
    if training_type == "full_training":
        score_name = "best train C-index"
    elif training_type == "basic_training":
        score_name = "best basic train C-index"
    best_train_c_index_column = findall_cells(summary_main_category, score_name)[BEST_METRICS_COL_ORDER_SURVIVAL[target]].col

    previous_best_train_c_index = get_cell(summary_main_category, summary_category_row, best_train_c_index_column).value
    if previous_best_train_c_index is None or float(previous_best_train_c_index) < metrics["train C-index"]:
        update_cell(summary_main_category, summary_category_row, best_train_c_index_column, np.round(metrics["train C-index"], 3))
        format_cell(summary_main_category, summary_category_row, best_train_c_index_column, algorithm)
    
    return results_updated


    return results_updated
