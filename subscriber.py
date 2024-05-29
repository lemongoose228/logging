import time
import paho.mqtt.client as mqtt_client
import random
import requests
import json
import logging
import sys
import time
import platform
from logging.handlers import TimedRotatingFileHandler

broker="broker.emqx.io"

FORMATTER_STRING = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "tmp/sub.log"  # use fancy libs to make proper temp file

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

def getId():
    uri = "http://127.0.0.1:8000/getid"
    try:
        response = requests.get(uri)
        if (response.status_code == 200):
            jsn = json.loads(response.text)
            return jsn["user_id"]
        else:
            logger.error("Ошибка(")
    except Exception as exception:
        logger.error(exception)

def on_message(client, userdata, message):
    time.sleep(1)
    data = str(message.payload.decode("utf-8"))
    logger.info(f"Получено сообщение: '{data}' для пользователя {userid[0:10]}")

logger = get_logger("sub_logger")

userid = getId()

machine_info = f"Публикация запущена на машине: {platform.machine()}, Система: {platform.system()}, Версия: {platform.version()}, Пользователь: {platform.node()} c id: {userid[0:10]}"

logger.info(machine_info)


logger.info(f"Подписчик получил id: {userid[0:10]}") #выводит первые 10 символов

client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION1, 
    userid
)
client.on_message=on_message

logger.info(f"Подключение к брокеру {broker} пользователя {userid[0:10]}")
client.connect(broker) 
client.loop_start() 
logger.info(f"Началось прослушивание пользователя {userid[0:10]}")
client.subscribe("lab/leds/goose")
time.sleep(1800)
logger.warning(f"Прослушивание прекратилось пользователя {userid[0:10]} ")
client.disconnect()
client.loop_stop()

