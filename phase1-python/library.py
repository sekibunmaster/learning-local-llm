class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_checked_out = False
    
    def checkout(self):
        if self.is_checked_out:
            print("貸出中です")
        else:
            self.is_checked_out = True
    
    def return_book(self):
        if self.is_checked_out:
            self.is_checked_out = False
        else:
            print("返却済みです")
    
    def info(self):
        if self.is_checked_out:
            print(f"{self.title}, {self.author}, {'貸出中'}")
        else:
            print(f"{self.title}, {self.author}, {'利用可能'}")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
    
    def show_available(self):
        for i in self.books:
            if not i.is_checked_out:
                i.info()