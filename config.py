import os
import dotenv

dotenv.load_dotenv('.env')

TOKEN = os.environ['TOKEN']  # Telegram bot key

# message list
start_message = "Hello, I'm a bot that can download YouTube videos!\n" \
                "If the size of the uploaded video is less than 50 MB,\n " \
                "I can send you the video directly here\n" \
                "Sent me the URL:"
video_is_ready = "I can download video on:"
