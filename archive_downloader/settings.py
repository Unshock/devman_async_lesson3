import os
import dotenv


dotenv.load_dotenv()

SLOWING_STATE = bool(int(os.getenv('SLOWING_STATE', 0)))
SLOWING_TIME = int(os.getenv('SLOWING_TIME', 3))

STORAGE_DIRECTORY = os.getenv('STORAGE_DIRECTORY', 'files_storage')
CHUNK_SIZE_KB = int(os.getenv('CHUNK_SIZE_KB', 512))

LOG_SHOW_STATE = bool(int(os.getenv('LOG_SHOW_STATE', 1)))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
