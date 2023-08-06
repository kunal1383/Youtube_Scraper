    
from flask import Flask, render_template, request, Response
from youtube_scrapper import YouTubeScraper
import logging
import os
from mysqldb import MySQLHandler

os.makedirs('youtube_scraper',exist_ok=True)
logging.basicConfig(filename='youtube_scraper/youtube_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
application = Flask(__name__)
app = application

@app.route('/', methods=['GET','POST'])
def homePage():
    return render_template("index.html", show_result=False)


@app.route("/find", methods=['GET','POST'])
def find():
    try:
        if request.method == "POST":
            url = request.form.get("search_query")
            youtube = YouTubeScraper()
            logging.info(f"Received URL: {url}")

            info = {}  # Define 'info' variable with default empty dictionary

            if 'youtube.com' in url:
                if '@' in url:
                    channel_info = youtube.get_channel_info(url)
                    if channel_info:
                        handler = MySQLHandler()
                        handler.connect()
                        handler.create_database()
                        handler.create_channels_table()
                        handler.insert_channel_info(channel_info)
                        handler.close()
                        info = channel_info  # Assign channel_info to 'info' variable
                    else:
                        error_message = "Channel information not found"
                        return render_template("index.html", show_result=True, error_message=error_message)
                elif '?v=' in url:
                    video_info = youtube.get_video_info(url)
                    if video_info:
                        handler = MySQLHandler()
                        handler.connect()
                        handler.create_database()
                        handler.create_videos_table()
                        handler.insert_video_info(video_info)
                        handler.close()
                        info = video_info  # Assign video_info to 'info' variable
                    else:
                        error_message = "Video information not found"
                        return render_template("index.html", show_result=True, error_message=error_message)
                else:
                    error_message = f"Error Occurred: {url} is invalid"
                    return render_template("index.html", show_result=True, error_message=error_message)
            else:
                error_message = f"Error Occurred: {url} is not a valid YouTube URL"
                return render_template("index.html", show_result=True, error_message=error_message)

            return render_template("index.html", show_result=True, info=info)  # Render template with 'info' variable
    except Exception as e:
        error_message = f"Error Occurred: {e}"
        return render_template("index.html", show_result=True, error_message=error_message)

    # Default return statement for the case when no information is found
    error_message = "Unable to fetch details."
    return render_template("index.html", show_result=True, error_message=error_message)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000 ,debug=True)
