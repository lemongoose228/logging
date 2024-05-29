from fastapi import FastAPI
import hashlib
import datetime
import uvicorn
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

app = FastAPI()

FORMATTER_STRING = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "tmp/serv.log"  # use fancy libs to make proper temp file

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)

    return logger

logger = get_logger("serv_logger")

@app.get("/getid")
async def root():
    time_str = str(datetime.datetime.now())
    userid = hashlib.md5(time_str.encode()).hexdigest()
    logger.info(f"Id сгенерирован {userid[0:10]}")
    return {"user_id": userid}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


