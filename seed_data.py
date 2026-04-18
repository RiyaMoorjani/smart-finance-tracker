#data base info of 2025 
import database as db
from datetime import date

db.init_db()

transactions = [
    # April 2025 — income
    ("2025-04-01", "income",  "salary",        45000, "Monthly salary"),
    ("2025-04-15", "income",  "freelance",       8000, "Web design project"),

    # April 2025 — expenses
    ("2025-04-02", "expense", "rent",           12000, "Monthly rent"),
    ("2025-04-03", "expense", "food",            3200, "Groceries"),
    ("2025-04-05", "expense", "dining out",      2100, "Restaurants/Zomato"),
    ("2025-04-07", "expense", "transport",       1500, "Metro + cab"),
    ("2025-04-10", "expense", "stocks",         10000, "Nifty 50 ETF"),
    ("2025-04-12", "expense", "utilities",       1800, "Electricity + internet"),
    ("2025-04-14", "expense", "entertainment",   2500, "OTT + movies"),
    ("2025-04-18", "expense", "shopping",        3500, "Clothes"),
    ("2025-04-22", "expense", "mutual funds",    4000, "SIP"),
    ("2025-04-25", "expense", "healthcare",       800, "Doctor + medicine"),
    ("2025-04-28", "expense", "subscriptions",   1200, "Netflix, Spotify"),

    # March 2025
    ("2025-03-01", "income",  "salary",         45000, "Monthly salary"),
    ("2025-03-03", "expense", "rent",           12000, "Monthly rent"),
    ("2025-03-04", "expense", "food",            2800, "Groceries"),
    ("2025-03-06", "expense", "dining out",      1800, "Swiggy"),
    ("2025-03-08", "expense", "stocks",         12000, "Reliance, TCS"),
    ("2025-03-10", "expense", "transport",       1200, "Metro pass"),
    ("2025-03-15", "expense", "utilities",       1600, "Electricity"),
    ("2025-03-20", "expense", "shopping",        4200, "Amazon"),
    ("2025-03-24", "expense", "mutual funds",    4000, "SIP"),
    ("2025-03-28", "expense", "entertainment",   1800, "Movies + games"),

    # February 2025
    ("2025-02-01", "income",  "salary",         45000, "Monthly salary"),
    ("2025-02-02", "expense", "rent",           12000, "Monthly rent"),
    ("2025-02-05", "expense", "food",            3000, "Groceries"),
    ("2025-02-08", "expense", "stocks",          8000, "HDFC Bank"),
    ("2025-02-10", "expense", "transport",       1100, "Cab + metro"),
    ("2025-02-12", "expense", "utilities",       1500, "Bills"),
    ("2025-02-15", "expense", "travel",          6000, "Trip to Jaipur"),
    ("2025-02-18", "expense", "dining out",      2200, "Valentines dinner"),
    ("2025-02-20", "expense", "mutual funds",    4000, "SIP"),
    ("2025-02-25", "expense", "healthcare",      1200, "Gym membership"),
]

for t in transactions:
    db.add_transaction(*t)

print(f" Seeded {len(transactions)} transactions.")
