import click

from book import book

#TODO: 
#Create nice help menu
#Create formatting
#Create author endpoint mapping
#Create library endpoint mapping
#Create authorship endpoint mapping
#Create ownership endpoint mapping

@click.group
def commands():
    pass

commands.add_command(book)

if __name__ == "__main__":
    commands()