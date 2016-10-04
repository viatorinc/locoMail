__author__ = 'jmoriano'
from mailDTO import MailWrapper
import sqlite3
import os.path
from collections import OrderedDict
class MailDAO(object):
    """
    A simple object to interact with the database and store and retrieve mail objects
    """

    def __init__(self):
        self.__conn = sqlite3.connect('/tmp/mail.db')
        self.__conn.isolation_level = None  # Sets autocommit to true
        sql_tables = "SELECT name FROM sqlite_master WHERE type='table' AND name='table_name';"

        self.__cursor = self.__conn.cursor()

        sql_mail_table = """
        CREATE TABLE IF NOT EXISTS mails (
            id integer primary key,
            subject text,
            from_address text,
            to_address text,
            text text,
            html text,
            created DEFAULT (datetime('now','localtime'))
        )
        """

        self.__cursor.execute(sql_mail_table)


        sql_mail_files_table = """
        CREATE TABLE IF NOT EXISTS attachments (
            id integer primary key,
            mail_id integer,
            file_name text,
            file_contents text
        )
        """

        self.__cursor.execute(sql_mail_files_table)

    def store(self, mail: MailWrapper) -> MailWrapper:
        sql = "INSERT INTO mails (subject, from_address, to_address, text, html) VALUES (?, ?, ?, ?, ?);"
        values_to_insert = (mail.subject, mail.from_address, mail.to_address, mail.text, mail.html)
        self.__cursor.execute(sql, values_to_insert)
        mail.id = self.__cursor.lastrowid
        return mail.id

    def get_by_id(self, id: int) -> MailWrapper:
        sql = """SELECT m.*, a.file_name FROM mails m LEFT JOIN attachments a ON a.mail_id = m.id WHERE m.id = %d ORDER BY m.created DESC""" % id
        result = self.__get_list(sql)
        return result[0]

    def delete_by_id(self, id: int):
        sql ="DELETE FROM mails WHERE id = %d" % id
        self.__cursor.execute(sql)
        sql_delete = "DELETE FROM attachments WHERE mail_id = %d" % id
        self.__cursor.execute(sql_delete)

    def get_by_from_address(self, from_address: str) -> [MailWrapper]:
        sql = "SELECT m.*, a.file_name FROM mails m LEFT JOIN attachments a ON a.mail_id = m.id WHERE m.from_address = '%s' ORDER BY m.created DESC" % from_address
        return self.__get_list(sql)

    def get_by_to_address(self, to_address: str) -> [MailWrapper]:
        sql = "SELECT m.*, a.file_name FROM mails m LEFT JOIN attachments a ON a.mail_id = m.id WHERE m.to_address = '%s'  ORDER BY m.created DESC" % to_address
        return self.__get_list(sql)

    def get_all(self) -> [MailWrapper]:
        sql = "SELECT m.*, a.file_name FROM mails m LEFT JOIN attachments a ON a.mail_id = m.id  ORDER BY m.created DESC"
        return self.__get_list(sql)

    def store_attachments(self, mail_id: int, attachments: dict):
        sql = "INSERT INTO attachments (mail_id, file_name, file_contents) VALUES (?, ?, ?)"
        for file_name, file_contents in attachments.items():
            self.__cursor.execute(sql, (mail_id, file_name, file_contents))

    def get_attachments(self, mail_id: int) -> dict:
        attachments = {}
        sql = "SELECT file_name, file_contents FROM attachments WHERE mail_id = %d"
        rs = self.__cursor.execute(sql % mail_id)
        for entry in rs:
            attachments[entry[0]] = entry[1]

        return attachments


    def __get_list(self, sql):
        attachments = {}  # Key is mail id, value is a list
        results = []
        rs = self.__cursor.execute(sql)
        all = rs.fetchall()
        added_mails = []
        for row in all:
            mail_wrapper = MailWrapper.from_row(row)
            if mail_wrapper.id not in added_mails:
                added_mails.append(mail_wrapper.id)

                results.append(mail_wrapper)

            file_names = attachments.get(mail_wrapper.id, [])
            file_names.append(row[-1])
            attachments[mail_wrapper.id] = file_names

        for result in results:
            my_attachments = attachments.get(result.id, [])
            result.set_attachments(my_attachments)
        return results