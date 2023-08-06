# Youtube Scraper

## Description

This project is a YouTube data scrapper that allows you to fetch information about YouTube channels and videos. The scrapper is implemented in Python and uses the YouTube Data API to retrieve the data.

## Installation

To use this project, follow these steps:

1. Clone the repository to your local machine using the following command:
   ```
   git clone https://github.com/kunal1383/your-repo.git
   ```

2. Create a new Conda environment to install the required dependencies. Run the following command from the project directory:
   ```
   conda create --name youtube-scrapper python=3.8
   conda activate youtube-scrapper
   ```

3. Install the required packages using pip:
   ```
   pip install -r requirements.txt
   ```

4. Obtain a YouTube Data API key from the Google Developer Console. You can find more information on how to get the API key [here](https://developers.google.com/youtube/registering_an_application).

5. After obtaining the API key, open the `utils.py` file in the project directory and replace the `YOUR_YOUTUBE_API_KEY` variable with your actual API key.

## Usage

To run the YouTube data scrapper, execute the main script `main.py` using the following command:
```
python main.py
```

The script will prompt you to enter a YouTube channel URL or video URL, and it will fetch and display the relevant information.

## Important Note

Please note that this project requires a valid YouTube Data API key to function properly. You must obtain your own API key from the Google Developer Console and insert it into the `utils.py` file. Failing to provide the API key will result in the scrapper not working.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.