# BASIC LIBRARY MANAGEMENT SYSTEM
## Description:
Library Management System Project that supports operations
*Searching* book in the catalogue and *searching online* incase not found in catalogue,
*Adding* new book or another copy of the existing book,
*Removing* A book, and *Listing* all the books which are available in Library
after *authenticating* the staff id and password.

## About Files in this Directory

### project.py

This python file contains *main()* function and all remaining functions which are listed below.

### admin_ids.csv

It contains *staff ids, passwords and names* of staff members of Library. This CSV file is used for validating staff id and password entered during *login* process.

### books.csv

This CSV file contains the information about all the books available in the Library. It  follows the sequence *"isbn, title, authors, quantity, published date"*.

### requirements.txt

This text file lists all the python third party *libraries* which are *required* for this project.

## Function Reference

### main()

The main() function is the *entry point* of the entire program. It *coordinates* the program control and the execution of other functions in the program. This also provides *menu of actions* for the staff member after login.

### authenticate()

This function authenticates the staff login by *checking credentials* entered
against the details stored in admin_ids.csv file.  
**Parameters**: None  
**Returns**: staff id and name of the logged in staff member  

### get_isbn()

A function to *get input* which is isbn number and *validates* using the functions available isbnlib library.
**Parameters**: None  
**Returns**: isbn if valid, None otherwise  

### search_book(book_id)

Function that searches for the book in library *catalogue* using Book ISBN.  
**Parameters**: book_id which is isbn number of book  
**Returns**:dict object that contains book information if found

### search_online(book_id)

This function searches for the book on the *web* by ISBN number and uses *Google Books API* to search and retrieve the Book Information.  
**Parameters**: book_id which is isbn number of book  
**Returns**:dict object that contains book information if found

### add_book(isbn)

This function is for *adding* a new book to the *catalogue* or increasing the no of copies of that book by 1 if already exist.   
**Parameters**: isbn number of book  
**Returns**: isbn number of the added book, -1 if isbn number is invalid

### remove_book(isbn)

It is for *removing* a copy of the book or removing the book completely from *catalogue* if only one book exist in library.  
**Parameters**: isbn number of book   
**Returns**: isbn of the removed book, -1 book not found

### get_book_list()

This function is to get the list of books available in Library.  
**Parameters**: None  
**Returns**: Dataframe object that contains details of all books available in library

### show_book_details(book)

This function prints details of the given book     
**Parameters**: dict object that contains book information as input  
**Returns**: None

## Dependencies

### requests

This Project make use of *get()* function and *json()* method of this library.

### isbnlib 
*is_isbn10(), to_isbn10(), is_isbn13()* and *to_isbn13()* functions of this library are used in this project.

### pandas

*read_csv(), to_dict()* functions, *drop(), to_csv()*, methods and *at, loc, index* properties of this library are utilized.

### cowsay

tux() function of this library is imported.

### validator_collection

is_date() function of this library is leveraged in this project.

## Thank you

Thankyou for spending time to read this README file. I hope you found it Useful and Informative.