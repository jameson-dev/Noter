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
            self.database_name = "notes"
            self.check_database()
            self.connection.select_db(self.database_name)
            self.check_tables()
        except Exception as e:
            logger.error(e)

    def execute_query(self, query, fetch=False):
        """Helper method to execute SQL queries"""
        try:
            logger.info(f"Executing SQL: {query}")
            self.cursor.execute(query)
            if fetch:
                return self.cursor.fetchall()
        except MySQLdb.Error as e:
            logger.error(f"Error executing query: {e}")

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE {self.database_name}")
            logger.info(f"Database '{self.database_name}' has been created.")
        except MySQLdb.Error as e:
            logger.error(f"Error creating database: {e}")

    def check_tables(self):
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
                """,
            'tags': """
                CREATE TABLE IF NOT EXISTS tags (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL
                    )                        
                """,
            'note_tags': """
                CREATE TABLE IF NOT EXISTS note_tags (
                    note_id INT NOT NULL,
                    tag_id INT NOT NULL,
                    PRIMARY KEY (note_id, tag_id),
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
                    )
                """,
            'user_prefs': """
                CREATE TABLE IF NOT EXISTS user_prefs (
                    user_id INT NOT NULL,
                    theme VARCHAR(50),
                    notifs_enabled BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """,
            'audit_logs': """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    action VARCHAR(255),
                    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
        }

        try:
            existing_tables = self.execute_query("SHOW TABLES", fetch=True)
            existing_tables = [table[0] for table in existing_tables]

            for table_name, table_query in required_tables.items():
                if table_name in existing_tables:
                    logger.info(f"Table '{table_name}' exists.")
                else:
                    self.execute_query(table_query)
                    logger.info(f"Table {table_name}' created")
        except MySQLdb.Error as e:
            logger.error(f"Error checking tables: {e}")

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
