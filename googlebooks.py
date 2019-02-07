import urllib.request
import json
import os
import textwrap

# CONSTANTS
KEY_TITLE = "title"
KEY_SUBTITLE = "subtitle"
KEY_AUTHORS = "authors"
KEY_PUBDATE = "publication_date"
KEY_DESCRIPTION = "description"
KEY_PRINT_TYPE = "printType"
KEY_IMAGE_LINKS = "imageLinks"
KEY_THUMBNAIL = "thumbnail"

HTML_START_TABLE = "<table><tr><td>"
HTML_NEXT_CELL = "</td><td>"
HTML_END_TABLE = "</td></tr></table>"

BOOK_FILENAME = 'bookfile.html'

# Clear the screen.
def _clear_screen():
	os.system('cls')

# Add surrounding HTML tags to a string.
def _tagged(tag, textin):
	return("<" + tag + ">" + textin + "</" + tag + ">")

# Get size of displayed list.
def _get_list_size():
	# This must return an integer between 1 and 40.
	while True:
		list_size_text = input("Enter number of books per page (Maximum is 40): ")
		if list_size_text.isnumeric():
			list_size = int(list_size_text)
			if list_size > 0 and list_size <= 40:
				return list_size

if __name__ == "__main__":

	# Get search term.
	query = input("Enter search term: ")

	# Get list size.
	max_books_per_page = _get_list_size()

	print()
	startindex = 0
	while True:
		url_page = "https://www.googleapis.com/books/v1/volumes?q=" + query \
				+ "&startIndex=" + str(startindex) \
				+ "&maxResults=" + str(max_books_per_page)
		with urllib.request.urlopen(url_page) as f:
			text = f.read()
		decodedtext = text.decode('utf-8')
		obj = json.loads(decodedtext)
		no_of_items_returned = len(obj["items"])
		_clear_screen()
		print(f"Search term: {query}")
		print()
		for item_no in range(no_of_items_returned):
			volumeinfo = obj["items"][item_no]["volumeInfo"]
			if KEY_TITLE in volumeinfo:
				title = volumeinfo[KEY_TITLE]
			else:
				title = "Untitled"
			authors = ""
			if KEY_AUTHORS in volumeinfo:
				authors = '/'.join(volumeinfo[KEY_AUTHORS])
				print(f"{startindex+item_no+1}: {title}, by {authors}")
			else:
				print(f"{startindex+item_no+1}: {title}")
		print()
		while True:
			response = input("(n)ext, (p)revious, (r)efresh list, change (l)ist size, change (s)earch term, number or (q)uit: ")
			if response == "q":
				_clear_screen()
				raise SystemExit()
			if response == "n":
				startindex = startindex + no_of_items_returned
				break
			if response == "p":
				if startindex >= no_of_items_returned:
					startindex = startindex - no_of_items_returned
				else:
					startindex = 0
				break
			if response == "r":
				break
			if response == "l":
				max_books_per_page = _get_list_size()
				break
			if response == "s":
				query=input("Enter search term: ")
				startindex = 0
				break
			if response.isnumeric():
				item_no = int(response) - startindex - 1
				if item_no < 0 or item_no > no_of_items_returned -1:
					print("Invalid number")
				else:
					bookfile=open(BOOK_FILENAME,'w')
					volumeinfo = obj["items"][item_no]["volumeInfo"]
					
					# Start table.
					bookfile.write(HTML_START_TABLE)
					
					# Add book image if it exists.
					if KEY_IMAGE_LINKS in volumeinfo:
						image_links = volumeinfo[KEY_IMAGE_LINKS]
						if KEY_THUMBNAIL in image_links:
							thumbnail = image_links[KEY_THUMBNAIL]
							bookfile.write(_tagged("p",'<img src="' + thumbnail + '">'))	
						
					# Move to next cell.
					bookfile.write(HTML_NEXT_CELL)
					
					# Add title if it exists.
					if KEY_TITLE in volumeinfo:
						title = volumeinfo[KEY_TITLE]
					else:
						title = "Untitled"	
					bookfile.write(_tagged("h1", f"{title}"))
					
					# Add subtitle if it exists.
					if KEY_SUBTITLE in volumeinfo:
						subtitle = volumeinfo[KEY_SUBTITLE]
						bookfile.write(_tagged("h2",f"- {subtitle}"))
					
					# Add list of authors if such a list exists.
					authors = ""
					if KEY_AUTHORS in volumeinfo:
						authors = '/'.join(volumeinfo[KEY_AUTHORS])
						try:
							bookfile.write(_tagged("h1", f"   by {authors}"))
						except:
							print("Can't display authors. Sorry.")
					
					# Add publication date if it exists.
					if KEY_PUBDATE in volumeinfo:
						publication_date = volumeinfo[KEY_PUBDATE]
						bookfile.write(_tagged("p",f"Published: {publication_date}"))
					
					# End table.
					bookfile.write(HTML_END_TABLE)
					
					# Add description if it exists.
					if KEY_DESCRIPTION in volumeinfo:
						description = volumeinfo[KEY_DESCRIPTION]
						bookfile.write(_tagged("h2",f"Description:"))
						bookfile.write(_tagged("p", description))
						
					# Close and display HTML file.
					bookfile.close()
					os.startfile(BOOK_FILENAME)
