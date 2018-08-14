from numpy import inf

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{user}\'s email has been updated.".format(user=self.name))

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        rating_total = 0
        for rating in self.books.values():
            if rating != None:
                rating_total += rating
        rating_avg = rating_total / len(self.books)
        return rating_avg

    def __repr__(self):
        return "User: {name}, email: {email}, books read: {books}".format(name=self.name, email=self.email, books=len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The ISBN of {title} has been updated to: {isbn}.".format(title=self.title, isbn=new_isbn))

    def add_rating(self, rating):
        if rating != None and 0 <= rating <= 4:
            self.ratings.append(rating)
        elif rating == None:
            pass
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        rating_total = 0
        for rating in self.ratings:
            rating_total += rating
        if len(self.ratings) > 0:
            rating_avg = rating_total / len(self.ratings)
        else:
            rating_avg = 0
        return rating_avg

    def __repr__(self):
        return self.title + ", ISBN: " + str(self.isbn)

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}
        # Each added book is recorded in the book_shelf
        self.book_shelf = {}

    def create_book(self, title, isbn):
        #check if book with ISBN already exists before creating a new book
        if isbn not in self.book_shelf:
            new_book = Book(title, isbn)
            self.book_shelf[isbn] = title
            return new_book
        else:
            print("A book with ISBN {} already exists.".format(isbn))

    def create_novel(self, title, author, isbn):
        #check if book with ISBN already exists before creating a new book
        if isbn not in self.book_shelf:
            new_novel = Fiction(title, author, isbn)
            self.book_shelf[isbn] = title
            return new_novel
        else:
            print("A book with ISBN {} already exists.".format(isbn))

    def create_non_fiction(self, title, subject, level, isbn):
        #check if book with ISBN already exists before creating a new book
        if isbn not in self.book_shelf:
            new_nonfiction = Non_Fiction(title, subject, level, isbn)
            self.book_shelf[isbn] = title
            return new_nonfiction
        else:
            print("A book with ISBN {} already exists.".format(isbn))

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            user = self.users[email]
            if book:
                user.read_book(book, rating)
                book.add_rating(rating)
            else:
                print("Sorry, the book you are trying to read does not exist.")
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {}!".format(email))

    def add_user(self, name, email, user_books=None):
        # validate user email address
        if ('@' in email) and (('.com' in email) or ('.edu' in email) or ('.org' in email)):
            # checks to make sure user email does not already exist before adding a new user
            if email not in self.users:
                new_user = User(name, email)
                self.users[email] = new_user
                if user_books:
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("A user with email address {} already exists.".format(email))
        else:
            print("You have supplied an invalid email address for {}".format(name))

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        book_count = 0
        most_read_book = None
        for book in self.books:
            if self.books[book] > book_count:
                book_count = self.books[book]
                most_read_book = book
        return most_read_book

    def highest_rated_book(self):
        high_rating = float(-inf)
        highest_rated_book = None
        for book in self.books:
            book_avg_rating = book.get_average_rating()
            if book_avg_rating > high_rating:
                high_rating = book.get_average_rating()
                highest_rated_book = book
        return highest_rated_book

    def most_positive_user(self):
        high_user_rating = float(-inf)
        most_positive_user = None
        for user in self.users.values():
            user_avg_rating = user.get_average_rating()
            if user_avg_rating > high_user_rating:
                high_user_rating = user.get_average_rating()
                most_positive_user = user
        return most_positive_user

    def __repr__(self):
        return "This TomeRater has {users} users that have read a total of {books} books.".format(users=len(self.users), books=len(self.books))
