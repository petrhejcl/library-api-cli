import click

from book import book
from author import author

#TODO: 
#Create nice help menu
#Create formatting
#Create library endpoint mapping
#Create authorship endpoint mapping
#Create ownership endpoint mapping
#Fix message when item with given ID does not exist (finding, deleting, updating)
#Create tests


@click.group
def commands():
    pass

commands.add_command(book)
commands.add_command(author)

if __name__ == "__main__":
    commands()