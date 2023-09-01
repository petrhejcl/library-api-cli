import click
import requests
import json

from setup import operations, urls

@click.command()
@click.argument("operation", type=click.Choice(operations.BASIC_OPERATIONS), required=1)
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
            print("Please provied id to a book which you want to delete. For more info use -h or --help.")
        else:
            if operation == operations.DELETE:
                delete_book(id)
            elif operation == operations.UPDATE:
                update_book(id=id, isbn=isbn, name=name, release=release, genre=genre)

def list_books():
    response = requests.get(urls.BOOK_URL)
    print(response.text)

#TODO: Fix message when book with given ID does not exist
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