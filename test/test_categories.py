import unittest
import os
import pandas as pd

from utils.google_sheets_sdk import get_col_values


class TestCategories(unittest.TestCase):
    def test_matching_categories(self):
        # Test if all categories are in the google sheet.
        for main_category in ["examination", "laboratory", "questionnaire"]:
            categories_in_sheet = pd.Index(
                get_col_values(main_category, "category")[3:]
            )
            categories_in_data = (
                pd.Index(os.listdir(f"data/{main_category}"))
                .str.split(".")
                .map(lambda splitted_file: splitted_file[0])
            )

            self.assertTrue(all(categories_in_sheet.isin(categories_in_data)))
            self.assertTrue(all(categories_in_data.isin(categories_in_sheet)))
