from flask import Flask, request
import logging
from logging.handlers import SMTPHandler


logger = logging.getLogger()
logger.setLevel(logging.INFO)
LOG_FILENAME = 'webhook.log'

fh = logging.handlers.TimedRotatingFileHandler(
    LOG_FILENAME, when="midnight", interval=1, backupCount=90, encoding="utf-8", delay=False)

formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                              '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


app = Flask(__name__)

@app.route('/webhook',  methods=['POST'])
def webhook():

    logger.info(f"MESSAGE: {request.data.decode()}")

    return {'code': 200}


@app.route('/webhook/get', methods=['GET'])
def webhook_get():
    logger.info(f"MESSAGE: {request.query_string.decode()}")

    return {'code': 200}

if __name__ == "__main__":
    app.run(port=5666, use_reloader=False)

