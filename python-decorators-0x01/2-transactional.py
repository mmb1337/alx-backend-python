#!/usr/bin/python3
"""
Transaction Management Decorator - Corrected Implementation
"""
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator that automatically handles database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    
    return wrapper

def transactional(func):
    """
    Decorator that manages database transactions.
    Automatically commits on success or rolls back on error.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            # If no errors, commit changes
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise
    
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')