import json

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
        self.books = [] #格納されるbooknはBookオブジェクトになっている

    def add_book(self, book):
        self.books.append(book)
    
    def show_available(self):
        for i in self.books:
            if not i.is_checked_out:
                i.info()
    
    def save(self, filename):
        data = []
        for book in self.books:
            data.append({"title": book.title, "author" : book.author, "is_checked_out" : book.is_checked_out})
            
        with open(filename, "w", encoding="utf-8") as f :
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):

        self.books = []

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for d in data:
            book = Book(d["title"], d["author"])
            book.is_checked_out = d["is_checked_out"]
            self.books.append(book)


