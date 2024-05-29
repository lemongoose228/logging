import time
import paho.mqtt.client as mqtt_client
import requests
import json
import logging
import sys
import time
from logging.handlers import TimedRotatingFileHandler
import platform

broker="broker.emqx.io"

FORMATTER_STRING = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "tmp/pub.log"  # use fancy libs to make proper temp file

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


client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION1, 
    'isu100123008765432'
)


def getId():
    uri = "http://127.0.0.1:8001/getid"
    try:
        response = requests.get(uri)
        if (response.status_code == 200):
            jsn = json.loads(response.text)
            return jsn["user_id"]
        else:
            logger.error("Ошибка(")
    except Exception as exception:
        logger.error(exception)

logger = get_logger("pub_logger")

userid = getId()

machine_info = f"Публикация запущена на машине: {platform.machine()}, Система: {platform.system()}, Версия: {platform.version()}, Пользователь: {platform.node()} с id: {userid[0:10]}"

logger.info(machine_info)

logger.info(f"Паблишер получил id: {userid[0:10]}") #выводит первые 10 символов

logger.info(f"Подключение к брокеру {broker} пользоввателя {userid[0:10]}")
client.connect(broker)
client.loop_start()
logger.info(f"Началась публикация пользователя {userid[0:10]}")

for i in range(1):
    #state = "on" if random.randint(0,1) == 0 else "off"
    state = "Привет, мир!"
    logger.info(f"Сообщение: {state} пользователя {userid[0:10]}")
    client.publish("lab/leds/goose", state)
    time.sleep(2)

logger.info(f"Публикация прекратилась для пользователя {userid[0:10]}")
client.disconnect()
client.loop_stop()
