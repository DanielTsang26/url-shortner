import mysql.connector
import logging

logging.basicConfig(level = logging.DEBUG)

class Database:
    """This is the database class that holds information that accesses the database on MySQL"""
    def __init__ (self, host="localhost", user="root", password="dT!181290", database="url_shortener"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        logging.debug(f"Database config initialized: host={self.host}, user={self.user}, database={self.database}")


    def connect(self):
        """creates and returns a MySQL connection"""
        try:
            conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
            logging.info(" Database connection established!")
            return conn
        except mysql.connector.Error as e:
            logging.err(f" Database connection failed: {e}")
            raise
    
       
    
    
