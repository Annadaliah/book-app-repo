import logging
import re

import re

def remove_ansi_escape_sequences(text):
    # This regex removes any ANSI escape codes (like color codes)
    ansi_escape = re.compile(r'\x1b\[([0-9]{1,2};){0,2}[0-9]{1,2}m')
    return ansi_escape.sub('', text)

logging.basicConfig(level=logging.INFO, filename="logs/log.txt", filemode="a",
     format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

handler = logging.FileHandler('logs/log.txt') 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
handler.setFormatter(formatter) 

logger.addHandler(handler) 

class CleanFileHandler(logging.FileHandler):
    def emit(self, record):
        try:
            # Remove any ANSI escape sequences from the message before logging to the file
            record.msg = remove_ansi_escape_sequences(record.getMessage())
        except Exception as e:
            pass
        super().emit(record)

# Add the custom file handler that removes color codes
file_handler = CleanFileHandler('logs/log.txt')

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Disable werkzeug (Flask HTTP server) logs that generate colored output
logging.getLogger('werkzeug').setLevel(logging.ERROR)