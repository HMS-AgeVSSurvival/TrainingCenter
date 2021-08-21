import os
import time
import numpy as np
import gspread
import requests
import json
from json.decoder import JSONDecodeError

from prediction import COLOR_ALGORITHM
from utils.number_to_letter import get_letter


def get_worksheet(main_category):
    service_account_id = np.random.randint(1, 6)
    gc = gspread.service_account(filename=f"credentials/credentials_{service_account_id}.json")
    google_sheet = gc.open_by_key(os.environ.get("GOOGLE_RESULTS_SHEET_ID"))
    
    return google_sheet.worksheet(main_category)


def handle_gspread_error(error):
    try:
        error = json.loads(error.response._content)
    except JSONDecodeError:
        raise error

    if error["error"]["code"] in [404, 429, 101, 500]:  # Means too many Google Sheet API's calls
        sleep_time = 61
        print(f"Sleep {sleep_time}")
        time.sleep(sleep_time)
    else:
        raise error


def update_cell(main_category, row, col, value):
    cell_updated = False
    while not cell_updated:
        try:
            worksheet = get_worksheet(main_category)
            worksheet.update_cell(row, col, str(value))
            cell_updated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass




def update_cells(main_category, first_row, last_row, first_col, last_col, values):
    first_col_letter = get_letter(first_col)
    last_col_letter = get_letter(last_col)

    cell_updated = False
    while not cell_updated:
        try:
            worksheet = get_worksheet(main_category)
            worksheet.update(f"{first_col_letter}{first_row}:{last_col_letter}{last_row}", list(map(list, values.astype(str))))
            cell_updated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)     
        except requests.exceptions.ReadTimeout:
            pass


def find_cell(main_category, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(main_category)
            cell = worksheet.find(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass

    return cell


def find_all_cells(main_category, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(main_category)
            cells = worksheet.findall(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass

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
        except requests.exceptions.ReadTimeout:
            pass

    return cell


def get_col_values(main_category, col_name):
    col = find_cell(main_category, col_name).col

    got_col = False
    while not got_col:
        try:
            worksheet = get_worksheet(main_category)
            col_values = worksheet.col_values(col)
            got_col = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass

    return col_values


def format_cell(main_category, row, col, algorithm):
    letter_col = get_letter(col)

    cell_formated = False
    while not cell_formated:
        try:
            worksheet = get_worksheet(main_category)
            worksheet.format(f"{letter_col}{row}", {"backgroundColor": COLOR_ALGORITHM[algorithm]})
            cell_formated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)        
        except requests.exceptions.ReadTimeout:
            pass