import pandas as pd
from tqdm import tqdm

from utils.google_sheets_sdk import get_col_values, find_all_cells, find_cell, update_cells
from prediction import AGE_COLUMN, BASIC_TRAINING_COLUMNS

INFORMATION_COL = {"age": 0, "all": 1, "cvd": 2, "cancer": 3}

if __name__ == "__main__":
    for main_category in tqdm(["examination", "laboratory", "questionnaire"]):
        for target in ["age", "all", "cvd", "cancer"]:
            information = pd.DataFrame(None, columns=["n_participants", "n_variables", "min", "max"], index=get_col_values(f"{main_category} 1", "category")[3:])
            for category in information.index:
                data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")
                
                if target == "all":
                    data.drop(index=data.index[data["survival_type_alive"].isna()], inplace=True)
                elif target == "cvd":
                    data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cvd"] == 1)]
                elif target == "cancer":
                    data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cancer"] == 1)]

                data_age = data[AGE_COLUMN]
                data.drop(columns=data.columns[data.columns.isin(BASIC_TRAINING_COLUMNS)], inplace=True)

                information.loc[category, ["n_participants", "n_variables"]] = data.shape
                if len(data_age) > 0:
                    information.loc[category, ["min", "max"]] = (data_age.min() / 12).round(1), (data_age.max() / 12).round(1)
            
            for random_state in [1, 2]:
                first_row = find_cell(f"{main_category} {random_state}", information.index[0]).row
                last_row = find_cell(f"{main_category} {random_state}", information.index[-1]).row
                first_col = find_all_cells(f"{main_category} {random_state}", "n_participants")[INFORMATION_COL[target]].col
                last_col = find_all_cells(f"{main_category} {random_state}", "max")[INFORMATION_COL[target]].col
                update_cells(f"{main_category} {random_state}", first_row, last_row, first_col, last_col, information.values)
