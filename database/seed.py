import sqlite3

connection = sqlite3.connect("anyfind.db")

places = [
    (
        "Example University Ahmedabad",
        "University",
        "Ahmedabad",
        "Gujarat",
        "A test university record for developing AnyFind.",
        "",
        "Computer Science, Artificial Intelligence, Machine Learning",
        "",
        "Ahmedabad, Gujarat",
        "",
        ""
    ),
    (
        "Example Engineering College Mehsana",
        "University",
        "Mehsana",
        "Gujarat",
        "A test engineering college record for developing AnyFind.",
        "",
        "Computer Science, Information Technology",
        "",
        "Mehsana, Gujarat",
        "",
        ""
    ),
    (
        "Example Heart Hospital Ahmedabad",
        "Hospital",
        "Ahmedabad",
        "Gujarat",
        "A test hospital record for developing AnyFind.",
        "Heart treatment, Cardiology",
        "",
        "Cardiology",
        "Ahmedabad, Gujarat",
        "",
        ""
    )
]

connection.executemany("""
    INSERT INTO places
    (name, category, city, state, description, services,
     courses, specialties, address, phone, website)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", places)

connection.commit()
connection.close()

print("Test data added successfully!")