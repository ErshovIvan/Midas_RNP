from aiogram.filters import BaseFilter
from aiogram.types import Message

import sqlite3



conn = sqlite3.connect("db/bot_data", check_same_thread=False)
cursor = conn.cursor()


class IsUserFilter(BaseFilter):
    """
    Фильтр на наличие пользователя в db
    """
    def __init__(self, is_user: bool = True):
        self.is_user = is_user
        
    async def __call__(self, msg: Message) -> bool:
        cursor.execute("SELECT user_id FROM users WHERE user_id=?", (msg.from_user.id,))
        user_status = cursor.fetchone() 
        if self.is_user == True:
            if user_status != None:
                return(True)
            else:
                return(False)
        else:
            if user_status == None:
                return(True)
            else:
                return(False)

        
            
class IsAdminFilter(BaseFilter):
    """
    Фильтр на наличие прав админа в db
    """
    def __init__(self, is_admin: bool = True):
        self.is_admin = is_admin

    async def __call__(self, msg: Message) -> bool:
        cursor.execute("SELECT admin_rights FROM users WHERE user_id=?", (msg.from_user.id,))
        user_status = cursor.fetchone()
        if user_status == None:
            return(False)
        else:
            if self.is_admin == True:
                if user_status[0] == 1:
                    return(True)
                else:
                    return(False)
            else:
                if user_status[0] == 1:
                    return(False)
                else:
                    return(True)