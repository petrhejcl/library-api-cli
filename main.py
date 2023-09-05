import click

from book import book
from author import author
from library import library

#TODO: 
#Create nice help menu
#Fix formatting to listing
#Create authorship endpoint mapping
#Create ownership endpoint mapping
#Add option to recieve raw json response (listing etc.)
#Fix message when item with given ID does not exist (finding, deleting, updating)
#Fix message when adding a new item
#Fix message when deleting an item
#Fix message when updating an item
#Add error handling and appropriate responding to status codes
#Create (especially error) message constants
#Create tests
#Add return values to functions?


@click.group
def commands():
    pass

commands.add_command(book)
commands.add_command(author)
commands.add_command(library)

if __name__ == "__main__":
    commands()