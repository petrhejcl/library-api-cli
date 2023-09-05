import click
import requests
import json

from utils import operations, urls, printing, validation, messages, http_codes
from book import COLUMNS as BOOK_COLUMNS
from book import COLUMNS_ALIASES as BOOK_COLUMNS_ALIASES

LIST_BOOKS = "list_books"
AUTHOR_SPECIFIC_OPERATIONS = [LIST_BOOKS]
AUTHOR_OPERATIONS = operations.BASIC_OPERATIONS + AUTHOR_SPECIFIC_OPERATIONS

#Columns as recieved in JSON
ID = "id"
NAME = "name"
SURNAME = "surname"
YEAR_OF_BIRTH = "yearOfBirth"

COLUMNS = [ID, NAME, SURNAME, YEAR_OF_BIRTH]

#Key is name of colummn as recieved in JSON, value is 
#title of column to be printed 
COLUMNS_ALIASES = {ID : "ID", 
           NAME : "Name", 
           SURNAME : "Surname", 
           YEAR_OF_BIRTH : "Year Of Birth"}

@click.command()
@click.argument("operation", type=click.Choice(AUTHOR_OPERATIONS), required=1)
@click.option("-id", "--id", type=click.INT)
@click.option("-n", "--name", type=click.STRING)
@click.option("-s", "--surname", type=click.STRING)
@click.option("-b", "--birth", type=click.INT)
def author(operation, id, name, surname, birth):
    if operation == operations.LIST:
        if id is None:
            list_authors()
        else:
            list_author_by_id(id)
    elif operation == operations.ADD:
        add_author(name=name, surname=surname, birth=birth)
    else: 
        if id is None:
            print("Please provide id to an author which you want to delete. For more info use -h or --help.")
        else:
            if operation == operations.DELETE:
                delete_author(id)
            elif operation == operations.UPDATE:
                update_author(id=id, name=name, surname=surname, birth=birth)
            elif operation == LIST_BOOKS:
                list_books_by_author(id)

def list_authors():
    response = requests.get(urls.AUTHOR_URL)
    if validation.response_status_code_is_2xx(response.status_code):
        data = response.json()
        columns_lengths = printing.get_max_columns_lengths(data, COLUMNS, COLUMNS_ALIASES)
        printing.print_item_list(data, COLUMNS, COLUMNS_ALIASES, columns_lengths)
    else:
        print(f"{messages.NOT_SUCCESSFUL}{response.status_code}")
    return response

def list_author_by_id(id):
    response = requests.get(f"{urls.AUTHOR_URL}/{id}")
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        columns_lengths = printing.get_max_columns_lengths(data, COLUMNS, COLUMNS_ALIASES)
        printing.print_item_list(data, COLUMNS, COLUMNS_ALIASES, columns_lengths)
    if response.status_code == http_codes.NOT_FOUND:
        print(messages.AUTHOR_NOT_FOUND)
    return response

def add_author(name=None, surname=None, birth=None):
    headers = {"Content-Type": "application/json"}
    data = {
        NAME : name,
        SURNAME : surname,
        YEAR_OF_BIRTH : birth
    }
    response = requests.post(urls.ADD_AUTHOR_URL, headers=headers, data=json.dumps(data))
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        print(messages.AUTHOR_ADDED)
        columns_lengths = printing.get_max_columns_lengths(data, COLUMNS, COLUMNS_ALIASES)
        printing.print_item_list(data, COLUMNS, COLUMNS_ALIASES, columns_lengths)
    else:
        print(f"{messages.NOT_SUCCESSFUL}{response.status_code}")
    return response

def delete_author(id):
    response = requests.delete(f"{urls.DELETE_AUTHOR_URL}/{id}")
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        print(messages.AUTHOR_DELETED)
        columns_lengths = printing.get_max_columns_lengths(data, COLUMNS, COLUMNS_ALIASES)
        printing.print_item_list(data, COLUMNS, COLUMNS_ALIASES, columns_lengths)
    if response.status_code == http_codes.NOT_FOUND:
        print(messages.AUTHOR_NOT_FOUND)
    return response

def update_author(id, name=None, surname=None, birth=None):
    headers = {"Content-Type": "application/json"}
    data = {
        NAME : name,
        SURNAME : surname,
        YEAR_OF_BIRTH : birth
    }
    response = requests.put(f"{urls.UPDATE_AUTHOR_URL}/{id}", headers=headers, data=json.dumps(data))
    if validation.response_status_code_is_2xx(response.status_code):
        data = [response.json()]
        print(messages.AUTHOR_UPDATED)
        columns_lengths = printing.get_max_columns_lengths(data, COLUMNS, COLUMNS_ALIASES)
        printing.print_item_list(data, COLUMNS, COLUMNS_ALIASES, columns_lengths)
    if response.status_code == http_codes.NOT_FOUND:
        print(messages.AUTHOR_NOT_FOUND)
    return response

def list_books_by_author(id):
    author_response = list_author_by_id(id)
    if author_response.status_code == http_codes.NOT_FOUND:
        return author_response
    books_response = requests.get(f"{urls.BOOKS_BY_AUTHOR_URL}/{id}")
    data = books_response.json()
    if not data:
        print(messages.AUTHOR_WITHOUT_BOOKS)
    else:
        columns_lengths = printing.get_max_columns_lengths(data, BOOK_COLUMNS, BOOK_COLUMNS_ALIASES)
        printing.print_item_list(data, BOOK_COLUMNS, BOOK_COLUMNS_ALIASES, columns_lengths)
    return books_response


    