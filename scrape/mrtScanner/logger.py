import json
import boto3
import configparser
import os
from datetime import datetime
from calendar import timegm
from os import environ

import watchtower, logging
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

class Logger:
  date = ''
  stream = ''
  directory = ''
  group = "/scanner-logs"
  stream_prefix = environ.get('TRAIN_ID') or environ.get('RESIN_DEVICE_UUID') or config['default']['train_id']

  session, logs = None, None

  # watchtower logging
  logger = None

  def __init__(self, stream_category='', boto3_session=None):
    # Set log variables
    self.date = datetime.now().strftime('%Y-%m-%d')
    self.stream = self.stream_prefix if not stream_category else self.stream_prefix+'_'+stream_category

    # Create log file directory
    self.directory = 'logs/' + self.stream_prefix + '/' + self.date
    if not os.path.exists(self.directory):
      os.makedirs(self.directory)

    # Create logging object
    self.logger = logging.getLogger(__name__)

    if os.environ.get('LOG_TO_CLOUDWATCH', False):
        self.logger.addHandler(watchtower.CloudWatchLogHandler(
          log_group = self.group,
          stream_name = self.stream,
          use_queues = True,
          send_interval = 10,
          boto3_session = boto3_session
        ))

    if os.environ.get('LOG_TO_FILE', False):
        self.logger.addHandler(logging.FileHandler(self.directory + '/log.txt'))

  def log(self, text):
    try:
      self.logger.info(str(text))
    except Exception as error:
      print "Error logging to AWS"
      try:
          self.logger.error(error)
      except:
          print "Failed logging to file"
