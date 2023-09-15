import requests
import json

from utils import validation, printing, http_codes

def list_all(url, columns, columns_aliases, general_error_message):
    response = requests.get(url)
    if validation.response_status_code_is_2xx(response.status_code):
        data = response.json()
        columns_lengths = printing.get_max_columns_lengths(data, columns, columns_aliases)
        printing.print_item_list(data, columns, columns_aliases, columns_lengths)
    else:
        print(general_error_message)
    return response


def list_by_id(url, columns, columns_aliases, not_found_message, general_error_message):
    response = requests.get(url)
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        columns_lengths = printing.get_max_columns_lengths(data, columns, columns_aliases)
        printing.print_item_list(data, columns, columns_aliases, columns_lengths)
    elif response.status_code == http_codes.NOT_FOUND:
        print(not_found_message)
    else:
        print(general_error_message) 
    return response


def add(data, url, columns, columns_aliases, success_message, general_error_message):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        print(success_message)
        columns_lengths = printing.get_max_columns_lengths(data, columns, columns_aliases)
        printing.print_item_list(data, columns, columns_aliases, columns_lengths)
    else:
        print(general_error_message)
    return response


def update(data, url, columns, columns_aliases, success_message, not_found_message, general_error_message):
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        print(success_message)
        columns_lengths = printing.get_max_columns_lengths(data, columns, columns_aliases)
        printing.print_item_list(data, columns, columns_aliases, columns_lengths)
    elif response.status_code == http_codes.NOT_FOUND:
        print(not_found_message)
    else:
        print(general_error_message)
    return response


def delete(url, columns, columns_aliases, success_message, not_found_message, general_error_message):
    response = requests.delete(url)
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        print(success_message)
        columns_lengths = printing.get_max_columns_lengths(data, columns, columns_aliases)
        printing.print_item_list(data, columns, columns_aliases, columns_lengths)
    if response.status_code == http_codes.NOT_FOUND:
        print(not_found_message)
    else:
        print(general_error_message)
    return response

BASIC_OPERATIONS = [list_all, ]