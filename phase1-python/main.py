from book import Book

books = [
    Book("雪国", "川端康成", 208),
    Book("動物農場", "オーウェル", 155),
    Book("ラプラスの魔女", "東野圭吾", 493),
]

for i in books:
    if i.is_long():
        print (i.info())