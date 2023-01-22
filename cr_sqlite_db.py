from pydantic import BaseModel
import sqlite3

class User(BaseModel):
    username: str
    password: str

def save_user_to_db(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)'''
    )

    c.execute(
        '''INSERT INTO users (username, password) VALUES (?,?)''', (username, password)
    )

    conn.commit()
    conn.close()