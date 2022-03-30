from abc import ABC, abstractmethod
import sqlite3


class AbstractCountModel(ABC):
    @abstractmethod
    def get_count(self, user_id: str) -> int: ...

    @abstractmethod
    def increment_count(self, user_id: str) -> None: ...

    @abstractmethod
    def decrement_count(self, user_id: str) -> None: ...

    @abstractmethod
    def reset_count(self, user_id: str) -> None: ...

    @abstractmethod
    def add_user(self, user_id: str) -> None: ...

    @abstractmethod
    def remove_user(self, user_id: str) -> None: ...

    @abstractmethod
    def close(self) -> None: ...


class CountModelException(Exception):
    pass


class UserCountAlreadyExistException(CountModelException):
    def __init__(self, user_id: str):
        super().__init__(f'user "{user_id}" already exist.')


class UserCountNotFoundException(CountModelException):
    def __init__(self, user_id: str):
        super().__init__(f'user "{user_id}" is not found.')


class SqliteCountModel(AbstractCountModel):
    def __init__(self, dpath: str):
        self.dbpath = dpath
        self.connection = sqlite3.connect(self.dbpath)
        cursor = self.connection.cursor()
        sql_create_table = '''CREATE TABLE IF NOT EXISTS loginsData (
            username TEXT PRIMARY KEY,
            counter INT
            );'''
        cursor.execute(sql_create_table)

    def get_count(self, user_id: str) -> int:
        cur = self.connection.cursor()
        cur.execute("SELECT counter FROM loginsData WHERE username =:user", {"user" : user_id})
        a = cur.fetchone()
        if(a != None):
            return a[0]
        else:
            raise UserCountNotFoundException(user_id=user_id)

    def increment_count(self, user_id: str) -> None: 
        cur = self.connection.cursor()
        cur.execute("UPDATE loginsData SET counter = counter + 1 WHERE username=:user", {"user" : user_id})
        self.connection.commit()

    def decrement_count(self, user_id: str) -> None:
        cur = self.connection.cursor()
        cur.execute("UPDATE loginsData SET counter = counter - 1 WHERE username=:user", {"user" : user_id})
        self.connection.commit()

    def reset_count(self, user_id: str) -> None:
        cur = self.connection.cursor()
        cur.execute("UPDATE loginsData SET counter = 0 WHERE username=:user", {"user" : user_id})   
        self.connection.commit()
       
    def add_user(self, user_id: str) -> None:
        cur = self.connection.cursor()
        try:
            cur.execute("INSERT INTO loginsData VALUES (?, ?)",(user_id, 0))
        except sqlite3.IntegrityError:
            raise UserCountAlreadyExistException(user_id=user_id)
        self.connection.commit()
        
    def remove_user(self, user_id: str) -> None:
        cur = self.connection.cursor()
        cur.execute("DELETE FROM loginsData WHERE username =:user", {"user" : user_id})
        self.connection.commit()
      
    def close(self) -> None:
        self.connection.close()


class DictCountModel(AbstractCountModel):
    def __init__(self):
        self.dict = dict()

    def get_count(self, user_id: str) -> int:
        try:
            return self.dict[user_id]
        except KeyError:
            raise UserCountNotFoundException(user_id=user_id)

    def increment_count(self, user_id: str) -> None:
        try:
            self.dict[user_id] += 1
        except KeyError:
            raise UserCountNotFoundException(user_id=user_id)

    def decrement_count(self, user_id: str) -> None:
        try:
            self.dict[user_id] -= 1
        except KeyError:
            raise UserCountNotFoundException(user_id=user_id)

    def reset_count(self, user_id: str) -> None:
        if user_id not in self.dict:
            raise UserCountNotFoundException(user_id=user_id)
        self.dict[user_id] = 0

    def add_user(self, user_id: str) -> None:
        if user_id in self.dict:
            raise UserCountAlreadyExistException(user_id=user_id)
        self.dict[user_id] = 0

    def remove_user(self, user_id: str) -> None:
        if user_id not in self.dict:
            raise UserCountNotFoundException(user_id=user_id)
        del self.dict[user_id]

    def close(self) -> None:
        pass

