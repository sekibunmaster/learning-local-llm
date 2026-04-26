from library import Book
from library import Library

lib = Library()
b1 = Book("雪国", "川端康成")
b2 = Book("ラプラスの魔女", "東野圭吾")
b3 = Book("罪と罰", "ドストエフスキー")

lib.add_book(b1)
lib.add_book(b2)
lib.add_book(b3)

b1.checkout()
b2.checkout()
b2.checkout()

#lib.show_available()

lib.save("books.json")

lib2 = Library()
lib2.load("books.json")
lib2.show_available()