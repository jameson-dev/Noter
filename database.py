import MySQLdb
from loguru import logger


class Database:
    def __init__(self, config):
        try:
            self.connection = MySQLdb.connect(
                host=config.get('Database', 'db_host'),
                user=config.get('Database', 'db_username'),
                passwd=config.get('Database', 'db_password')
            )
            self.cursor = self.connection.cursor()
            self.database_name = "noter"
            self.check_database()
            self.connection.select_db(self.database_name)
        except Exception as e:
            logger.error(e)

    def execute_query(self, query, fetch=False):
        """Helper method to execute SQL queries"""
        try:
            logger.info(f"Executing SQL: {query}")
            self.cursor.execute(query)
            if fetch:
                return self.cursor.fetchall()
            self.connection.commit()
        except MySQLdb.Error as e:
            logger.error(f"Error executing query: {e}")

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE {self.database_name}")
            logger.info(f"Database '{self.database_name}' has been created.")
            self.connection.commit()
        except MySQLdb.Error as e:
            logger.error(f"Error creating database: {e}")

    def check_database(self):
        try:
            self.cursor.execute(f"SHOW DATABASES LIKE '{self.database_name}'")
            result = self.cursor.fetchone()

            if result:
                logger.info(f"Database '{self.database_name}' exists.")
            else:
                self.create_database()
        except MySQLdb.Error as e:
            logger.error(f"Error checking database: {e}")

    def close_conn(self):
        if self.cursor:
            self.cursor.close()
            logger.info("SQL Cursor closed.")
        if self.connection:
            self.connection.close()
            logger.info("SQL Connection closed.")
