import texts.t_user
from config import USERS_DIR

import sqlite3



conn = sqlite3.connect("db/bot_data", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER UNIQUE NOT NULL,
               user_name TEXT NOT NULL,
               admin_rights INTEGER DEFAULT 0 CHECK (admin_rights IN (0, 1)) NOT NULL 
)""")
conn.commit()


def add_new_user(user_id: int, user_name: str) -> str:
    """
    Добавляет пользователя в db по user_id
    """
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    user_status = cursor.fetchone()
    if user_status == None:
        cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
        conn.commit()
        return(texts.t_user.user_added)
    else:
        return(texts.t_user.user_already_added)
        

def remove_user(user_id: int) -> str:
    """
    Удаляет пользователя из db по user_id
    """
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    user_status = cursor.fetchone()
    if user_status == None:
        return(texts.t_user.user_not_exist)
    else:
        cursor.execute(f"DELETE FROM users WHERE user_id=?", (user_id,))
        conn.commit()
        return(texts.t_user.user_removed)


def add_admin_rights(user_id: int) -> str:
    """
    Активирует права админа
    """
    cursor.execute("SELECT admin_rights FROM users WHERE user_id=?", (user_id,))
    user_status = cursor.fetchone()
    if user_status == None:
        return(texts.t_user.user_not_exist)
    else:
        if user_status[0] == 1:
            return(texts.t_user.admin_already_on)
        else:
            cursor.execute("UPDATE users SET admin_rights=? WHERE user_id=?", (1, user_id,))
            conn.commit()
            return(texts.t_user.admin_turn_on)