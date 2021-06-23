import os
import numpy as np
import time
import gspread


GC = gspread.service_account(filename='credentials.json')
GOOGLE_SHEET = GC.open_by_key(os.environ.get('GOOGLE_RESULTS_SHEET_ID'))
METRICS_COL_ORDER_AGE = {"elastic_net": 2, "light_gbm": 3}
METRICS_COL_ORDER_SURVIVAL = {"all": {"elastic_net": 6, "light_gbm": 7}, "cvd": {"elastic_net": 8, "light_gbm": 9}, "cancer": {"elastic_net": 10, "light_gbm": 11}}


def update_results_age(main_category, category, algorithm, metrics):
    results_updated = False
    while not results_updated:
        try:
            worksheet = GOOGLE_SHEET.worksheet(main_category)
            category_row = worksheet.find(category).row
            test_r2_column = worksheet.findall("train r²")[METRICS_COL_ORDER_AGE[algorithm]].col

            previous_test_r2 = worksheet.cell(category_row, test_r2_column).value
            if previous_test_r2 is None or float(previous_test_r2) < metrics["train r²"]:
                for metric_name in list(metrics.keys()):
                    metric_column = worksheet.findall(metric_name)[METRICS_COL_ORDER_AGE[algorithm]].col
                    worksheet.update_cell(category_row, metric_column, np.round(metrics[metric_name], 3))
            results_updated = True
        except gspread.exceptions.APIError:  # Means too many Google Sheet API's calls
            sleep_time = np.random.randint(101, 1000)
            print(f"Sleep {sleep_time}")
            time.sleep(sleep_time)


def update_results_survival(main_category, category, algorithm, target, metrics):
    results_updated = False
    while not results_updated:
        try:
            worksheet = GOOGLE_SHEET.worksheet(main_category)
            category_row = worksheet.find(category).row
            test_c_index_column = worksheet.findall("train C-index")[METRICS_COL_ORDER_SURVIVAL[target][algorithm]].col

            previous_test_c_index = worksheet.cell(category_row, test_c_index_column).value
            if previous_test_c_index is None or float(previous_test_c_index) < metrics["train C-index"]:
                for metric_name in list(metrics.keys()):
                    metric_column = worksheet.findall(metric_name)[METRICS_COL_ORDER_SURVIVAL[target][algorithm]].col
                    if metrics[metric_name] != -1:  # -1 means that there is no data available
                        worksheet.update_cell(category_row, metric_column, np.round(metrics[metric_name], 3))
                    else:
                        worksheet.update_cell(category_row, metric_column, metrics[metric_name])
            results_updated = True
        except gspread.exceptions.APIError:  # Means too many Google Sheet API's calls
            sleep_time = np.random.randint(101, 1000)
            print(f"Sleep {sleep_time}")
            time.sleep(sleep_time)
