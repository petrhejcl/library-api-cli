import click
import requests
import json

from utils import operations, urls

LIST_AUTHORS = "list_authors"
LIST_LIBRARIES = "list_libraries"
BOOK_SPECIFIC_OPERATIONS = [LIST_AUTHORS, LIST_LIBRARIES]
BOOK_OPERATIONS = operations.BASIC_OPERATIONS + BOOK_SPECIFIC_OPERATIONS

#Columns as recieved in JSON
ID = "id"
ISBN = "isbn"
TITLE = "title"
YEAR_OF_RELEASE = "yearOfRelease"
GENRE = "genre"

COLUMNS = [ID, ISBN, TITLE, YEAR_OF_RELEASE, GENRE]

#Key is name of colummn as recieved in JSON, value is 
#title of column to be printed 
COLUMNS_ALIASES = {ID : "ID", 
           ISBN : "ISBN", 
           TITLE : "Title", 
           YEAR_OF_RELEASE: "Year Of Release",
           GENRE : "Genre"}

@click.command()
@click.argument("operation", type=click.Choice(BOOK_OPERATIONS), required=1)
@click.option("-id", "--id", type=click.INT)
@click.option("-isbn", "--isbn", type=click.STRING)
@click.option("-n", "--name", type=click.STRING)
@click.option("-r", "--release", type=click.INT)
@click.option("-g", "--genre", type=click.STRING)
def book(operation, id, isbn, name, release, genre):
    if operation == operations.LIST:
        if id is None:
            list_books()
        else:
            list_book_by_id(id)
    elif operation == operations.ADD:
        add_book(isbn=isbn, name=name, release=release, genre=genre)
    else: 
        if id is None:
            print("Please provide id to a book which you want to delete. For more info use -h or --help.")
        else:
            if operation == operations.DELETE:
                delete_book(id)
            elif operation == operations.UPDATE:
                update_book(id=id, isbn=isbn, name=name, release=release, genre=genre)
            elif operation == LIST_AUTHORS:
                list_authors_by_book(id)
            elif operation == LIST_LIBRARIES:
                list_libraries_by_book(id)

def list_books():
    response = requests.get(urls.BOOK_URL)
    print(response.text)

def list_book_by_id(id):
    response = requests.get(f"{urls.BOOK_URL}/{id}")
    print(response.text)

def add_book(isbn=None, name=None, release=None, genre=None):
    headers = {"Content-Type": "application/json"}
    data = {
        "isbn" : isbn,
        "name" : name,
        "yearOfRelease" : release,
        "genre": genre
    }
    response = requests.post(urls.ADD_BOOK_URL, headers=headers, data=json.dumps(data))
    print(response.text)

def delete_book(id):
    response = requests.delete(f"{urls.DELETE_BOOK_URL}/{id}")
    print(response.text)

def update_book(id, isbn=None, name=None, release=None, genre=None):
    headers = {"Content-Type": "application/json"}
    data = {
        "isbn" : isbn,
        "name" : name,
        "yearOfRelease" : release,
        "genre": genre
    }
    response = requests.put(f"{urls.UPDATE_BOOK_URL}/{id}", headers=headers, data=json.dumps(data))
    print(response.text)

def list_libraries_by_book(id):
    response = requests.get(f"{urls.LIBRARIES_BY_BOOK_URL}/{id}")
    print(response.text)

def list_authors_by_book(id):
    response = requests.get(f"{urls.AUTHORS_BY_BOOK_URL}/{id}")
    print(response.text)

