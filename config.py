import os
import dotenv

dotenv.load_dotenv('.env')

TOKEN = os.environ['TOKEN']  # Telegram bot key

# message list
sent_url = "Отправьте мне URL"
video_is_ready = "В каком качестве скачать видео?"
ctn_url = "Если вы хотите загрузить новое видео, отправьте мне URL еще раз!"
