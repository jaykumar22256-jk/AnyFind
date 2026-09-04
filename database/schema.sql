CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT,
    state TEXT,
    description TEXT,
    services TEXT,
    courses TEXT,
    specialties TEXT,
    address TEXT,
    phone TEXT,
    website TEXT
);