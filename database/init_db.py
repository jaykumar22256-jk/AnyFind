import sqlite3

connection = sqlite3.connect("anyfind.db")

with open("schema.sql", "r") as file:
    schema = file.read()

connection.executescript(schema)

connection.close()

print("Database created successfully!")