import pandas as pd
from tqdm import tqdm

from utils.google_sheets_sdk import get_col_values, find_cell, update_cells
from prediction import AGE_COLUMN


if __name__ == "__main__":
    for main_category in tqdm(["examination", "laboratory", "questionnaire"]):
        information = pd.DataFrame(None, columns=["n_participants", "n_variables", "min", "max"], index=get_col_values(main_category, "category")[3:])

        for category in information.index:
            data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")
            data.drop(columns=data.columns[data.columns.str.startswith("prediction")], inplace=True)
            data.drop(index=data.index[data.index.astype(str).str.startswith("feature_importances")], inplace=True)

            information.loc[category, ["n_participants", "n_variables"]] = data.shape
            information.loc[category, ["min", "max"]] = (data[AGE_COLUMN].min() / 12).round(1), (data[AGE_COLUMN].max() / 12).round(1)

        first_row = find_cell(main_category, information.index[0]).row
        last_row = find_cell(main_category, information.index[-1]).row
        first_col = find_cell(main_category, "n_participants").col
        last_col = find_cell(main_category, "max").col

        update_cells(main_category, first_row, last_row, first_col, last_col, information.values)
