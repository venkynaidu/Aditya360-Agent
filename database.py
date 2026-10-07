import sqlite3, hashlib, secrets, re
from datetime import datetime

DB = "students.db"

def conn():
    c = sqlite3.connect(DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")

def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200000).hex()

def register(student_id, name, email, department, year, password):
    student_id, name, email = student_id.strip().upper(), name.strip(), email.strip().lower()
    if not re.fullmatch(r"[A-Z0-9_-]{4,30}", student_id):
        return False, "Student ID must be 4–30 letters/numbers."
    if "@" not in email or len(password) < 8:
        return False, "Enter a valid email and password of at least 8 characters."
    salt = secrets.token_hex(16)
    try:
        with conn() as c:
            c.execute("""INSERT INTO students(student_id,name,email,department,year,salt,password_hash,created_at)
                       VALUES(?,?,?,?,?,?,?,?)""",
                      (student_id,name,email,department,year,salt,_hash(password,salt),
                       datetime.now().isoformat(timespec="seconds")))
        return True, "Registration successful. You can now sign in."
    except sqlite3.IntegrityError:
        return False, "Student ID or email is already registered."

def authenticate(student_id, password):
    with conn() as c:
        row = c.execute("SELECT * FROM students WHERE student_id=?", (student_id.strip().upper(),)).fetchone()
    if row and secrets.compare_digest(row["password_hash"], _hash(password,row["salt"])):
        return dict(row)
    return None
