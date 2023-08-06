from flask import Flask, render_template, request, Response
from youtubeAPI import APIBuilder
from googleapiclient.errors import HttpError
import logging
import os


os.makedirs('youtube_scraper', exist_ok=True)
logging.basicConfig(filename='youtube_scraper/youtube_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class YouTubeScraper:
    def __init__(self):
        self.youtube = APIBuilder.youtube_api()

    def get_channel_info(self, channel_url):
        logging.info("Extracting channel information")
        username = channel_url.split('@')[-1]
        channel_ids = {
            "krishnaik06": 'UCNU_lfiiWBdtULKOw6X0Dig',
            "iNeuroniNtelligence": 'UCb1GdqUqArXMQ3RS86lqqOw',
            "CollegeWallahbyPW": 'UCDrf0V4fcBr5FlCtKwvpfwA'
        }

        if username in channel_ids:
            channel_id = channel_ids[username]
        else:
            channel_id = None

        try:
            if channel_id:
                response = self.youtube.channels().list(
                    part='snippet,contentDetails,statistics',
                    id=channel_id
                ).execute()
            else:
                response = self.youtube.channels().list(
                    part='snippet,contentDetails,statistics',
                    forUsername=username
                ).execute()

            if 'items' in response and response['items']:
                channel_info = {
                    'channelName': response['items'][0]['snippet']['title'],
                    'channelProfileImage': response['items'][0]['snippet']['thumbnails']['default']['url'],
                    'viewCount': response['items'][0]['statistics']['viewCount'],
                    'subscriberCount': response['items'][0]['statistics']['subscriberCount'],
                    'hiddenSubscriberCount': response['items'][0]['statistics']['hiddenSubscriberCount'],
                    'videoCount': response['items'][0]['statistics']['videoCount']
                }
                #print(f"channelInfo: {channel_info}")
                logging.info("Channel information fetched successfully")
                return channel_info

            else:
                logging.warning("No channel information found")
                return None

        except HttpError as e:
            logging.error(f"An HTTP error occurred while fetching channel information: {e}")
            return {}


    def get_video_info(self, video_url):
        logging.info("Extracting video information")
        video_id = self.get_video_id(video_url)
        try:
            response = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()
            video_data = response['items'][0]
            title = video_data['snippet']['title']
            details = video_data['snippet']['description']
            likes = video_data['statistics']['likeCount']
            thumbnail = video_data['snippet']['thumbnails']['high']['url']
            comments = self.get_comments(video_id)
            return {
                'title': title,
                'details': details,
                'likes': likes,
                'thumbnail': thumbnail,
                'comments': comments
            }
        except HttpError as e:
            logging.error(f"An HTTP error occurred while fetching video information: {e}")
            return None

    def get_video_id(self, video_url):
        logging.info("Extracting video id")
        video_id = None
        try:
            if 'youtube.com' in video_url:
                video_id = video_url.split('?v=')[1].split('&')[0]
            elif 'youtu.be' in video_url:
                video_id = video_url.split('/')[-1]
            return video_id
        except Exception as e:
            logging.error(f"An error occurred while extracting video id: {e}")
            return None

    def get_comments(self, video_id):
        logging.info("Extracting video comments")
        try:
            response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=10
            ).execute()
            comments = []
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                author = comment['authorDisplayName']
                text = comment['textDisplay']
                comments.append(f"{author}: {text}")
            return comments
        except HttpError as e:
            logging.error(f"An HTTP error occurred while fetching video comments: {e}")
            return []