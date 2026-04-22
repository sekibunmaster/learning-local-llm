class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def info(self):
        return f"{self.title},{self.author},{self.pages}"
    
    def is_long(self):
        return self.pages >= 300
    
#book = Book("雪国", "川端康成", 208)
#print(book.info())
#print(book.is_long())