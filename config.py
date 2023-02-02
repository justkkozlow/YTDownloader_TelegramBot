import os
import dotenv

dotenv.load_dotenv('.env')

TOKEN = os.environ['TOKEN']  # Telegram bot key

# message list
start_message = "Sent YouTube URL:"
choose_resolution_message = "Availble resolution to download:"
