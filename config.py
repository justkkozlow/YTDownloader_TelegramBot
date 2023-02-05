import os
import dotenv

dotenv.load_dotenv('.env')

TOKEN = os.environ['TOKEN']  # Telegram bot key

# message list
sent_url = "Отправьте мне YouTube ссылку"
url_error = "Некорректная ссылка"
video_is_ready = "В каком качестве скачать видео?"
too_large_file = "Размер видео превышает допустимые 50 мб, но я все равно его скачал"
ctn_url = "Если вы хотите загрузить новое видео, отправьте мне URL еще раз!"
