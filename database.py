import MySQLdb
from loguru import logger
from config import Config


""" Add configuration file"""
config = Config()


class Database:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host=config.get('Database', 'db_host'),
            user=config.get('Database', 'db_username'),
            passwd=config.get('Database', 'db_password')
        )
        self.cursor = self.connection.cursor()
        self.database_name = "notes"
        self.check_database()
        self.connection.select_db(self.database_name)
        self.check_tables()

    def create_database(self):
        self.cursor.execute(f"CREATE DATABASE {self.database_name}")
        logger.info(f"Database '{self.database_name}' has been created.")

    def create_tables(self, table_name, query):
        required_tables = {
            'users': """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                    )
                """,
            'notes': """
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    content TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """
        }

        existing_tables = self.execute_query("SHOW TABLES", fetch=True)
        existing_tables = [table[0] for table in existing_tables]

        for table_name, table_query in required_tables.items():
            if table_name in existing_tables:
                logger.info(f"Table '{table_name} exists.")
            else:
                self.create_tables(table_name, table_query)

            print(f"Table '{table}' created.")

    def check_database(self):
        self.cursor.execute(f"SHOW DATABASES LIKE '{self.database_name}'")
        result = self.cursor.fetchone()

        if result:
            logger.info(f"Database '{self.database_name}' exists.")
        else:
            self.create_database()

    def check_tables(self):
        required_tables = ['users', 'notes']

        self.cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in self.cursor.fetchall()]

        for table in required_tables:
            if table in existing_tables:
                logger.info(f"Table '{table}' exists.")
            else:
                if table == 'notes':
                    self.create_tables(table)
                elif table == 'users':
                    self.create_tables(table)

    def close_conn(self):
        if self.cursor:
            self.cursor.close()
            logger.info("SQL Cursor closed.")
        if self.connection:
            self.connection.close()
            logger.info("SQL Connection closed.")
