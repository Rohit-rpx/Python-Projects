""" Basic Library Management System Project that supports operations
Searching book in the catalogue and searching online incase not found in catalogue,
Adding new book or another copy of the existing book,
Removing A book, and Listing all the books which are available in Library
after authenticating the staff id and password"""

import sys
import pandas as pd
import requests
import isbnlib
import cowsay
import re
from validator_collection import checkers as ch

def main():
    staff_id, name = authenticate()
    print(f"{"\t"*6}Welcome", name)

    while True:
        print("\n(1) Search Book\n(2) Add Book\n(3) List all Books")
        print("(4) Remove Book\n(5) Logout")
        try:
            choice = int(input("\nEnter option: "))
            if not 1 <= choice <= 5:
                raise ValueError
        except ValueError:
            print("\nInvalid Option\n")
            continue

        match choice:
            case 1:
                if isbn := get_isbn():
                    if book := search_book(isbn):
                        show_book_details(book)
                    else:
                        opt = (
                            input("\n\nWould you like to search online?(y/n) ")
                            .strip()
                            .lower()[0]
                        )
                        if opt == "y":
                            if book := search_online(isbn):
                                show_book_details(book)

                else:
                    print("\n\nInvalid ISBN number")

            case 2:
                if isbn:= get_isbn():
                    id = add_book(isbn)
                    if id == -1:
                        print("\n\n\nBook Addition Failed!!")
                    else:
                        print(f"\n\n\nBook with ISBN: {id} successfully added")
                        print(f"\nstaff id: {staff_id}   name: {name}")
                else:
                    print("\n\nInvalid ISBN number!!")

            case 3:
                print(get_book_list())

            case 4:
                if isbn := get_isbn():
                    id = remove_book(isbn)
                    if id == -1:
                        print("\n\n\nBook Removal failed")
                    else:
                        print(f"\n\n\nBook with ISBN: {id} has been removed")
                        print(f"\nstaff id: {staff_id}  name: {name}")
                else:
                    print("\n\nInvalid ISBN number")

            case 5:
                print("\n\n\nSuccessflly logged out\n\n")
                cowsay.tux("Thank you")
                sys.exit()
        try:
            input("Press enter to continue...")
        except KeyboardInterrupt:
            sys.exit()
        

def authenticate():
    """This function authenticates the staff login by checking credentials entered
    against the details stored in admin_ids.csv file.
    returns id and name of the staff member"""

    try:
        id1 = int(input("User id: "))
    except ValueError:
        sys.exit("\nuser id must be numeric!!!")
    password = input("Password: ")
    df = pd.read_csv("admin_ids.csv", index_col="id")
    try:
        fr = df.loc[id1]
        if fr["password"] != password:
            raise ValueError
    except KeyError:
        sys.exit("\n\nUser id not found")
    except ValueError:
        sys.exit("\n\nIncorrect password")
    return id1, fr["name"]


def get_isbn():
    """A function to take input which is isbn number and validates
    using the functions available in isbnlib library.
    returns isbn if valid None otherwise"""

    isbn = input("\n\nEnter book isbn: ")
    if isbnlib.is_isbn10(isbn):
        isbn = isbnlib.to_isbn10(isbn)
    elif isbnlib.is_isbn13(isbn):
        isbn = isbnlib.to_isbn13(isbn)
    else:
        return None
    return isbn


def search_book(book_id):
    """Function that searches for the book in library catalogue using Book ISBN.
    takes isbn number as input,
    returns dict object that contains book information if found"""

    df = pd.read_csv("books.csv", index_col="isbn", dtype={"isbn": object})
    try:
        fr = df.loc[book_id].to_dict()
        fr["isbn"] = book_id
        return fr
    except KeyError:
        print("\n\nBook Not found in Catalougue\n\n")


def search_online(book_id):
    """This function searches for the book on the web by ISBN number
    and uses Google Books API to search and retrieve the Book Information.
    takes isbn number as input,
    returns dict object that contains book information if found"""

    url = f"https://www.googleapis.com/books/v1/volumes/?q=isbn:{book_id}"
    response = requests.get(url)
    try:
        details = response.json()["items"][0]["volumeInfo"]
        return {
            "isbn": book_id,
            "title": details["title"],
            "authors": " ".join(details["authors"]),
            "published date": details["publishedDate"],
            "language": details["language"],
        }
    except KeyError:
        print("\n\nBook not Found!!")
        return None


def add_book(isbn):
    """This function is for adding a new book to the catalogue or
    increasing the no of copies of that book by 1 if already exist.
    returns isbn number of the added book, -1 if isbn number is invalid"""

    df = pd.read_csv("books.csv", index_col="isbn", dtype={"isbn": object})
    if book := search_book(isbn):
        print(
            f"\n\nA book found with ISBN: {isbn} Title: {book['title']}\nIncreasing quantity by 1"
        )
        df.at[book["isbn"], "quantity"] += 1
    else:
        title = input("Enter book name: ").strip().title()
        authors = input("Enter Author[s] name: ").strip().title()
        pdate = input("Enter publish date: ").strip()
        if (
            re.search(r"^[\w\s,.]+$", title)
            and re.search(r"^[a-zA-Z\s,.]+$", authors)
            and ch.is_date(pdate)
        ):
            book = {
                "title": title,
                "authors": authors,
                "quantity": 1,
                "published date": pdate,
            }
            df.loc[isbn] = book
        else:
            print(
                "\n\nInvalid Book details, make sure the details are in common format"
            )
            return -1
    df.to_csv("books.csv")
    return isbn
    


def remove_book(isbn):
    """It is for removing a copy of the book or removing the book completely from
    catalogue if only one book exist in library.
    returns isbn of the removed book, -1 if either invalid isbn or book not found"""

    df = pd.read_csv("books.csv", index_col="isbn", dtype={"isbn": object})
    if book := search_book(isbn):
        if book["quantity"] > 1:
            print(f"\n\nRemoving one copy of the book '{book['title']}'")
            df.at[isbn, "quantity"] -= 1
        elif book["quantity"] == 1:
            print(f"\n\nRemoving the book '{book['title']}'")
            df.drop(isbn, inplace=True)
        df.to_csv("books.csv")
        return isbn
    else:
        print(f"\n\n\nBook with ISBN: {isbn} Not Found!!")
        return -1


def get_book_list():
    """This function returns the Dataframe object that contains details
    of all books available in library"""

    df = pd.read_csv("books.csv", dtype={"isbn": object})
    df.index += 1
    return df


def show_book_details(book):
    """This function prints details of the given book
    takes dict object that contains book information as input"""

    print(f"\n{'\t'*6}Book Details\n")
    for i in book:
        print(f"{i} :  {book[i]}")


if __name__ == "__main__":
    main()
