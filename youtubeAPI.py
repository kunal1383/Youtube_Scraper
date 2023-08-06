from utils import KEY
from googleapiclient.discovery import build

class APIBuilder:
    
    def __init__(self):
        pass
    @staticmethod
    def youtube_api():
        youtube = build('youtube', 'v3', developerKey=KEY)
        return youtube