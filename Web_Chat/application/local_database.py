import sqlite3
from sqlite3 import Error
from datetime import datetime
import time

# CONSTANTS

FILE = "messages.db"
PLAYLIST_TABLE = "Messages"


class DataBase:
    """
    used to  write to and read from a local sqlite3 database
    """
    def __init__(self):

        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        """
        close the db
        :return: None
        """
        self.conn.close()

    def _create_table(self):
        """
        make new db table if no
        :return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit=100, your_name=None):
        """
        return all of the messages
        :param your_name: handle user name
        :param limit: int
        :return: list[dict]
        """
        if not your_name:
            query = f"SELECT * FROM {PLAYLIST_TABLE}"
            self.cursor.execute(query)
        else:
            query = f"SELECT * FROM {PLAYLIST_TABLE} WHERE NAME = ?"
            self.cursor.execute(query, (your_name,))

        result = self.cursor.fetchall()

        # return messages in sorted order by date
        results = []
        for r in sorted(result, key=lambda x: x[3], reverse=True)[:limit]:
            your_name, content, date, _id = r
            data = {"name":your_name, "message":content, "time":str(date)}
            results.append(data)

        return list(reversed(results))

    def get_messages_by_name(self, name, limit_messages=100):
        """
        return list of messages according to the user

        :param limit_messages: hard code limit
        :param name: str
        :return: list
        """
        return self.get_all_messages(limit_messages, name)

    def save_message(self, your_name, message):
        """
        place message
        :param message: message to db
        :param your_name: name to db
        :param time: datetime
        :return: None
        """
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (your_name, message, datetime.now(), None))
        self.conn.commit()