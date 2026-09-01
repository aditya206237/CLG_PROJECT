"""
Oppenheimer Skill Portal (Team Oppenheimer)
Authentication & User Management Module
----------------------------------------
Provides secure password hashing (SHA-256 + salt) and SQLite persistent storage
for user accounts coexisting in portal.db.
"""

import sqlite3
import hashlib
import secrets
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

BASE_DIR = Path(__file__).parent.resolve()
DB_FILE = BASE_DIR / "portal.db"


def get_db_connection():
    """Returns an active SQLite database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db() -> None:
    """
    Initializes the users table in portal.db if it does not already exist.
    Coexists cleanly with existing database tables (students, skill_responses).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def _hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hashes a password with SHA-256 and a random or provided salt.
    Returns (hex_hash, salt).
    """
    if salt is None:
        salt = secrets.token_hex(16)
    combined = salt + password
    hashed = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return hashed, salt


def register_user(
    username: str,
    password: str,
    full_name: str,
    role: str = "Student"
) -> Tuple[bool, str]:
    """
    Registers a new user in portal.db with salted SHA-256 password hashing.
    
    Validation:
    - Username cannot be empty.
    - Password must be at least 6 characters long.
    - Full Name cannot be empty.

    Returns (True, "") on success or (False, error_message) on failure.
    """
    init_auth_db()
    
    clean_username = username.strip().lower()
    clean_full_name = full_name.strip()
    
    if not clean_username:
        return False, "Username cannot be empty."
    if not clean_full_name:
        return False, "Full Name cannot be empty."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    pwd_hash, salt = _hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, full_name, role, password_hash, salt)
            VALUES (?, ?, ?, ?, ?)
            """,
            (clean_username, clean_full_name, role, pwd_hash, salt)
        )
        conn.commit()
        return True, "Account registered successfully! Please log in."
    except sqlite3.IntegrityError:
        return False, f"Username '{clean_username}' is already taken. Please choose another username."
    except Exception as e:
        return False, f"Registration error: {e}"
    finally:
        conn.close()


def verify_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Verifies user credentials against stored SHA-256 salt + hash.
    
    Returns user info dict {"user_id": ..., "username": ..., "full_name": ..., "role": ...}
    if credentials are valid, or None if invalid.
    """
    init_auth_db()
    clean_username = username.strip().lower()

    if not clean_username or not password:
        return None

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id, username, full_name, role, password_hash, salt
        FROM users
        WHERE username = ?
        """,
        (clean_username,)
    )
    user_row = cursor.fetchone()
    conn.close()

    if not user_row:
        return None

    stored_hash = user_row["password_hash"]
    stored_salt = user_row["salt"]

    calc_hash, _ = _hash_password(password, stored_salt)

    if calc_hash == stored_hash:
        return {
            "user_id": user_row["user_id"],
            "username": user_row["username"],
            "full_name": user_row["full_name"],
            "role": user_row["role"]
        }

    return None


if __name__ == "__main__":
    print("=== Testing Auth Module ===")
    init_auth_db()
    print("[OK] Auth DB initialized.")
    
    # Test Registration
    success, msg = register_user("testuser", "password123", "Test User", "Student")
    print(f"[OK] Register result: {success} -> {msg}")
    
    # Test Duplicate Registration
    dup_success, dup_msg = register_user("testuser", "password123", "Test User", "Student")
    print(f"[OK] Duplicate Register result: {dup_success} -> {dup_msg}")
    
    # Test Verification
    user_info = verify_user("testuser", "password123")
    print(f"[OK] Verify valid user result: {user_info}")
    
    # Test Invalid Verification
    invalid_info = verify_user("testuser", "wrongpass")
    print(f"[OK] Verify invalid user result: {invalid_info}")
