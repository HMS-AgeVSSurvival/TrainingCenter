import os
import time
import numpy as np
import gspread
import json

from prediction import COLOR_ALGORITHM


def get_worksheet(main_category):
    service_account_id = np.random.randint(1, 6)
    gc = gspread.service_account(filename=f"credentials/credentials_{service_account_id}.json")
    google_sheet = gc.open_by_key(os.environ.get("GOOGLE_RESULTS_SHEET_ID"))
    
    return google_sheet.worksheet(main_category)


def handle_gspread_error(error):
    error = json.loads(error.response._content)
    if error["error"]["code"] == 429:  # Means too many Google Sheet API's calls
        sleep_time = 20
        print(f"Sleep {sleep_time}")
        time.sleep(sleep_time)
    else:
        raise error


def update_cell(main_category, row, col, value):
    cell_updated = False
    while not cell_updated:
        try:
            worksheet = get_worksheet(main_category)
            worksheet.update_cell(row, col, float(value))
            cell_updated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)


def find_cell(main_category, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(main_category)
            cell = worksheet.find(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)

    return cell


def findall_cells(main_category, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(main_category)
            cells = worksheet.findall(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)

    return cells


def get_cell(main_category, row, col):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(main_category)
            cell = worksheet.cell(row, col)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)

    return cell


def format_cell(main_category, row, col, algorithm):
    letter_col = chr(ord('A') - 1 + col)

    cell_formated = False
    while not cell_formated:
        try:
            worksheet = get_worksheet(main_category)
            worksheet.format(f"{letter_col}{row}", {"backgroundColor": COLOR_ALGORITHM[algorithm]})
            cell_formated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)