import logging

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

logger = logging.getLogger(__name__)


class Database:

    def __init__(
        self,
        host: str,
        user: str,
        port: int,
        password: str,
        database: str,
        charset: str = "utf8",
        timeout: int = 60,
    ) -> None:
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database
        self.timeout = timeout
        self.charset = charset

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.database,
            port=self.port,
            charset=self.charset,
            cursorclass=DictCursor,
        )

    def query(self, sql: str, args: list):
        with self.get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(sql, args)
            results = cursor.fetchall()

            return results

    def query_one(self, sql: str, args: list):
        return self.query(sql, args)[0]

    def insert_one(self, sql: str, args: list):
        with self.get_connection() as connection, connection.cursor() as cursor:
            rows_affected = cursor.execute(sql, args)
            if rows_affected == 1:
                logger.info("we have successfully inserted into the DB")
                connection.commit()
            else:
                logger.warning("i am rolling back")
                connection.rollback()
                raise RuntimeError(
                    f"Unable to insert record into the DB. Failed Statement: {sql}, args: {args}"
                )

    def update(self, sql: str, args: list):
        with self.get_connection() as connection, connection.cursor() as cursor:
            rows_affected = cursor.execute(sql, args)
            if rows_affected == 1:
                logger.info("successfully updated record")
                connection.commit()
            if rows_affected == 0:
                logger.info("did not update any record")
                connection.commit()
