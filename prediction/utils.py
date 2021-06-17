import os
import numpy as np
import gspread


GC = gspread.service_account(filename='credentials.json')
GOOGLE_SHEET = GC.open_by_key(os.environ.get('GOOGLE_RESULTS_SHEET_ID'))
TEST_R2_COL_ORDER = {"elastic_net": 0, "light_gbm": 1}


def update_results(main_category, category, algorithm, metrics):
    worksheet = GOOGLE_SHEET.worksheet(main_category)
    category_row = worksheet.find(category).row
    test_r2_column = worksheet.findall("test r²")[TEST_R2_COL_ORDER[algorithm]].col

    previous_test_r2 = worksheet.cell(category_row, test_r2_column).value
    if previous_test_r2 is None or float(previous_test_r2) < metrics["test r²"]:
        for metric_name in list(metrics.keys()):
            metric_column = worksheet.findall(metric_name)[TEST_R2_COL_ORDER[algorithm]].col
            worksheet.update_cell(category_row, metric_column, np.round(metrics[metric_name], 3))