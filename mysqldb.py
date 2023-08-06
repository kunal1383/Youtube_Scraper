import sqlite3
import logging
import os

class MySQLHandler:
    def __init__(self):
        self.db_file = 'youtube.db'
        self.connection = None
        self.cursor = None
        log_directory = 'SQLITEDB'
        log_file = 'sqldb.log'
        os.makedirs(log_directory, exist_ok=True)
        
        # Create a new logger
        self.logger = logging.getLogger('SQLiteHandler')
        self.logger.setLevel(logging.INFO)
        
        # Create a file handler for the logger
        file_handler = logging.FileHandler(os.path.join(log_directory, log_file))
        file_handler.setLevel(logging.INFO)
        
        # Create a formatter and set it for the file handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        
        if not os.path.exists(self.db_file):
            self.create_database()
        self.connect()

    def create_database(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            self.logger.info(f'Successfully connected to SQLite database: {self.db_file}')
        except sqlite3.Error as e:
            self.logger.error(f'Failed to connect to SQLite database: {e}')
            raise Exception

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            self.logger.error(f'Failed to connect to SQLite database: {e}')
            raise Exception

    def create_channels_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY,
                    channelName TEXT,
                    profileImageURL TEXT,
                    viewCount INTEGER,
                    subscriberCount INTEGER,
                    hiddenSubscriberCount INTEGER,
                    videoCount INTEGER
                )
            """)
            self.logger.info("Channels table created successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to create channels table: {e}")

    def create_videos_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    comments TEXT,
                    likes INTEGER,
                    thumbnailURL TEXT
                )
            """)
            self.logger.info("Videos table created successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to create videos table: {e}")

    def insert_channel_info(self, channel_info):
        try:
            sql = """
                INSERT INTO channels
                (channelName, profileImageURL, viewCount, subscriberCount, hiddenSubscriberCount, videoCount)
                VALUES
                (?, ?, ?, ?, ?, ?)
            """
            values = (
                channel_info['channelName'],
                channel_info['channelProfileImage'],
                channel_info['viewCount'],
                channel_info['subscriberCount'],
                channel_info['hiddenSubscriberCount'],
                channel_info['videoCount']
            )
            self.cursor.execute(sql, values)
            self.connection.commit()
            self.logger.info("Channel information inserted successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to insert channel information: {e}")

    def insert_video_info(self, video_info):
        try:
            sql = """
                INSERT INTO videos
                (title, description, comments, likes, thumbnailURL)
                VALUES
                (?, ?, ?, ?, ?)
            """
            values = (
                video_info['title'],
                video_info['details'],
                ", ".join(video_info['comments']),
                video_info['likes'],
                video_info['thumbnail']
            )
            self.cursor.execute(sql, values)
            self.connection.commit()
            self.logger.info("Video information inserted successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to insert video information: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            self.logger.info("SQLite connection closed")
