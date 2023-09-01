import click
import requests
import json

from setup import operations, urls

LIST_BOOKS = "list_books"
AUTHOR_SPECIFIC_OPERATIONS = [LIST_BOOKS]
AUTHOR_OPERATIONS = operations.BASIC_OPERATIONS + AUTHOR_SPECIFIC_OPERATIONS

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
    print(response.text)

def list_author_by_id(id):
    response = requests.get(f"{urls.AUTHOR_URL}/{id}")
    print(response.text)

def add_author(name=None, surname=None, birth=None):
    headers = {"Content-Type": "application/json"}
    data = {
        "name" : name,
        "surname" : surname,
        "yearOfBirth": birth
    }
    response = requests.post(urls.ADD_AUTHOR_URL, headers=headers, data=json.dumps(data))
    print(response.text)

def delete_author(id):
    response = requests.delete(f"{urls.DELETE_AUTHOR_URL}/{id}")
    print(response.text)

def update_author(id, name=None, surname=None, birth=None):
    headers = {"Content-Type": "application/json"}
    data = {
        "name" : name,
        "surname" : surname,
        "yearOfBirth": birth
    }
    response = requests.put(f"{urls.UPDATE_AUTHOR_URL}/{id}", headers=headers, data=json.dumps(data))
    print(response.text)

def list_books_by_author(id):
    response = requests.get(f"{urls.BOOKS_BY_AUTHOR_URL}/{id}")
    print(response.text)