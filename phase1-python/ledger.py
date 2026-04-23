import json
class Transaction: #確認
    
    def __init__(self, date, content, money, sort):
        self.date = date
        self.content = content
        self.money = money
        self.sort = sort

    def info(self):     #
        print(f"{self.date}, {self.content}, {self.money}, {self.sort}")

    def is_expense(self):
        if self.sort == "支出":
            return True     #
        
        else:
            return False

class Ledger:

    def __init__(self):
        self.ledger = []

    def add(self, transaction):
        self.ledger.append(transaction)     #
    
    def show_expenses(self):
        for e in self.ledger:
            if e.sort == "支出":
                 e.info()
            

    def total_expense(self):
        total=0

        for expense in self.ledger:
            if expense.sort == "支出":
                total += expense.money      #
        
        return total
    
    def save(self, filename):
        data = []
        for i in self.ledger:
            data.append({"date" : i.date, "content" : i.content, "money" : i.money, "sort" : i.sort})
        
        with open (filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):

        self.ledger = []

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        for d in data:
            t = Transaction(d["date"],d["content"], d["money"], d["sort"])
            self.ledger.append(t)
            