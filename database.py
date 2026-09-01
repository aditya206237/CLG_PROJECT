"""
SQLite Database Access Layer for AIIA Skill Assessment Portal
--------------------------------------------------------------
Provides persistent storage using Python's built-in sqlite3 standard library.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any

# Database path relative to database module location
BASE_DIR = Path(__file__).parent.resolve()
DB_FILE = BASE_DIR / "portal.db"

_db_initialized = False


def get_connection(db_path: Path = DB_FILE) -> sqlite3.Connection:
    """Returns a SQLite database connection with Foreign Keys enabled."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Path = DB_FILE, force: bool = False) -> None:
    """Creates portal.db and required database tables if they do not exist."""
    global _db_initialized
    if _db_initialized and not force:
        return

    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        # Students Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target_role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Skill Responses Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_responses (
            response_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            skill_id TEXT NOT NULL,
            self_rating INTEGER NOT NULL,
            quiz_adjusted_rating INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE
        );
        """)
        conn.commit()
    _db_initialized = True


def save_student(name: str, target_role: str, db_path: Path = DB_FILE) -> int:
    """
    Inserts a new student record into the database.
    Returns the newly generated integer student_id.
    """
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, target_role) VALUES (?, ?)",
            (name.strip(), target_role.strip())
        )
        conn.commit()
        if cursor.lastrowid is None:
            raise RuntimeError("Failed to retrieve generated student_id.")
        return cursor.lastrowid


def save_skill_responses(
    student_id: int,
    raw_ratings: Dict[str, int],
    adjusted_ratings: Dict[str, int],
    db_path: Path = DB_FILE
) -> None:
    """
    Saves a student's raw self-ratings and quiz-adjusted ratings into skill_responses table.
    """
    init_db(db_path)
    rows = []
    for skill_id, self_val in raw_ratings.items():
        adj_val = adjusted_ratings.get(skill_id, self_val)
        rows.append((student_id, skill_id, int(self_val), int(adj_val)))

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO skill_responses (student_id, skill_id, self_rating, quiz_adjusted_rating)
            VALUES (?, ?, ?, ?)
            """,
            rows
        )
        conn.commit()


def get_student_skill_vector(student_id: int, db_path: Path = DB_FILE) -> Dict[str, int]:
    """
    Retrieves the quiz-adjusted skill vector {skill_id: quiz_adjusted_rating} for a student.
    """
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT skill_id, quiz_adjusted_rating FROM skill_responses WHERE student_id = ?",
            (student_id,)
        )
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}


def get_student_responses_full(student_id: int, db_path: Path = DB_FILE) -> List[Dict[str, Any]]:
    """
    Retrieves complete skill response records including self_rating and quiz_adjusted_rating.
    """
    init_db(db_path)
    with get_connection(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT response_id, student_id, skill_id, self_rating, quiz_adjusted_rating, created_at "
            "FROM skill_responses WHERE student_id = ?",
            (student_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]



def get_all_students(db_path: Path = DB_FILE) -> List[Dict[str, Any]]:
    """
    Retrieves all student records ordered by submission time for admin/institution dashboards.
    """
    init_db(db_path)
    with get_connection(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_id, name, target_role, created_at FROM students ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    print("=== Testing SQLite Database Layer ===")
    try:
        init_db()
        print("[OK] Database schema initialized successfully.")

        # Test inserting dummy student
        sid = save_student("Demo Student", "Data Science")
        print(f"[OK] Test Student created with ID: {sid}")

        # Test inserting skill responses
        raw_vec = {"py_prog": 5, "sql_db": 4}
        adj_vec = {"py_prog": 5, "sql_db": 3}
        save_skill_responses(sid, raw_vec, adj_vec)
        print("[OK] Skill responses saved successfully.")

        # Test retrieval
        retrieved_vec = get_student_skill_vector(sid)
        print(f"[OK] Retrieved skill vector for Student #{sid}: {retrieved_vec}")

        students_list = get_all_students()
        print(f"[OK] Total students in DB: {len(students_list)}")

    except Exception as e:
        print(f"[ERROR] Database Test Error: {e}")
