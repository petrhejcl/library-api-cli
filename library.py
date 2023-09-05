import click
import requests
import json

from utils import operations, urls, validation, printing

LIST_BOOKS = "list_books"
LIBRARY_SPECIFIC_OPERATIONS = [LIST_BOOKS]
LIBRARY_OPERATIONS = operations.BASIC_OPERATIONS + LIBRARY_SPECIFIC_OPERATIONS

#Columns as recieved in JSON
ID = "id"
NAME = "name"
CITY = "city"
STREET = "street"
STREET_NUMBER = "streetNumber"
DESCRIPTION = "description"

COLUMNS = [ID, NAME, CITY, STREET, STREET_NUMBER, DESCRIPTION]

#Key is name of colummn as recieved in JSON, value is 
#title of column to be printed 
COLUMNS_ALIASES = {ID : "ID", 
           NAME : "Name",
           CITY : "City",
           STREET : "Street",
           STREET_NUMBER : "Street Number",
           DESCRIPTION : "Description"}

@click.command()
@click.argument("operation", type=click.Choice(LIBRARY_OPERATIONS), required=1)
@click.option("-id", "--id", type=click.INT)
@click.option("-n", "--name", type=click.STRING)
@click.option("-c", "--city", type=click.STRING)
@click.option("-s", "--street", type=click.STRING)
@click.option("-sn", "--street_number", type=click.INT)
@click.option("-d", "--description", type=click.STRING)
def library(operation, id, name, city, street, street_number, description):
    if operation == operations.LIST:
        if id is None:
            list_libraries()
        else:
            list_library_by_id(id)
    elif operation == operations.ADD:
        add_library(name=name, city=city, street=street, street_number=street_number, description=description)
    else: 
        if id is None:
            print("Please provide id to a library which you want to take action with. For more info use -h or --help.")
        else:
            if operation == operations.DELETE:
                delete_library(id)
            elif operation == operations.UPDATE:
                update_library(id=id, name=name, city=city, street=street, street_number=street_number, description=description)
            elif operation == LIST_BOOKS:
                list_books_by_library(id)

def list_libraries():
    response = requests.get(urls.AUTHOR_URL)
    if validation.response_status_code_is_2xx(response.status_code):
        data = response.json()
        columns_lengths = printing.get_max_columns_lengths(data, COLUMNS, COLUMNS_ALIASES)
        printing.print_item_list(data, COLUMNS, COLUMNS_ALIASES, columns_lengths)
    return response

def list_library_by_id(id):
    response = requests.get(f"{urls.LIBRARY_URL}/{id}")
    print(response.text)

def add_library(name=None, city=None, street=None, street_number=None, description=None):
    headers = {"Content-Type": "application/json"}
    data = {
        "name" : name,
        "city" : city,
        "street" : street,
        "streetNumber": street_number,
        "description" : description
    }
    response = requests.post(urls.ADD_LIBRARY_URL, headers=headers, data=json.dumps(data))
    print(response.text)

def delete_library(id):
    response = requests.delete(f"{urls.DELETE_LIBRARY_URL}/{id}")
    print(response.text)

def update_library(id, name=None, city=None, street=None, street_number=None, description=None):
    headers = {"Content-Type": "application/json"}
    data = {
        "name" : name,
        "city" : city,
        "street" : street,
        "streetNumber": street_number,
        "description" : description
    }
    response = requests.put(f"{urls.UPDATE_LIBRARY_URL}/{id}", headers=headers, data=json.dumps(data))
    print(response.text)

def list_books_by_library(id):
    response = requests.get(f"{urls.BOOKS_BY_LIBRARY_URL}/{id}")
    print(response.text)