from house import Transaction, Ledger

ledger = Ledger()
t1 = Transaction("2026-04-23", "昼食", 800, "支出")
t2 = Transaction("2026-04-23", "給付金", 50000, "収入")
t3 = Transaction("2026-04-23", "交通費", 320, "支出")

ledger.add(t1)
ledger.add(t2)
ledger.add(t3)

ledger.show_expenses()
# 2026-04-23, 昼食, 800, 支出
# 2026-04-23, 交通費, 320, 支出

print(ledger.total_expense())
# 1120

ledger.save("ledger.json")

ledger2 = Ledger()
ledger2.load("ledger.json")
ledger2.show_expenses()
# 2026-04-23, 昼食, 800, 支出
# 2026-04-23, 交通費, 320, 支出