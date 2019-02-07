# Googlebooks
This application requests a search term, then displays a list of books from https://www.googleapis.com/books/v1/volumes which contain that search term. If the user specifies a particular book from that list, an HTML page is displayed giving further details of that book.

In the list page, the following details of each book are displayed:
* Title
* Author(s)

Each list page is limited to how may books can be shown. Once the page is shown, the user has the following options:
* Show next page
* Show previous page
* Refresh the current page
* Change the number of entries ddisplayed on each page (up to a maximum of 40)
* Change the search term
* Request details of a specific book
* Quit

In the details page, the following details (where exist) of each book are displayed:
* Cover art
* Title
* Subtitle
* Author(s)
* Description
* Publication Date

To run:
* pip install -r requirements.txt
* python googlebooks.py